#!/usr/bin/env python3
"""Build standalone guides, including their executable reference contracts."""
from pathlib import Path
import argparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ("projection.py", "attempts.py")


def render_guide(root=ROOT):
    parts = sorted((root / "spec/parts").glob("[0-9][0-9].md"))
    if not parts:
        raise ValueError("no spec parts found")
    content = b"".join(p.read_bytes() for p in parts)
    for name in REFERENCES:
        marker = f"<!-- include-reference: {name} -->".encode()
        if content.count(marker) != 1:
            raise ValueError(f"expected one reference include: {name}")
        source = (root / "spec/reference" / name).read_bytes()
        content = content.replace(marker, b"```python\n" + source + b"```", 1)
    if re.search(br"<!-- include-reference:", content):
        raise ValueError("unknown reference include")
    content.decode("utf-8", errors="strict")
    if b"\r" in content:
        raise ValueError("canonical sources must use LF")
    return content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render_guide()
    targets = [ROOT / "UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md",
               ROOT / "skills/project-governance-bootstrap/references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md"]
    if args.check:
        bad = [str(t.relative_to(ROOT)) for t in targets if not t.exists() or t.read_bytes() != content]
        if bad:
            print("generated guide out of date: " + ", ".join(bad), file=sys.stderr)
            return 1
        print("generated guide: PASS")
    else:
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        print("generated guide written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
