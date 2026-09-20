# Operational failure model

Repository acceptance controls protect the meaning of completion. Work can also
fail before reaching those controls: an agent can inspect the wrong checkout,
misread an API, repeat an ineffective command, or write a verifier that shares
the implementation's mistaken assumption. These failures can waste work or
hide a real defect even when no participant intends to bypass policy.

This model generalizes observations from commissioning, including implementer,
verifier and tool-use mistakes. The underlying working records are private and
are not a benchmark: counts of incidents do not establish failure rates, time
or token costs, provider intent, or the effectiveness of the measures below.
Some observations exposed missing implementations of existing security controls;
others exposed operational reliability problems. They are not all new attacks.

## Failure scenarios and controls

| ID | Scenario and consequence | Required working practice | Evidence to inspect |
|---|---|---|---|
| OF-01 | A guessed path, checkout, command or identity causes work against the wrong target or an avoidable command failure. | Discover the repository root, remote identity, branch, current head and relevant files before acting. Read the actual CI adapter and command prerequisites; discover filenames before opening them. Refresh volatile facts after a context or checkout change. | A short working note points to the authoritative paths/commands and records the observed head. The verifier independently checks relevant current facts. |
| OF-02 | Provider behavior is assumed: a write is expected to be immediately visible, every token is expected to expose the same fields, or a green run is mistaken for qualifying evidence. | Check the interface at the pinned dependency revision. Observe the relevant API view with the intended credential role without exposing credentials. Distinguish acknowledged writes, delayed views, denied access and missing evidence; use only protocol-authorized bounded readback. | Actual scoped response metadata, pinned action inputs, run/head/attempt provenance and bounded observation results. A missing field or ambiguous response must not be silently treated as success or absence. |
| OF-03 | A verifier or test invents an output format or shares the implementation's incorrect expectation, producing false rejection or false confidence. | Derive expectations from the authoritative contract and actual interface. Exercise representative valid and invalid cases. When a control rejects valid behavior, determine which premise is wrong before changing product code or acceptance criteria. | Literal expected cases and independently inspected output. A test count must exclude duplicate discovery; changed commands must have their affected fixtures updated. |
| OF-04 | A correction covers one entry point but misses another with the same defect, leaving a security or correctness gap. | List related callers, workflows, privileged entry points and consumers before closing a finding. Mark each as affected or unaffected with a reason; repair the authorized affected scope and add meaningful regression coverage for distinct boundaries. | A compact coverage list plus behavioral evidence for the affected boundaries. For example, a module-shadowing repair must consider inline scripts and test runners as well as CLI wrappers. |
| OF-05 | An unchanged action is repeated without a new premise, or two agents replay the same expensive audit without a reason. | Before another attempt, identify the newly verified fact or concrete correction and check whether repetition is allowed. Assign the final full reconciliation to one independent verifier and preserve its result. A new finding triggers a focused check unless it invalidates the wider evidence. | Incident and verification notes state what changed, which checks are affected and why a repeat is needed. No note can authorize replay of an admitted mutation or reuse of invalidated completion evidence. |
| OF-06 | Setup silently grows beyond the task or depends on an unavailable account, reviewer or permission. | Check required capabilities and actual owner constraints early. State the deliverable and unresolved dependencies. Keep unrelated discoveries on the existing queue/amendment path; continue independent authorized work while a specific action is blocked. | Existing authorization and a capability/readiness note. Do not add unnecessary account requirements or weaken a receiving repository's stricter controls to avoid a blocker. |
| OF-07 | Generic diagnostics hide the cause, a status report outlives its evidence, or public artifacts/history reveal private working data. | Preserve a concise sanitized failure record and later resolution. Distinguish preparation, execution and accepted completion. Inspect the actual exported files, reachable history, commit attribution and release metadata before publication. | Useful error codes/statuses and scoped evidence pointers; artifact hashes and public-surface inspection. Never copy credentials, personal data or private response bodies into a public incident log. |

## A small working record

Reuse an existing task note, handoff or incident record instead of creating a new
tracking service. A local ignored note is acceptable; confirm it is excluded
before recording private context. Keep only the context needed to resume:

- observed repository/root, branch/head, relevant paths and exact check commands;
- current operation, required capability/authorization, and unresolved assumptions;
- for a mistake: ID, observed failure, impact, sanitized evidence pointer, known
  cause or `unknown`, correction, related earlier incident and next permitted action;
- for a correction: affected boundaries, check results and verifier attribution.

Append a short resolution instead of erasing the earlier failure. Expected
negative tests are not incidents. An error in a verifier's helper is not by
itself evidence of a product defect. Read the relevant recent notes when resuming;
do not repeatedly load an entire historical transcript or repeat completed checks
merely to reconstruct context.

The record supports diagnosis and coordination. It cannot mark a task complete,
grant permission, replace authenticated evidence, edit a completion ledger or
change the immutable plan. Keep it outside the trusted finalizer's write set.

## Recovery example

An agent tries to read a guessed test path and receives a file-not-found error.
It first verifies the checkout and discovers the actual file list, then records
the correct path and uses that new fact. Repeating the same guessed path would
not add evidence. If a later failure is an ambiguous remote publication result,
the permitted response is the protocol's separate read-only reconciliation;
the path-recovery example does not authorize retrying that write.

For a security fix shared by three execution paths, the agent lists all three,
checks which are affected and verifies the relevant boundaries before requesting
independent acceptance. If the verifier later makes a formatting mistake in an
auxiliary report, only that check needs correction unless the mistake invalidates
the prior evidence. Head and canonical-body changes still invalidate the evidence
specified by the task lifecycle. Refresh that evidence and all required external
gates; retained notes never substitute for them. A body-only change does not itself
require another unchanged-source build when its existing exact-head evidence still
qualifies.

## Enforcement and evaluation limits

The receiving agent instructions and execution protocol contain the portable
working rules. These are process requirements, not an installed monitor: this
repository cannot observe whether an agent guessed a filename, mentally reused
an assumption or caused a scope discussion. Independent agents can also share
the same failure mode.

Where a receiving project can check an objective condition reliably, place that
check at the actual boundary: exact checkout identity in CI, validated dependency
inputs, credential-scoped readback, a regression for each distinct affected
execution path, or publication checks over the reviewed artifact and ref state.
Such checks must be implemented and commissioned in that project. A checked box
or another instruction is not proof of enforcement.

To evaluate improvement, use comparable future tasks and record both incidents
and opportunities for failure. Record recurrence links, discovery stage, impact,
and measured time/tool usage if available. Keep external behavior and unknown
causes separate from confirmed agent mistakes. Existing live acceptance proves
the earlier commissioned protocol flows, not that these new working practices
eliminate recurrence or reduce cost.

See the [threat model](THREAT_MODEL.md), [design](DESIGN.md) and
[validation limits](VALIDATION.md).
