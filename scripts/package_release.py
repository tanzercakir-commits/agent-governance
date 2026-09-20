#!/usr/bin/env python3
"""Build deterministic candidate archives without Git/private review history."""
import argparse
import hashlib
from pathlib import Path
import re
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
# Explicit public surface: adding a private work brief cannot silently ship it.
PUBLIC_FILES = (
    "README.md", "LICENSE", "VERSION", ".gitignore", "CONTRIBUTING.md",
    "RELEASE_CHECKLIST.md", "UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md",
    ".github/workflows/validate.yml", "docs/DESIGN.md", "docs/THREAT_MODEL.md",
    "docs/COMPARISON.md", "docs/SOURCES.md", "docs/VALIDATION.md",
    "spec/README.md", "plans/amendments/README.md",
    "examples/plan-amendments/PA-0001.md",
    "tests/fixtures/app-token-input-contract.json",
)
PUBLIC_PATTERNS = ("spec/parts/*.md", "spec/reference/*.py", "scripts/*.py", "tests/*.py",
                   "skills/project-governance-bootstrap/SKILL.md",
                   "skills/project-governance-bootstrap/LICENSE",
                   "skills/project-governance-bootstrap/references/*.md")
SKILL = "skills/project-governance-bootstrap/"


def public_files(root=ROOT):
    names = set(PUBLIC_FILES)
    for pattern in PUBLIC_PATTERNS:
        names.update(str(path.relative_to(root)) for path in root.glob(pattern))
    for name in names:
        path = root / name
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"missing or nonregular public file: {name}")
    return sorted(names)


def write_zip(path, entries):
    with ZipFile(path, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(entries.items()):
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, content)


def verify_skill(directory, guide, license_bytes):
    skill = directory / "project-governance-bootstrap"
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\nname: project-governance-bootstrap\n"):
        raise ValueError("invalid standalone skill frontmatter")
    if (skill / "references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md").read_bytes() != guide:
        raise ValueError("standalone guide mismatch")
    if (skill / "LICENSE").read_bytes() != license_bytes:
        raise ValueError("standalone license mismatch")
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if "://" not in target and not (skill / target).is_file():
            raise ValueError(f"broken standalone reference: {target}")


def build(output, root=ROOT):
    # Import through the script directory so this also works after ZIP extraction.
    sys.path.insert(0, str(root / "scripts"))
    from build_guide import render_guide
    guide = render_guide(root)
    if (root / "UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md").read_bytes() != guide:
        raise ValueError("regenerate the root guide before packaging")
    license_bytes = (root / "LICENSE").read_bytes()
    verify_skill(root / "skills", guide, license_bytes)
    version = (root / "VERSION").read_text(encoding="ascii").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9.]+)?", version):
        raise ValueError("invalid version")
    output.mkdir(parents=True, exist_ok=True)
    prefix = f"agent-governance-{version}"
    source = output / f"{prefix}.zip"
    skill = output / f"project-governance-bootstrap-{version}.zip"
    names = public_files(root)
    write_zip(source, {f"{prefix}/{name}": (root / name).read_bytes() for name in names})
    write_zip(skill, {name.removeprefix("skills/"): (root / name).read_bytes()
                      for name in names if name.startswith(SKILL)})
    with tempfile.TemporaryDirectory(prefix="agent-governance-package-") as temporary:
        unpacked = Path(temporary)
        for path in (source, skill):
            with ZipFile(path) as archive:
                if archive.testzip() is not None:
                    raise ValueError("archive integrity failure")
                archive.extractall(unpacked)
        verify_skill(unpacked, guide, license_bytes)
        exported = unpacked / prefix
        if render_guide(exported) != guide:
            raise ValueError("exported sources do not reproduce the guide")
        for name in names:
            if (exported / name).read_bytes() != (root / name).read_bytes():
                raise ValueError(f"export differs: {name}")
    manifest = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
                       for path in (source, skill))
    (output / "SHA256SUMS").write_text(manifest, encoding="ascii")
    return source, skill


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    for path in build(args.output):
        print(f"candidate package: {path}")
    print("archive extraction, source reproduction and standalone skill: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
