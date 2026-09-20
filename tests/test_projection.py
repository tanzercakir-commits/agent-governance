"""Literal byte vectors for the distributed reference projection."""
import unittest

from spec.reference.projection import parse_todo, project_amendment


HEADER = b"# Queue\n\nContract mentions _Queue complete._ here.\n\n<!-- governance:tasks -->\n\n"
A = "### AG-M0-001 — First\n\nOutcome:\nOne.\n".encode()
B = "### AG-M0-002 — Second\n\nOutcome:\nTwo.\n".encode()
C = "### AG-M0-003 — Third\n\nOutcome:\nThree.\n".encode()


class ProjectionTests(unittest.TestCase):
    def test_pending_one_addition(self):
        expected = ("# Queue\n\nContract mentions _Queue complete._ here.\n\n"
                    "<!-- governance:tasks -->\n\n"
                    "### AG-M0-001 — First\n\nOutcome:\nOne.\n\n"
                    "### AG-M0-002 — Second\n\nOutcome:\nTwo.\n").encode()
        self.assertEqual(project_amendment(HEADER + A, [B]), expected)

    def test_pending_multiple_additions(self):
        expected = ("# Queue\n\nContract mentions _Queue complete._ here.\n\n"
                    "<!-- governance:tasks -->\n\n"
                    "### AG-M0-001 — First\n\nOutcome:\nOne.\n\n"
                    "### AG-M0-002 — Second\n\nOutcome:\nTwo.\n\n"
                    "### AG-M0-003 — Third\n\nOutcome:\nThree.\n").encode()
        self.assertEqual(project_amendment(HEADER + A, [B, C]), expected)
        self.assertEqual(project_amendment(HEADER + A + b"\n" + B, [C]), expected)

    def test_terminal_one_and_multiple(self):
        before = HEADER + b"_Queue complete._\n"
        self.assertEqual(project_amendment(before, [B]), HEADER + B)
        expected = ("# Queue\n\nContract mentions _Queue complete._ here.\n\n"
                    "<!-- governance:tasks -->\n\n"
                    "### AG-M0-002 — Second\n\nOutcome:\nTwo.\n\n"
                    "### AG-M0-003 — Third\n\nOutcome:\nThree.\n").encode()
        self.assertEqual(project_amendment(before, [B, C]), expected)

    def test_invalid_regions(self):
        for region in (b"", b"\n", b"_Queue complete._", b"_Queue complete._\n\n",
                       b"_Queue complete._\n\n" + A, A + b"\n_Queue complete._\n",
                       A[:-1], A + b"\n", A + B, A + b"\n\n" + B,
                       b"\n" + A, A + b"\n" + A, b"junk\n" + A):
            with self.subTest(region=region), self.assertRaises(ValueError):
                project_amendment(HEADER + region, [C])

    def test_invalid_framing_and_encoding(self):
        for before in (A, HEADER + HEADER + A, (HEADER + A).replace(b"\n", b"\r\n"),
                       HEADER + A + b"\xff\n", b"\xef\xbb\xbf" + HEADER + A,
                       HEADER + A + b"\x00\n", HEADER.replace(b"-->\n\n", b"-->\n") + A):
            with self.subTest(before=before), self.assertRaises(ValueError):
                parse_todo(before)

    def test_invalid_additions(self):
        for blocks in ([], [A], [B, B], [B[:-1]], [B + b"\n"], [B + b"\n" + C],
                       [b"_Queue complete._\n"], [B.replace(b"\n", b"\r\n")]):
            with self.subTest(blocks=blocks), self.assertRaises(ValueError):
                project_amendment(HEADER + A, blocks)

    def test_preserves_unicode_spaces_and_old_prefix(self):
        old = A.replace(b"One.", "Görev:  é é \t".encode())
        result = project_amendment(HEADER + old, [B])
        self.assertTrue(result.startswith(HEADER + old))
        self.assertEqual(parse_todo(result), (HEADER, (old, B)))
