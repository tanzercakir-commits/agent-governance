"""Regression checks for the fail-closed immutable release workflow."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/release.yml"


class ReleaseWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_release_is_manual_main_only_and_exact_source_bound(self):
        self.assertIn("workflow_dispatch:", self.text)
        self.assertIn('test "$GITHUB_REF" = "refs/heads/main"', self.text)
        self.assertIn('test "$(git rev-parse HEAD)" = "$GITHUB_SHA"', self.text)
        self.assertIn('test "$remote_main" = "$GITHUB_SHA"', self.text)

    def test_release_actions_are_sha_pinned(self):
        self.assertIn(
            "uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            self.text,
        )
        self.assertIn(
            "uses: actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6",
            self.text,
        )

    def test_write_token_is_not_job_wide_environment(self):
        prefix = self.text.split("    steps:", 1)[0]
        self.assertNotIn("GH_TOKEN:", prefix)
        self.assertIn("GH_TOKEN: ${{ github.token }}", self.text)

    def test_verification_capabilities_are_checked_before_release_mutation(self):
        create = self.text.index('gh release create "$tag"')
        for command in (
            "gh attestation verify --help",
            "gh release verify --help",
            "gh release verify-asset --help",
        ):
            self.assertLess(self.text.index(command), create)

    def test_build_attestation_is_exact_workflow_and_sha_bound(self):
        for required in (
            '--signer-workflow "$GITHUB_REPOSITORY/.github/workflows/release.yml"',
            '--signer-digest "$GITHUB_SHA"',
            '--source-ref "$GITHUB_REF"',
            '--source-digest "$GITHUB_SHA"',
        ):
            self.assertIn(required, self.text)

    def test_draft_is_verified_before_publish_and_immutable_state_uses_rest(self):
        draft = self.text.index('gh release create "$tag"')
        publish = self.text.index('gh release edit "$tag"')
        self.assertLess(draft, publish)
        self.assertIn("--draft", self.text[draft:publish])
        self.assertIn("sha256sum -c SHA256SUMS", self.text[draft:publish])
        self.assertIn("--jq '.immutable // false'", self.text[publish:])
        self.assertNotIn("--json isImmutable", self.text)

    def test_post_publish_retries_are_read_only(self):
        post = self.text[self.text.index("- name: Verify published immutable release"):]
        self.assertIn('gh release verify "$tag"', post)
        self.assertIn('gh release verify-asset "$tag"', post)
        for forbidden in ("gh release create", "gh release edit", "gh release upload", "gh api --method"):
            self.assertNotIn(forbidden, post)


if __name__ == "__main__":
    unittest.main()
