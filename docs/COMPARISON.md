# What distinguishes agent-governance

The project concentrates on repository acceptance: the state and evidence needed
to accept a task as complete. Its contribution is the combination of explicit
scope history, ordered task transitions and a verifiable completion protocol.
These are concrete design choices, not a claim that no other project offers
similar mechanisms.

## Scope survives changes and new sessions

The original PLAN remains an immutable baseline. Later discoveries are recorded
as additive, numbered amendments. The pending queue follows that combined roadmap;
only its front task can execute. Accepted completion records remain in PROGRESS,
newest first, so a new agent session can recover the same agreed state.

## Verification names the work it examined

Implementation and verification use distinct run identities. The verification
payload binds both the exact source commit and the complete canonical PR body.
Changing the implementation or material scope requires fresh matching evidence.
The target's own build, tests and acceptance criteria remain essential.

## Completion has a defined state transition

Trusted automation reconstructs the expected queue and progress changes from
verified evidence. A candidate record in a PR is not sufficient to certify
completion. The protocol requires the associated checks, authorized command,
trusted producer and durable attempt history to agree before acceptance.

## Failure remains part of the record

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
