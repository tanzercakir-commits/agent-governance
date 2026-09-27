# Low-Level Contract Method

**Optional method. Non-normative by default.** This document describes how to
develop a low-level component one demonstrated boundary at a time. It does not
select a governance profile or change a repository's acceptance rules.

## Scope and activation

Governance defines what a project must preserve and what evidence permits a
change to be accepted. This method describes how an explicitly selected task is
developed. Keep these judgments separate:

- **Governance-conformance** means the change meets the receiving project's
  selected PRACTICAL, REVIEWED, or STRICT controls and any stricter local rules.
- **Method-conformance** means a task that selected `low-level-contract` followed
  the stages and recorded the applicable evidence below.

A governance-conformant task need not select any method. Selecting this method
never replaces governance checks or elevates a task to STRICT.

The owner selects `low-level-contract` for a bounded task in the project's
existing authorized task scope or decision record. A task description can name
the method and link its working evidence; a PR description alone cannot expand
an already authorized scope. In STRICT, respect the accepted plan/amendment and
queue protocol; do not edit protected records to turn the method on. The method
is inactive for every task without that explicit selection. There is no global
switch, new configuration format, or new required CI status.

**Only when `low-level-contract` is explicitly selected for a task, the stages
below are requirements for that task's method-conformance.** A repository that
does not select it has no obligation to produce method artifacts, and its CI
must not fail because they are absent. Evidence produced here can satisfy a
governance gate when that gate accepts it; the gate judges the relevant property
and provenance under its own rules, regardless of the method used to produce it.

## Loop for one implementation boundary

First map the component as a whole, then select one small externally observable
boundary to deepen. Work through the stages in order. Keep the contract and
evidence in the task's existing notes, PR, code, and tests as appropriate; this
method does not prescribe a directory or a separate file for each stage.

**Do not implement before stages 1–4 establish a reviewable contract for the
selected boundary.**

**Work one demonstrated boundary at a time; do not generalize until a second
real use justifies the shared abstraction.**

| Stage | Record or demonstrate before moving on |
| --- | --- |
| 1. Topology hypothesis | Map the component from the top down before implementing it: major types/components and their ownership, calls, state and lifetime relationships. This map is provisional. A proposed component may move, become private or disappear if no demonstrated behavior needs it. Select one concrete node or boundary to deepen next. |
| 2. Type and interface surface | For that boundary, define only the types and caller-visible interface: inputs, outputs, states, errors, ownership and lifetime. Where the language uses headers, make a header/type-surface pass without implementation bodies. Do not generalize neighboring interfaces or add speculative abstractions. |
| 3. Behavioral pseudocode | Before implementation, describe relevant operations in language-neutral pseudocode: success, failure, timeout, cleanup, state transitions, ordering and concurrency where applicable. If a path exposes a bad interface or missing invariant, revise the type/interface surface before continuing. |
| 4. Test contract | Convert the pseudocode and invariants into explicit executable test expectations before implementation. Cover every material behavioral path, including meaningful invalid/edge cases and required real-environment checks. State what cannot yet be verified. |
| 5. Implementation | Implement this boundary against the recorded contract. Do not preserve a proposed class, adapter or other abstraction merely because it appeared in the topology hypothesis; remove or reshape it if the demonstrated behavior does not need it. |
| 6. Executable verification | Run the focused tests and the project's required build/CI checks. Run extra tools, such as sanitizers, when they address an actual risk in the boundary; record what ran, its result, and what could not be verified. |
| 7. Audit | Compare the implemented behavior and executable evidence with the type surface, pseudocode and test contract. Resolve material mismatches; use an independent reviewer when the selected governance profile or project rules require one. |
| 8. Next demonstrated boundary | Record what the current work proves, what remains unproven and the next concrete pressure on the design. Generalize only when observed boundaries justify the shared contract. |

If implementation reveals a mistaken assumption, revise the affected topology,
interface, pseudocode and tests, then verify the revised behavior. A green test
result for an obsolete contract does not close the boundary.

The audit MUST distinguish observed results from expectations and identify
verification that could not run. Completion of this method does not itself
assert release readiness, independent approval, or trusted provenance; those
claims depend on the receiving project's governance controls.

## Keeping the method small

- Reuse existing task notes, tests and CI. Do not create a second approval or
  status system for this method.
- Choose evidence in proportion to the boundary: a timeout test for a timeout
  claim, a lifetime check for an ownership claim, a compatibility test for a
  caller-visible type change.
- An audit finding that changes the contract returns to the affected stage;
  unrelated improvements go to the project's normal backlog.
- The stages can repeat for another boundary within the same authorized task.
  A future task requires its own explicit selection of this method.

For a concrete walk-through of the topology, interface-only, pseudocode and
test-contract stages, see the [incremental frame decoder example](examples/frame-decoder.md).
