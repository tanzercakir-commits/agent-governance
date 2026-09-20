#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
guide = root / "UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md"
skill_ref = root / "skills/project-governance-bootstrap/references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md"
skill = root / "skills/project-governance-bootstrap/SKILL.md"

errors = []
if not guide.exists() or not skill_ref.exists():
    errors.append("canonical guide or skill reference copy missing")
elif guide.read_bytes() != skill_ref.read_bytes():
    errors.append("root guide and skill reference copy differ")

if not skill.exists():
    errors.append("SKILL.md missing")
else:
    data = skill.read_text()
    if not data.startswith("---\n"):
        errors.append("SKILL.md missing YAML frontmatter")
    if not re.search(r"^name:\s*project-governance-bootstrap\s*$", data, re.M):
        errors.append("unexpected skill name")
    if not re.search(r"^description:\s*\S", data, re.M):
        errors.append("skill description missing")

required = [
    "README.md",
    "docs/DESIGN.md",
    "docs/THREAT_MODEL.md",
    "docs/FAILURE_MODES.md",
    "docs/COMPARISON.md",
    "plans/amendments/README.md",
    "spec/README.md",
    "RELEASE_CHECKLIST.md",
]
for rel in required:
    if not (root / rel).exists():
        errors.append(f"required file missing: {rel}")

if guide.exists():
    txt = guide.read_text()
    for phrase in [
        "immutable baseline",
        "Append-only plan amendments",
        "/project amend-plan",
        "Plan amendment: `<PA-NNNN>`",
        "PLAN_AMENDMENTS_PREFIX",
        "Rationale:\n<why this follow-up is necessary and was not already represented in the effective roadmap>",
        "reactivate a terminal queue",
        "accepted plan amendments, TODO, or PROGRESS",
    ]:
        if phrase not in txt:
            errors.append(f"guide missing required plan-evolution phrase: {phrase}")

for forbidden in [
    ".github/workflows/generate-guide.yml",
    ".github/workflows/private-bootstrap-normalize.yml",
]:
    if (root / forbidden).exists():
        errors.append(f"private bootstrap workflow must not ship: {forbidden}")

workflow_dir = root / ".github/workflows"
if workflow_dir.exists():
    for workflow in workflow_dir.glob("*.yml"):
        text = workflow.read_text()
        for match in re.finditer(r"uses:\s*actions/checkout@([^\s#]+)", text):
            if not re.fullmatch(r"[0-9a-f]{40}", match.group(1)):
                errors.append(f"{workflow.relative_to(root)} uses unpinned actions/checkout ref: {match.group(1)}")

if errors:
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
print("repository validation: PASS")
