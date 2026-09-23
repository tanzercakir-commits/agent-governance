# Design

## The layer this project targets

Coding-agent systems usually focus on **agent behavior**: plan first, test first, review carefully, keep changes small. Those are valuable controls, but they are instructions to an actor that can forget, misinterpret or rationalize them.

`agent-governance` adds a second layer: **repository acceptance semantics**. The repository should be able to answer, from durable state, whether a specific change is eligible to advance.

## Risk-proportional operating profiles

The core design rule is **assurance proportional to consequence**.

- **PRACTICAL** is the default for ordinary reversible product work. Existing
  project CI, focused tests, normal protected PR review and durable project notes
  are usually enough.
- **REVIEWED** adds a fresh independent read-only review when compatibility,
  cross-module correctness or reversibility risk is material.
- **STRICT** is the existing fail-closed reference protocol for governance,
  security, authentication/authorization, release/provenance, protected-state
  mutation, destructive migration and other declared high-assurance boundaries.

The profiles are not quality rankings. They are different cost/risk contracts.
A PRACTICAL project must not claim STRICT provenance guarantees; a STRICT project
must not silently downgrade a protected boundary.

## Governance budget

A control earns its cost by reducing a concrete risk. Prefer focused deterministic
checks before broad agent review, affected checks before full re-audits, and one
final reconciliation instead of repeated full verification. If governance work
repeatedly exceeds the product change while producing no material risk reduction,
the process should be reclassified rather than normalized.

A verifier may block only failed acceptance, a relevant required gate, material
risk in changed scope, or invalid evidence required by the selected profile.
Other improvements are backlog, not recursive task expansion.

## Operational reliability

Operational reliability complements acceptance semantics. The guide also tells
implementers and verifiers to establish actual working context, record concise
incidents, diagnose before repeating an operation and check every affected
boundary of a correction. A retained working note helps prevent rediscovery; it
is not trusted completion evidence. See the [failure model](FAILURE_MODES.md)
for the scenarios, expected evidence and limits of instruction-only controls.

## Authority model

```text
Immutable intent/history
├── PLAN.md                       bootstrap baseline
├── plans/amendments/PA-*.md      append-only roadmap growth
├── INVARIANTS.md                 non-negotiable project rules
└── MASTER_PROMPT.md              execution/finalization protocol

Operational projection
├── TODO.md                       pending FIFO queue
└── PROGRESS.md                   verified completion ledger

Evidence boundary
├── exact implementation SHA
├── exact canonical final PR body digest
├── trusted workflow/check provenance
├── independent verifier identity
├── trusted finalizer commit
└── protected merge + main audit
```

## Immutable baseline, append-only evolution

A permanently mutable master plan lets later work rewrite the contract that earlier work was supposedly implementing. A permanently frozen plan makes discovery painful. The design separates the two concerns:

- `PLAN.md` records what was known and authorized at bootstrap. It is immutable.
- `PA-NNNN` files record later accepted growth. Once accepted, they are immutable too.
- `TODO.md` is the current executable projection.
- On the default branch, `PROGRESS.md` records accepted verified completion. PR-branch candidate records are not accepted project completion.

The result is event-like history without requiring a separate database. Candidate
attempt history uses protected create-only Git refs; deploying and commissioning
that adapter and tag ruleset is a separate required trust boundary.

For v0.x, amendments are additive only. That restriction is intentional: append-only scope growth is easy to reason about and validate. Reordering, cancellation and supersession are more powerful state transitions and should not be smuggled in under the word “amendment.”

The single `project_amendment` projection preserves pending bytes/order and appends, or replaces only an exact terminal task-region sentinel while preserving the header/contract. A unique task-region marker separates the prefix. Each UTF-8/LF block has one final LF; exactly one additional LF separates blocks. Finalizer, amendment-ledger policy, final validator and main audit use the same routine; self-check shares its region parser. Malformed or mixed states are rejected.

## Why FIFO

FIFO is not universally optimal project management. In STRICT v0.x it removes a
large class of agent discretion: an agent cannot silently cherry-pick the easiest
task, skip a blocked task, or promote a newly discovered item ahead of authorized
work. Exceptional priority changes belong in an explicit owner-authorized
protocol.

PRACTICAL does not need to pretend real product priorities never change. The
owner may record an ordinary defer/reprioritize/cancel decision in the project's
normal durable tooling. That flexibility deliberately does **not** claim STRICT's
immutable queue-transition guarantee.

## Why exact-head evidence

A green check on yesterday's commit is not evidence for today's commit. A verifier's PASS before a PR-body scope edit is not evidence for the edited scope. The system therefore binds completion to:

- exact implementation SHA;
- exact PR number/repository/base;
- exact canonical PR-body digest;
- trusted workflow/check producer;
- workflow run and check suite;
- independent verifier run identity.

Any change to canonical PR-body bytes invalidates its digest binding. `canonical_pr_body` converts CRLF/lone CR to LF, collapses only terminal LF characters and encodes UTF-8 with one final LF. EOL-style/extra-final-LF edits alone are equivalent; spaces, tabs, internal blank lines and Unicode are not normalized. This is not a raw-byte or edit-history attestation. Other state/evidence gates still apply.

## Why trusted finalization

The implementation agent should not be able to both claim completion and edit the ledgers that define completion. Trusted finalization runs from governance code already present on the protected default branch, reconstructs the allowed state transition, and writes only the deterministic ledger diff.

This does not make GitHub or the governance code infallible. It narrows the trusted computing base and makes the transition auditable.

## Publication is not completion

UNPUBLISHED rejection leaves PR ledgers unchanged; an unreachable commit object is not branch publication. Ref advancement creates one PUBLISHED_UNVERIFIED candidate. Later failure preserves that commit without a second mutation or accepted completion. FINALIZED requires every final gate and still needs authorized protected merge. UNKNOWN after an ambiguous response requires separate read-only reconciliation, not retry/rollback. Neither finalizer writes the default branch. Final dispatch and final-success publication remain last-call boundaries even on ambiguous responses.

See [validation status](VALIDATION.md) for the current evidence limits.

Publication and final validation each acquire a protected, create-only admission
and write one immutable READY or FAILED decision. Slots are keyed by numeric
repository ID and PR, binding the chosen source/candidate/body and authenticated
workflow run/attempt; changing any caller-supplied identity cannot allocate a
retry. Missing outcomes after admission remain blocked, including when failure
recording loses its response. Duplicate callers never emit status failures.
Every success consumer reads complete history and the admitted producer's exact
status; a newer green status cannot replace terminal failure. READY is written
before the last-call dispatch/success boundary, so reconciliation needs no later
mutating acknowledgement. The reference protocol is tested with a durable local
adapter; it is not a commissioned GitHub implementation.

Record authentication and the final merge status belong to an isolated
governance GitHub App. Its RSA public key is pinned for record verification;
its private key is available only to reviewed default-branch jobs through an
environment restricted to that exact branch. The final required status binds
to this App's integration ID, so a generic Actions token cannot satisfy it.
Run descriptions alone are not authenticated provenance. The wire schema also
binds authorization, phase, claim and audit IDs. This additional App/environment
setup is required before live commissioning, and has not been installed here.

## Bootstrap paradox

A repository cannot enforce workflows that do not yet exist on its default branch. The guide therefore treats bootstrap as a special commissioning phase: build locally, independently verify, merge under a narrow documented bootstrap exception, install the no-bypass ruleset, then prove the first ordinary task through the real path.

The bootstrap exception is temporary state, not a permanent back door.
