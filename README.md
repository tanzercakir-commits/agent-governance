# agent-governance

**A guide for keeping AI-assisted projects organized, with checks that match the risk.**

Projects often outlive a single agent session. agent-governance helps a coding
agent leave a clear record of the plan, the next task, decisions and completed
work. It also defines what needs to be checked before a change is accepted.

Small, reversible changes use the project's normal tests and review process.
Changes with greater consequences receive more scrutiny.

Created by [Tanzer](https://github.com/tanzercakir-commits) · [MIT license](LICENSE)

## Versions

- **Latest published release: [v0.1.1](https://github.com/tanzercakir-commits/agent-governance/releases/tag/v0.1.1).** It contains the original protocol, now called STRICT, and guidance for avoiding recurring agent mistakes.
- **Current development version: [0.2.0-dev](VERSION).** The `main` branch adds PRACTICAL and REVIEWED alongside STRICT. **v0.2 has not been released.**

This README describes `main`. Use its guide or Skill for the three profiles below.
For a published snapshot, use the source or standalone Skill ZIP from v0.1.1
and verify the download against that release's `SHA256SUMS`.

## What it helps with

- **Continuity:** keep the plan, task queue, progress and decisions in the repository so another session can pick up the work.
- **Clear completion:** agree on what “done” means and check it with the project's actual tests and CI.
- **Appropriate review:** add an independent reviewer when the consequences justify it.
- **Bounded scope:** put useful, unrelated improvements in the backlog instead of expanding the task being finished.

## Three levels of checking

| Profile | Typical work | What completion requires |
|---|---|---|
| **PRACTICAL** — the default | Features, fixes and refactors with limited, reversible impact | Focused tests, project CI and the normal review/merge process |
| **REVIEWED** | Changes to shared interfaces or data models with material compatibility or correctness risk | PRACTICAL checks plus a fresh, independent review of the exact change |
| **STRICT** | Governance rules, security, access control, release signing or destructive migrations | The full protocol: independent review, checks tied to the exact commit, authenticated records and controlled acceptance |

Existing stricter project rules always apply. STRICT blocks completion when
required evidence is missing or invalid; its guarantees require the complete
controls to be implemented and tested in the receiving repository.

In PRACTICAL, the owner can change priorities, defer or cancel work with a
recorded reason. An agent cannot silently skip tasks or rewrite their history.
Related small tasks can share a bounded PR when each keeps its own completion
checks and the owner has not required separate PRs.

A review should block work that misses agreed requirements, fails a required
check, introduces material risk within the change, or lacks required evidence.
Other improvements go into the backlog.

## How it fits with other agent tools

There is overlap: planning, tests and independent review are also part of other
engineering skill packs. Their published descriptions emphasize different work:

| Tools | Main focus |
|---|---|
| [Superpowers](https://github.com/obra/superpowers), [Matt Pocock's skills](https://github.com/mattpocock/skills), [Addy Osmani's skills](https://github.com/addyosmani/agent-skills) | Requirements, planning, implementation, testing and review workflows |
| [Karpathy-inspired skills](https://github.com/multica-ai/andrej-karpathy-skills), [Ponytail](https://github.com/DietrichGebert/ponytail) | Clear assumptions, focused changes and avoiding unnecessary code |
| [Anthropic Skills](https://github.com/anthropics/skills), [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Specialized tasks such as document creation and interface design |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Exploring relationships across code and documents through a knowledge graph |

**Our strongest fit is a project that needs a durable record of what was agreed,
what was completed and which evidence justified accepting it.** STRICT spells
out how that evidence binds to the reviewed commit and scope, and how failed
attempts remain part of the record. Those controls require project-specific setup.
Other skills can complement this after their rules are reconciled. This is a
design focus, not a measured claim of better speed, cost or code quality.
See the [comparison and sources](docs/COMPARISON.md) for more detail.

## Get started

1. Open your target project and have its goal and real build/test command ready.
2. Give your coding agent the [single-file guide](UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md).
3. Ask it to prepare the project using this prompt:

```text
Read UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md in full and inspect this project.
Choose the lightest profile that fits the risk: PRACTICAL by default,
REVIEWED for material engineering risk, and STRICT for high-assurance work.
Preserve existing work and stricter project rules. Use our real tests and CI.
Keep unrelated improvements in the backlog.
Prepare changes on a separate branch and show the results before any
protected merge or settings change.
```

PRACTICAL reuses the project's existing CI and adds only missing planning and
tracking records. STRICT also prepares dedicated governance workflows and
protections; installing those controls requires explicit owner authorization.

**Using an Agent Skill:** copy the whole
[`skills/project-governance-bootstrap/`](skills/project-governance-bootstrap/SKILL.md)
folder into your agent's supported skills directory, including `references/`
and `LICENSE`. Then ask the agent to use `project-governance-bootstrap`.
The single-file guide works without installing a Skill.

An independent reviewer can be another agent or a person. The protocol does not
require a second GitHub account, but existing repository review rules still apply.

## What is included, and what is verified

This repository includes the guide, the portable Skill, executable STRICT
reference contracts, tests and packaging scripts. Copying the guide does not
install an enforcement service: each project must supply its own tests and put
the selected controls into practice.

Repository checks cover the reference code, generated guide consistency and
package contents. They do not establish live enforcement in another project.
Improvements in delivery speed, cost or safety from the new profiles have not
been measured.

The old `agent-governance-lab` and `agent-governance-adoption-lab` GitHub
repositories were deleted. The project does not depend on them to build, test
or package, but their historical live-test records are no longer accessible.
The [validation record](docs/VALIDATION.md) explains what remains verifiable.

## Check or package this repository

Use Python 3.10 or later. These checks need only the standard library:

```bash
python3 scripts/build_guide.py --check
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 scripts/check_mutations.py
python3 scripts/package_release.py --output dist
```

Packaging produces source and standalone Skill ZIPs with SHA-256 checksums in
`dist/`. It prepares local artifacts; publishing a release is a separate step.

## More detail

- [Full guide](UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md) — setup, workflows and the complete STRICT protocol
- [Design](docs/DESIGN.md) and [design choices](docs/COMPARISON.md) — how the approach fits together
- [Threat model](docs/THREAT_MODEL.md) — security assumptions and limits
- [Common failure modes](docs/FAILURE_MODES.md) — recurring mistakes and preventive practices
- [Validation record](docs/VALIDATION.md) and [historical v0.1 checklist](RELEASE_CHECKLIST.md) — checks and evidence availability
- [Contributing](CONTRIBUTING.md) — how to propose and validate changes
