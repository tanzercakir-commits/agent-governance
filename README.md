# agent-governance

**A project preparation guide and Agent Skill for verifiable AI-assisted development.**

Give it to your coding agent before starting a project. It specifies how to turn
your plan, task queue, tests and independent reviews into repository-owned
completion rules, with evidence tied to the exact commit being accepted.

Created by [Tanzer](https://github.com/tanzercakir-commits). [MIT licensed](LICENSE).

## Start here

You can use the [single-file guide](UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md)
with a coding agent without installing anything. Give the agent the guide and
this request in your target project:

```text
Read UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md in full.
Inspect this repository and use the guide to prepare its governance.
Preserve existing work and stricter controls. Ask only for missing project inputs.
Work on a dedicated branch, run the checks and obtain independent verification.
Present the prepared changes before any protected merge or settings change.
```

Have your project's intended outcome and actual build/test command ready. The
agent prepares the project-specific files and workflows; installing branch
protections and commissioning them on GitHub are later, explicit steps.

Independent verification can come from a separate agent or a person; the protocol
does not itself require a second GitHub account. Existing review requirements in
the receiving repository must still be respected.

If your agent supports Agent Skills, copy the entire
[`skills/project-governance-bootstrap/`](skills/project-governance-bootstrap/SKILL.md)
folder into that agent's supported skills directory. Keep its `references/`
folder and `LICENSE` together. Then ask it to use `project-governance-bootstrap`
on your target repository. Skill directory discovery varies by agent; the
single-file guide remains the direct-use option.

## What it prepares

| Project artifact | Purpose |
|---|---|
| `PLAN.md` and append-only amendments | Preserve the original plan and record later scope |
| `TODO.md` and `PROGRESS.md` | Track pending work in order and verified completion |
| Agent instructions and execution protocol | Define implementation, review and owner responsibilities |
| Governance validators and CI workflows | Check exact commit, PR scope and evidence provenance |
| Protected-branch and attempt-history rules | Control acceptance and prevent failed-attempt replay |

The core distinction is between **work claimed complete** and **work whose exact
state has passed the required checks**. The guide defines that acceptance
contract; each target repository must implement and commission it.

## What makes it different

agent-governance defines **what must be true before a repository accepts work as
complete**. The plan, task order and verification evidence become explicit parts
of the project, so they can be checked across agent sessions.

| Design choice | Practical effect |
|---|---|
| Preserve the original plan; record additions separately | New discoveries can extend the roadmap without silently rewriting earlier commitments |
| Execute the front task and append new work at the back | Pending work cannot be quietly skipped or reordered |
| Separate implementation from independent verification | A completion claim needs another review tied to the exact commit and full PR body |
| Retain completion and failure evidence | A later green status cannot erase a failed attempt or replace missing evidence |

You can pair this protocol with your preferred planning, coding or design skills.
Your project supplies its acceptance criteria and tests; agent-governance specifies
how their evidence participates in the completion decision. See the
[design distinctions](docs/COMPARISON.md) for more detail.

These are the specified protocol's properties. **Live enforcement requires an
implemented and commissioned target repository.**

## Scope and current status

This is a **v0.1 specification and skill**, with executable reference
contracts and regression tests. It is not an installed governance service.
Copying the guide or skill alone does not enforce a repository's policy.

The full protocol suits projects that need durable task history and explicit
review gates. It adds setup and GitHub administration work; a small disposable
script may not need that process. Project-specific tests and acceptance criteria
remain your responsibility.

Local reference tests do not establish live GitHub enforcement. See
[validation status](docs/VALIDATION.md) and the
[release checklist](RELEASE_CHECKLIST.md) for the evidence and publication requirements.

## Read further

- [Complete specification](UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md)
- [Design and trust boundaries](docs/DESIGN.md)
- [Threat model and limitations](docs/THREAT_MODEL.md)
- [Operational failure model and recurrence controls](docs/FAILURE_MODES.md)
- [Design distinctions](docs/COMPARISON.md)
- [Example plan amendment](examples/plan-amendments/PA-0001.md)
- [Contributing](CONTRIBUTING.md)

## Check or package this repository

Python 3.10 or later is sufficient; the repository checks use the standard library.

```bash
python3 scripts/build_guide.py --check
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 scripts/check_mutations.py
python3 scripts/package_release.py --output dist
```

The packaging command creates reproducible source and standalone skill ZIPs
with SHA-256 checksums. It prepares local candidate artifacts; it does not
publish a release or change repository visibility.
