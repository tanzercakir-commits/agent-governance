"""Bounded source regression checks for LAB-001/002/003, not runtime verification."""
import hashlib
import re
import unittest
from pathlib import Path
from scripts.build_guide import render_guide

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md"


def section(text: str, heading: str) -> str:
    start = text.index(heading) + len(heading)
    match = re.search(r"^#{1,4} ", text[start:], re.M)
    return text[start:start + match.start()] if match else text[start:]


class SourceRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = GUIDE.read_text(encoding="utf-8")
        match = re.search(r"```python\n(def canonical_pr_body\(body: str\) -> bytes:.*?)(?:\n```)", cls.text, re.S)
        if not match:
            raise AssertionError("missing normative canonical_pr_body implementation")
        # CI is read-only. This executes the source's tiny reference function,
        # not any received PR's privileged governance runtime.
        namespace = {}
        exec(compile(match.group(1), "<canonical_pr_body specification>", "exec"), namespace)
        cls.canon = staticmethod(namespace["canonical_pr_body"])

    def test_obsolete_absolute_clauses_are_absent(self):
        for obsolete in (
            "preserves every prior TODO byte",
            "Any PR body edit invalidates the payload",
            "Any head or body change invalidates",
            "Reject any body edit after verification",
            "any changed PR-body byte",
            "verifier invalidation on any body edit",
            "any body edit invalidates it",
            "Failed completion or amendment attempts leave governed ledgers byte-for-byte unchanged",
            "amendment failure leaves TODO unchanged",
            "failed transition leaves both inputs unchanged",
        ):
            with self.subTest(clause=obsolete):
                self.assertNotIn(obsolete, self.text)

    def test_all_amendment_validators_name_shared_projection(self):
        for heading in ("#### Trusted amendment-ledger mode", "### `finalize-amendment`", "### `validate-final`", "### `audit-main`", "### Repository self-check"):
            with self.subTest(heading=heading):
                self.assertIn("project_amendment", section(self.text, heading))

    def test_projection_has_three_explicit_cases(self):
        body = section(self.text, "### Shared amendment projection: `project_amendment`")
        for required in ("**Pending:**", "**Terminal:**", "**Invalid:**", "header/contract", "sentinel-plus-task", "self-check", "only TODO"):
            with self.subTest(required=required):
                self.assertIn(required, body)

    def test_both_finalizers_distinguish_publication(self):
        for heading in ("### `finalize`", "### `finalize-amendment`"):
            with self.subTest(heading=heading):
                body = section(self.text, heading)
                for required in ("UNPUBLISHED", "PUBLISHED_UNVERIFIED", "UNKNOWN", "ref"):
                    self.assertIn(required, body)

    def test_final_status_attempt_is_a_last_call_boundary(self):
        body = section(self.text, "### `validate-final`")
        self.assertIn("After attempting final success publication, make no further remote call", body)
        self.assertIn("read-only reconciliation", body)
        self.assertIn("canonical_pr_body", body)

    def test_invariant_is_branch_scoped(self):
        body = section(self.text, "## Repository state")
        for required in ("Before PR-branch ref publication", "After publication", "UNKNOWN", "Neither finalizer mutates the default branch", "candidate"):
            self.assertIn(required, body)

    def test_no_task_completion_for_owner_amendment(self):
        self.assertIn("An owner amendment changes only TODO and never records a task completion in PROGRESS", self.text)

    def test_distribution_is_byte_identical(self):
        copy = ROOT / "skills/project-governance-bootstrap/references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md"
        self.assertEqual(GUIDE.read_bytes(), copy.read_bytes())
        parts = sorted((ROOT / "spec/parts").glob("[0-9][0-9].md"))
        self.assertEqual(len(parts), 4)
        self.assertEqual(GUIDE.read_bytes(), render_guide(ROOT))

    def test_build_jobs_test_exact_pr_head_without_persisted_credentials(self):
        workflow = section(self.text, "### `.github/workflows/build-and-test.yml`")
        self.assertEqual(workflow.count("ref: ${{ github.event.pull_request.head.sha || github.sha }}"), 2)
        self.assertEqual(workflow.count('test "$(git rev-parse HEAD)" = "$EXPECTED_SHA"'), 2)
        self.assertEqual(workflow.count("persist-credentials: false"), 2)

    def test_governance_entrypoints_do_not_prepend_unprotected_cwd(self):
        workflow_text = self.text[self.text.index("## 13. GitHub Actions workflows"):self.text.index("## 14. Governance package contract")]
        commands = re.findall(r"python3 (.*?)project_governance ", workflow_text)
        self.assertEqual(len(commands), 6)
        for options in commands:
            self.assertEqual(options, "-P -m ")
        self.assertIn("python3 -P - <<'PY'", workflow_text)
        self.assertNotIn("python3 - <<'PY'", workflow_text)
        self.assertIn("python3 -P -m unittest discover", workflow_text)
        self.assertIn("Python 3.11 or later", workflow_text)
        self.assertIn("must not contain the repository root or an empty entry", workflow_text)

    def test_policy_can_read_the_provenance_it_validates(self):
        workflow = section(self.text, "### `.github/workflows/governance-pr.yml`")
        for permission in ("actions: read", "checks: read", "statuses: write"):
            self.assertIn(permission, workflow)
        self.assertIn("if: github.ref == format('refs/heads/{0}', github.event.repository.default_branch)", workflow)
        self.assertIn("ref: ${{ github.sha }}", workflow)

    def test_hidden_ruleset_fields_require_attested_baseline_and_drift_recovery(self):
        for clause in ("not an empty bypass list", "after the entire last mutation second",
                       "Never automatically refresh the attestation", "add-and-restore within a later single second"):
            self.assertIn(clause, self.text)

    def test_canonical_equivalence_cases(self):
        expected = b"A\nB\n"
        for raw in ("A\nB", "A\nB\n", "A\nB\n\n", "A\r\nB\r\n", "A\rB\r"):
            with self.subTest(raw=raw):
                self.assertEqual(self.canon(raw), expected)

    def test_whitespace_and_unicode_are_not_trimmed(self):
        for left, right in (("Scope: A", "Scope:  A"), ("A", "A "), ("A", "A\t"), ("A\nB", "A\n\nB"), ("é", "e\u0301"), ("A\nB", "B\nA")):
            with self.subTest(left=left, right=right):
                self.assertNotEqual(self.canon(left), self.canon(right))
                self.assertNotEqual(hashlib.sha256(self.canon(left)).digest(), hashlib.sha256(self.canon(right)).digest())

    def test_canonicalizer_is_utf8_strict_and_idempotent(self):
        for text in ("değişiklik", "", "A\r\n\r\n", "A "):
            value = self.canon(text)
            self.assertEqual(self.canon(value.decode("utf-8")), value)
            self.assertTrue(value.endswith(b"\n"))
            self.assertFalse(value.endswith(b"\n\n"))
        with self.assertRaises(UnicodeEncodeError):
            self.canon("\ud800")

    def test_equivalence_is_not_edit_history_attestation(self):
        self.assertIn("not raw-byte or edit-history binding", self.text)
        self.assertIn("Missing/non-string API bodies", self.text)

    def test_risk_proportional_profiles_do_not_force_strict_on_routine_work(self):
        for required in (
            "PRACTICAL — default for ordinary product development",
            "REVIEWED — material but ordinary engineering risk",
            "STRICT — high-assurance boundary",
            "What may block the current task",
            "Governance budget",
            "non-blocking discovery does not expand the active task",
            "Mandatory STRICT governance tests",
            "Final STRICT bootstrap acceptance checklist",
            "DEFER",
            "REPRIORITIZE",
            "SUPERSEDE",
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.text)
        self.assertNotIn(
            "Every non-trivial implementation or change separates implementation from verification.",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
