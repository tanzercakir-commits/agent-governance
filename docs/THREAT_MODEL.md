# Threat model

This document describes process and evidence failure modes. It is not a claim that this project is a complete application-security framework.

## Assets

The design tries to protect:

- the historical baseline plan and accepted roadmap evolution;
- FIFO task ordering;
- the distinction between pending and completed work;
- the integrity and provenance of completion evidence;
- protected-branch policy;
- the separation between implementer, verifier and trusted finalizer roles.

## Failure/adversary model

Assume an implementation agent may accidentally or strategically:

- declare a task done without fresh tests;
- modify acceptance criteria to fit its implementation;
- edit TODO/PROGRESS directly;
- reuse green CI from another SHA;
- reuse a verifier PASS after the head or canonical PR-body content changed;
- spoof a status name from an untrusted producer;
- skip a blocked queue-front task;
- insert newly discovered work ahead of authorized work;
- run untrusted PR code with a write-capable token;
- exploit ambiguous failure/retry behavior to cause a second ledger mutation.

## Primary mitigations

| Failure mode | Primary control |
|---|---|
| Rewrite history | Immutable `PLAN.md`; immutable accepted amendments |
| Scope grows silently | Canonical queue additions / plan amendments |
| Skip task | FIFO front-only TODO policy |
| Self-approval | Distinct implementer/verifier identities |
| Stale verifier evidence | Exact head + full canonical PR-body digest binding |
| Stale CI | Exact top-level workflow head SHA |
| Fake green status | Creator/integration/URL/description provenance checks |
| Human/agent edits completion ledgers | Trusted finalizer reconstructs deterministic transition |
| PR code gets write token | Trusted workflows execute governance code from protected default branch |
| Retry duplicates completion | Protected create-only attempt admission + sole-parent transition + no replay |
| Later green hides terminal failure | Complete immutable attempt history + exact admitted producer |
| Hidden priority bypass | Additive amendments append to back only |

## Operational failure model

Integrity failures can also originate in ordinary implementation and verification
mistakes. The [operational failure model](FAILURE_MODES.md) covers wrong working
context, incorrect provider assumptions, faulty verification expectations,
incomplete fix coverage, ineffective repetition, unnecessary dependencies and
insufficient diagnostics or publication hygiene.

These scenarios threaten the usefulness of evidence, reliable progress and the
confidentiality of private working data. Some exercise security boundaries already
listed above; others are reliability failures without an adversary. The receiving
AGENTS/MASTER_PROMPT templates require compact incident notes, verified premises
before another attempt, affected-boundary coverage and scoped verification.
Those process requirements supplement the existing gates; they neither implement
new runtime enforcement here nor establish a measured reduction in recurrence.

## Contract precision

`project_amendment` distinguishes pending queues from exact terminal regions and rejects malformed/mixed input. The same projection is used by the finalizer and all amendment validators. Sentinel mentions in the header are not terminal state. A structural self-check is not evidence of accepted completion.

The PR digest intentionally treats EOL styles and extra final LF characters as equivalent. It does not detect raw-byte changes in that equivalence class or an edit followed by restoration of the same canonical content. It must still bind all substantive fields, spaces/tabs, internal blank lines and order. No broader normalization is allowed.

Pre-publication rejection and post-publication failure have different guarantees. A published PR candidate can survive a later error without becoming accepted completion. Ambiguous publication/dispatch/status responses are UNKNOWN observations: no second ledger mutation, no rollback to disguise failure, and no call after the final-dispatch/final-success attempt. A separate read-only audit reconciles reality. Neither finalizer changes the default branch.

These clarifications address source-level inconsistencies; live GitHub authorization, concurrency and failure behavior remain to be commissioned. See [validation status](VALIDATION.md).

Review 003 adds a protected tag namespace for immutable publication/validation
claims and decisions. Lost failure records cannot erase an existing claim;
reruns, alternate candidate identities and newer statuses cannot claim it again.
Rejected duplicates make no status or history mutation. The tag ruleset must
deny updates/deletion with no bypass, and the adapter authenticates the correct
workflow role, trusted code revision, run and attempt for every record. Missing,
untrusted, malformed or incompletely read history blocks completion.

The REST ref update's `force=false` checks fast-forward ancestry, not an atomic
expected-old-SHA condition. Finalizers recheck and observe exact branch state;
they never retry the one admitted publication. PR branch writers can still
move their branch or squat an immutable attempt slot and deny service. Candidate
objects remain reachable through immutable attempt refs, and every success
consumer rejects a changed/missing PR head. These controls constrain trusted
finalizer behavior; they do not make arbitrary PR refs immutable. Live ruleset
and producer verification remains mandatory; the local model cannot prove it.

Generic Actions bot signatures and caller-controlled status descriptions do
not prove a workflow/run identity. The contract therefore requires a dedicated
App credential isolated to reviewed default-branch jobs, domain-separated RSA
signatures over the complete record schema, and an App-bound final required
status. The public key, environment branch restriction, pinned token action and
credential access paths join the trusted computing base. The model's `trusted`
boolean denotes the authenticated adapter's result; it is not a wire field.
Key/App compromise or a malicious trusted default-branch workflow is outside
this protection, as is malicious owner administration. Runtime signature,
credential-isolation and protected-merge negative tests remain release gates.

## Out of scope / residual risk

The system does not by itself protect against:

- a malicious repository owner who can change GitHub settings and policy;
- compromise of GitHub, the trusted GitHub App/integration, runner infrastructure or owner credentials;
- incorrect project-specific tests or acceptance criteria;
- two independent agents that are actually backed by the same hidden failure mode;
- logic bugs in the governance implementation itself;
- supply-chain compromise of tools the project deliberately trusts;
- social engineering outside the repository boundary.

For that reason, live commissioning, independent review, pinned dependencies/actions, adversarial unit tests and narrow privileges remain necessary.

GitHub hides ruleset bypass actors from minimal runtime credentials. A protected
owner attestation can establish the initial full configuration, while runtime
readers compare visible fields and provider update timestamps. This relies on
commissioned provider behavior for every hidden-field edit and restoration; it
does not provide direct live visibility of those actors. Missing or unreliable
change metadata blocks commissioning. The owner-side administrative credential
never enters runtime jobs. Any protection drift invalidates affected history,
including after settings are restored; automatic re-attestation is forbidden.

## Security principle

The goal is not “trust the agent less” as a slogan. The goal is to reduce how much correctness depends on any participant remembering to behave perfectly.
