"""Durable/concurrent protocol model tests; no GitHub commissioning claim."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import asdict, replace
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from spec.reference.attempts import Candidate, Record, Rejected, Unknown, run_phase, reconciled_success


class Store:
    """Test adapter for authenticated create-only refs, backed by a UNIQUE key."""
    def __init__(self, path):
        self.path = path
        self.trace = []
        self.fault = None
        with closing(sqlite3.connect(path)) as db, db:
            db.execute("CREATE TABLE IF NOT EXISTS records (k TEXT, slot TEXT, data TEXT, PRIMARY KEY(k, slot))")

    def read(self, key):
        self.trace.append("read")
        with closing(sqlite3.connect(self.path)) as db:
            rows = db.execute("SELECT slot, data FROM records WHERE k = ?", (key,)).fetchall()
        result = {}
        for slot, raw in rows:
            data = json.loads(raw)
            data["candidate"] = Candidate(**data["candidate"])
            result[slot] = Record(**data)
        return result

    def create(self, key, slot, record):
        self.trace.append(slot)
        if self.fault == (slot, "before"):
            raise Unknown("uncommitted response loss")
        try:
            with closing(sqlite3.connect(self.path)) as db, db:
                db.execute("INSERT INTO records VALUES (?, ?, ?)", (key, slot, json.dumps(asdict(record))))
        except sqlite3.IntegrityError as error:
            raise Rejected("already admitted/decided") from error
        if self.fault == (slot, "after"):
            raise Unknown("committed response loss")


class AttemptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Store(str(Path(self.temp.name) / "attempts.sqlite"))
        self.candidate = Candidate(1, 3, "a" * 40, "b" * 40, "c" * 64, "task")
        self.statuses = []

    def phase(self, phase, *, work=lambda: None, last=None, owner=None, candidate=None):
        owner = owner or phase + "@trusted-code:run-1:attempt-1"
        candidate = candidate or self.candidate
        if last is None:
            def last():
                self.store.trace.append("last")
                if phase == "validate":
                    self.statuses.append(Record(candidate, owner, "SUCCESS", True))
        return run_phase(self.store, candidate, phase, owner, work, last)

    def accepted(self, candidate=None, **kwargs):
        return reconciled_success(self.store, candidate or self.candidate, self.statuses,
                                  other_gates_pass=kwargs.get("gates", True),
                                  complete=kwargs.get("complete", True))

    @staticmethod
    def fail():
        raise RuntimeError("known validation/publication failure")

    def test_failure_then_rerun_and_fabricated_success_stay_rejected(self):
        self.assertEqual(self.phase("publish"), "SENT")
        self.assertEqual(self.phase("validate", work=self.fail), "FAILED")
        for owner in ("validate@trusted-code:run-1:attempt-2", "validate@trusted-code:run-2:attempt-1"):
            self.assertEqual(self.phase("validate", owner=owner), "REJECTED")
        self.statuses.append(Record(self.candidate, "validate@trusted-code:run-1:attempt-1", "SUCCESS", True))
        self.assertFalse(self.accepted())

    def test_restart_does_not_reset_admission(self):
        self.assertEqual(self.phase("publish", work=self.fail), "FAILED")
        self.store = Store(self.store.path)
        self.assertEqual(self.phase("publish"), "REJECTED")
        self.assertEqual(self.phase("validate"), "REJECTED")

    def test_concurrent_first_admission_has_one_winner(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda n: self.phase("publish", owner=f"trusted:{n}:1"), range(16)))
        self.assertEqual(results.count("SENT"), 1)
        self.assertEqual(results.count("REJECTED"), 15)
        self.assertEqual(self.store.trace.count("last"), 1)

    def test_unknown_publication_with_and_without_remote_commit_cannot_retry(self):
        for committed in (False, True):
            with self.subTest(committed=committed):
                candidate = replace(self.candidate, pr=10 + int(committed))
                refs = []
                def work():
                    if committed:
                        refs.append(candidate.ledger)
                    raise Unknown("ref-update response lost")
                self.assertEqual(self.phase("publish", candidate=candidate, work=work), "UNKNOWN")
                self.assertEqual(self.phase("publish", candidate=candidate), "REJECTED")
                self.assertEqual(len(refs), int(committed))
                self.assertFalse(self.accepted(candidate))

    def test_failure_record_response_loss_and_process_death_block_success(self):
        self.phase("publish")
        for index, timing in enumerate(("before", "after")):
            candidate = replace(self.candidate, pr=20 + index)
            self.phase("publish", candidate=candidate)
            self.store.fault = ("validate/outcome", timing)
            self.assertEqual(self.phase("validate", candidate=candidate, work=self.fail), "UNKNOWN")
            self.store.fault = None
            self.assertEqual(self.phase("validate", candidate=candidate), "REJECTED")
            self.assertFalse(self.accepted(candidate))
        def crash():
            raise SystemExit("process death")
        with self.assertRaises(SystemExit):
            self.phase("validate", work=crash)
        self.assertEqual(self.phase("validate"), "REJECTED")
        self.assertFalse(self.accepted())

    def test_unknown_last_call_is_only_read_only_reconciled(self):
        for index, committed in enumerate((False, True)):
            candidate = replace(self.candidate, pr=30 + index)
            self.phase("publish", candidate=candidate)
            self.statuses = []
            def last():
                self.store.trace.append("last")
                if committed:
                    self.statuses.append(Record(candidate, "validate@trusted-code:run-1:attempt-1", "SUCCESS", True))
                raise Unknown("success response lost")
            self.assertEqual(self.phase("validate", candidate=candidate, last=last), "UNKNOWN")
            self.assertEqual(self.store.trace[-1], "last")
            self.assertEqual(self.accepted(candidate), committed)
            self.assertEqual(self.phase("validate", candidate=candidate), "REJECTED")
            self.assertEqual(self.accepted(candidate), committed)

    def test_duplicate_dispatch_does_not_poison_success_or_inflight(self):
        self.phase("publish")
        def work():
            self.assertEqual(self.phase("validate", owner="duplicate:2:1"), "REJECTED")
        self.assertEqual(self.phase("validate", work=work), "SENT")
        before = self.store.read(self.candidate.key)
        self.assertEqual(self.phase("validate"), "REJECTED")
        self.assertEqual(before, self.store.read(self.candidate.key))
        self.assertTrue(self.accepted())

    def test_complete_pending_to_success_history_and_invalid_statuses(self):
        self.phase("publish")
        self.phase("validate")
        success = self.statuses[0]
        pending = Record(self.candidate, "publish@trusted-code:run-1:attempt-1", "PENDING", True)
        self.statuses = [pending, success]
        self.assertTrue(self.accepted())
        for statuses in ([pending], [success, pending],
                         [replace(pending, owner="forged"), success],
                         [pending, replace(success, owner="another-run")],
                         [pending, replace(success, trusted=False)],
                         [pending, replace(success, event="FAILURE"), success]):
            with self.subTest(statuses=statuses):
                self.statuses = statuses
                self.assertFalse(self.accepted())

    def test_alternate_attempt_identity_cannot_allocate_a_new_candidate(self):
        self.phase("publish", work=self.fail)
        for change in ({"ledger": "d" * 40}, {"source": "e" * 40},
                       {"body_sha256": "e" * 64}, {"operation": "amendment"}):
            self.assertEqual(self.phase("publish", candidate=replace(self.candidate, **change)), "REJECTED")
        fresh = replace(self.candidate, pr=50, source="f" * 40)
        self.phase("publish", candidate=fresh)
        self.phase("validate", candidate=fresh)
        self.assertTrue(self.accepted(fresh))

    def test_malformed_untrusted_wrong_candidate_and_incomplete_history(self):
        self.phase("publish")
        self.phase("validate")
        real_read = self.store.read
        original = real_read(self.candidate.key)
        variants = [{}, {k: v for k, v in original.items() if k != "validate/claim"},
                    dict(original, surprise=original["publish/claim"])]
        for change in ({"trusted": False}, {"owner": "forged"},
                       {"candidate": replace(self.candidate, pr=99)}, {"event": "FAILED"}):
            variants.append(dict(original, **{"validate/outcome": replace(original["validate/outcome"], **change)}))
        for records in variants:
            with self.subTest(records=records):
                self.store.read = lambda key: records
                self.assertFalse(self.accepted())
        self.store.read = real_read
        self.assertFalse(self.accepted(complete=False))
        self.assertFalse(self.accepted(gates=False))
        self.statuses.insert(0, replace(self.statuses[0], event="FAILURE"))
        self.assertFalse(self.accepted())

    def test_ambiguous_admission_or_ready_never_calls_success(self):
        self.phase("publish")
        for index, (slot, timing) in enumerate((("validate/claim", "after"),
                                              ("validate/outcome", "before"),
                                              ("validate/outcome", "after"))):
            candidate = replace(self.candidate, pr=60 + index)
            self.phase("publish", candidate=candidate)
            self.store.fault = (slot, timing)
            self.assertEqual(self.phase("validate", candidate=candidate), "UNKNOWN")
            self.store.fault = None
            self.assertFalse(self.accepted(candidate))
            self.assertEqual(self.phase("validate", candidate=candidate), "REJECTED")
