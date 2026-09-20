#!/usr/bin/env python3
"""Seed the two reviewed defects in disposable copies and require detection."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(root, pattern):
    return subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", pattern, "-v"],
                          cwd=root, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                          text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def main():
    cases = [
        ("terminal-failure", "attempts.py", "test_attempts.py",
         '    if other_gates_pass is not True or complete is not True:',
         '    return bool(statuses and statuses[-1].event == "SUCCESS")\n    if other_gates_pass is not True or complete is not True:',
         "test_failure_then_rerun_and_fabricated_success_stay_rejected"),
        ("amendment-separator", "projection.py", "test_projection.py",
         'before_todo + b"\\n" + rendered', 'before_todo + b"\\n\\n" + rendered',
         "test_pending_one_addition"),
    ]
    for name, file, pattern, old, new, expected_test in cases:
        baseline = run(ROOT, pattern)
        if baseline.returncode:
            raise SystemExit(baseline.stdout)
        with tempfile.TemporaryDirectory(prefix="agent-governance-mutation-") as directory:
            copy = Path(directory)
            for folder in ("spec", "tests"):
                shutil.copytree(ROOT / folder, copy / folder, ignore=shutil.ignore_patterns("__pycache__"))
            target = copy / "spec/reference" / file
            source = target.read_text(encoding="utf-8")
            if source.count(old) != 1:
                raise SystemExit(f"mutation anchor drifted: {name}")
            target.write_text(source.replace(old, new, 1), encoding="utf-8")
            result = run(copy, pattern)
            if result.returncode == 0 or f"FAIL: {expected_test}" not in result.stdout:
                raise SystemExit(f"mutation was not detected by expected regression: {name}\n{result.stdout}")
            print(f"mutation {name}: detected by {expected_test}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
