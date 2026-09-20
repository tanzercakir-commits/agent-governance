"""Check exported public files and standalone installation, without a host app."""
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from scripts.package_release import build


class DistributionTests(unittest.TestCase):
    def test_reproducible_archives_and_private_history_exclusion(self):
        with tempfile.TemporaryDirectory() as directory:
            first = build(Path(directory) / "first")
            second = build(Path(directory) / "second")
            for left, right in zip(first, second):
                self.assertEqual(left.read_bytes(), right.read_bytes())
            with ZipFile(first[0]) as archive:
                names = archive.namelist()
                self.assertTrue(any(name.endswith("/LICENSE") for name in names))
                for name in names:
                    self.assertFalse("/.git/" in name or "PREFLIGHT" in name or "REVIEW_003" in name)
                    self.assertNotIn("__pycache__", name)
                    self.assertNotIn("..", Path(name).parts)
            with ZipFile(first[1]) as archive:
                self.assertEqual(set(archive.namelist()), {
                    "project-governance-bootstrap/SKILL.md",
                    "project-governance-bootstrap/LICENSE",
                    "project-governance-bootstrap/references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md",
                })
