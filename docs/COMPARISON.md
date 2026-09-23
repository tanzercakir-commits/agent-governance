# What distinguishes agent-governance

The project concentrates on repository acceptance: the state and evidence needed
to accept a task as complete. Its contribution is the combination of explicit
scope history, ordered task transitions and a verifiable completion protocol.
These are concrete design choices, not a claim that no other project offers
similar mechanisms.

## How it relates to other projects

This summary was checked against the linked projects' own documentation on
2026-09-24. It compares their stated focus, not every feature or measured outcomes.

| Project and primary source | Stated focus |
|---|---|
| [Superpowers](https://github.com/obra/superpowers#the-basic-workflow) | A development workflow covering design, plans, TDD, agent execution and code review |
| [Matt Pocock's skills](https://github.com/mattpocock/skills#reference) | Focused engineering practices including requirements interviews, specifications, tickets, TDD, handoffs and review |
| [Karpathy-inspired skills](https://github.com/multica-ai/andrej-karpathy-skills#the-solution) | A compact instruction set for explicit assumptions, simple solutions, focused edits and verifiable goals |
| [Anthropic Skills](https://github.com/anthropics/skills#skill-sets) | Skills and examples for documents, design, development and other specialized tasks |
| [Ponytail](https://github.com/DietrichGebert/ponytail#how-it-works) | Avoid unnecessary implementation by reusing existing code, standard libraries and native platform features |
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill#intelligent-design-system-generation) | Design-system generation, UI styling and UX guidance across technology stacks |
| [Addy Osmani's skills](https://github.com/addyosmani/agent-skills#all-25-skills) | Engineering workflows from requirements through delivery, including quality gates, adversarial review and security practices |
| [Graphify](https://github.com/Graphify-Labs/graphify#what-it-does) | Queryable knowledge graphs connecting code and documents, with source-derived and inferred relationships identified |

Planning, testing, review and persistent context are shared concerns; they are not
exclusive to agent-governance. Its emphasis is the project's acceptance contract:
which task may proceed, how scope changes are authorized, and what exact evidence
permits work to be recorded as complete. The STRICT protocol below makes those
relationships explicit.

This focus can be useful when a project needs traceable acceptance across many
agent sessions or sensitive changes. Specialized tools can still supply coding,
design or exploration workflows. Their instructions must be reconciled with the
selected governance profile; combined use has not been validated here.

No head-to-head evaluation establishes that agent-governance produces better
code, costs less or delivers faster than these projects. STRICT adds implementation
and operating costs, and its historical lab records are now unavailable as
described in [validation status](VALIDATION.md).

## What the STRICT profile specifies

The following contracts apply to STRICT. PRACTICAL uses ordinary CI/review and
owner-recorded queue decisions; REVIEWED adds independent review. Neither gets
STRICT's guarantees merely by using this guide.

### Scope survives changes and new sessions

The original PLAN remains an immutable baseline. Later discoveries are recorded
as additive, numbered amendments. The pending queue follows that combined roadmap;
only its front task can execute. Accepted completion records remain in PROGRESS,
newest first, so a new agent session can recover the same agreed state.

### Verification names the work it examined

Implementation and verification use distinct run identities. The verification
payload binds both the exact source commit and the complete canonical PR body.
Changing the implementation or material scope requires fresh matching evidence.
The target's own build, tests and acceptance criteria remain essential.

### Completion has a defined state transition

Trusted automation reconstructs the expected queue and progress changes from
verified evidence. A candidate record in a PR is not sufficient to certify
completion. The protocol requires the associated checks, authorized command,
trusted producer and durable attempt history to agree before acceptance.

### Failure remains part of the record

A failed or ambiguous admitted attempt cannot be repaired by rerunning the same
PR and displaying a newer green status. Preserve the candidate and its evidence;
reconcile uncertain remote outcomes read-only and use the specified fresh-candidate
recovery path when needed.

## The tradeoff is explicit

The project now makes the tradeoff an explicit profile choice. PRACTICAL keeps
ordinary development on the repository's real CI/review path; REVIEWED adds
independent review for material engineering risk; STRICT retains the full
provenance/finalization machinery.

STRICT guarantees require a target implementation, GitHub setup and live
commissioning. The source guide and Skill alone do not enforce them. Do not pay
that cost for routine work without a concrete risk premise, and do not claim
STRICT guarantees from a PRACTICAL setup. Existing planning, coding and design
skills can still guide day-to-day work. See [validation status](VALIDATION.md)
for current evidence and [sources](SOURCES.md) for platform references.
