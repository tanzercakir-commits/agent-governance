"""Executable protocol model, not a GitHub adapter or authentication service.

Store.create must atomically create an immutable authenticated record or raise;
Store.read must return a complete authenticated snapshot or raise. The adapter,
never PR data, supplies producer trust and the workflow/run/attempt identity.
"""
from dataclasses import dataclass
import re


class Rejected(ValueError):
    pass


class Unknown(RuntimeError):
    pass


@dataclass(frozen=True)
class Candidate:
    repository_id: int
    pr: int
    source: str
    ledger: str
    body_sha256: str
    operation: str

    def __post_init__(self):
        if (type(self.repository_id) is not int or self.repository_id <= 0
                or type(self.pr) is not int or self.pr <= 0
                or self.operation not in ("task", "amendment")):
            raise Rejected("invalid scope")
        for value, length in ((self.source, 40), (self.ledger, 40), (self.body_sha256, 64)):
            if not isinstance(value, str) or not re.fullmatch(rf"[0-9a-f]{{{length}}}", value):
                raise Rejected("invalid digest")
        if self.source == self.ledger:
            raise Rejected("ledger must differ from source")

    @property
    def key(self):
        # A different run, body, operation or ledger does not create a fresh slot.
        return f"v1/{self.repository_id}/{self.pr}"


@dataclass(frozen=True)
class Record:
    candidate: Candidate
    owner: str  # Authenticated workflow path + trusted code SHA + run ID + attempt.
    event: str
    trusted: bool  # Adapter output after provenance verification, not wire input.


def checked_history(store, candidate):
    records = store.read(candidate.key)
    allowed = {f"{phase}/{kind}" for phase in ("publish", "validate")
               for kind in ("claim", "outcome")}
    if not isinstance(records, dict) or not set(records) <= allowed:
        raise Rejected("malformed history")
    for slot, record in records.items():
        if (not isinstance(record, Record) or record.trusted is not True
                or record.candidate != candidate or not isinstance(record.owner, str)
                or not record.owner or record.event not in ("CLAIM", "READY", "FAILED")):
            raise Rejected("untrusted or mismatched history")
        if slot.endswith("/claim"):
            if record.event != "CLAIM":
                raise Rejected("invalid admission")
        else:
            claim = records.get(slot.replace("/outcome", "/claim"))
            if (claim is None or claim.owner != record.owner
                    or record.event not in ("READY", "FAILED")):
                raise Rejected("outcome without its admitted producer")
    if any(slot.startswith("validate/") for slot in records):
        ready = records.get("publish/outcome")
        if ready is None or ready.event != "READY":
            raise Rejected("validation without authorized dispatch")
    return records


def run_phase(store, candidate, phase, owner, work, last_call):
    """Only an acknowledged first claim may work; no call follows last_call.

    publish work: exact ref publication, verified policy, finalizer audit.
    validate work: all exact final gates and durable final audit comment.
    last_call: final dispatch (publish) or success status (validate).
    Admission/provenance errors and duplicates never publish a failure status.
    """
    if phase not in ("publish", "validate") or not isinstance(owner, str) or not owner:
        raise Rejected("invalid caller")
    try:
        records = checked_history(store, candidate)
        if phase == "validate":
            if records.get("publish/outcome") is None or records["publish/outcome"].event != "READY":
                return "REJECTED"
        if f"{phase}/claim" in records:
            return "REJECTED"
        store.create(candidate.key, f"{phase}/claim", Record(candidate, owner, "CLAIM", True))
    except Rejected:
        return "REJECTED"
    except Exception:
        return "UNKNOWN"  # No acknowledged ownership; do not mutate anything else.
    try:
        work()
    except Unknown:
        return "UNKNOWN"  # A surviving claim is sufficient to prohibit replay.
    except Exception:
        try:
            store.create(candidate.key, f"{phase}/outcome", Record(candidate, owner, "FAILED", True))
        except Exception:
            return "UNKNOWN"  # The immutable claim still prevents replay.
        return "FAILED"
    try:
        store.create(candidate.key, f"{phase}/outcome", Record(candidate, owner, "READY", True))
    except Exception:
        return "UNKNOWN"  # Includes an ambiguous READY write: never proceed.
    try:
        last_call()
    except Exception:
        return "UNKNOWN"
    return "SENT"  # Transport acknowledgement alone is not FINALIZED.


def reconciled_success(store, candidate, statuses, *, other_gates_pass, complete):
    """Read-only: all status pages and all other live gates are mandatory inputs.

    statuses are authenticated Record values with PENDING/SUCCESS/FAILURE events for
    governance/queue-finalized on this exact candidate, including historical ones.
    """
    if other_gates_pass is not True or complete is not True:
        return False
    try:
        records = checked_history(store, candidate)
    except Exception:
        return False
    if len(records) != 4 or any(records[f"{p}/outcome"].event != "READY" for p in ("publish", "validate")):
        return False
    owner = records["validate/claim"].owner
    publisher = records["publish/claim"].owner
    if not statuses:
        return False
    success = False
    for status in statuses:
        if (not isinstance(status, Record) or status.trusted is not True
                or status.candidate != candidate):
            return False
        if status.event == "PENDING" and status.owner == publisher and not success:
            continue  # Only the initial publisher pending, in ascending ID order.
        if status.event == "SUCCESS" and status.owner == owner:
            success = True
        else:
            return False
    return success
