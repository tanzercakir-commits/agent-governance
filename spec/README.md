# Specification source

The maintainable source of the universal governance guide lives in `spec/parts/`.

The numbered files are concatenated in lexical order, and their two explicit
reference markers expand the tested Python contracts from `spec/reference/`:

```bash
python3 scripts/build_guide.py
```

That command generates two byte-identical distributable copies:

- `UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md`
- `skills/project-governance-bootstrap/references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md`

Use `python3 scripts/build_guide.py --check` in CI or review to prove that both generated copies match the canonical parts. Do not hand-edit either generated copy.

`projection.py` defines normative byte framing. `attempts.py` is an executable
protocol model over a trusted create-only store; it is not an installed GitHub
adapter. Both are embedded in the single-file distribution. Run
`python3 -m unittest discover -s tests -v` after changing either contract.

The split source exists only for maintainability. Users of the project should normally consume the single root guide or the bundled Agent Skill.
