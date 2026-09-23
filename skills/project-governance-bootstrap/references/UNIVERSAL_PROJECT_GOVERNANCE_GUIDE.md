# Universal Project Governance Bootstrap Guide

> **Purpose:** Give this single file to the primary coding agent before work starts in a new repository.
>
> **Outcome:** The agent must choose the lightest governance profile that preserves the project's actual risk boundary. Ordinary product development defaults to **PRACTICAL** governance; **STRICT** fail-closed governance is reserved for changes whose failure would materially threaten security, release integrity, protected state, provenance, or another explicitly declared high-assurance boundary.
>
> **Important:** This is a project-bootstrap specification. It is intentionally language-agnostic. Project build and test commands remain a required project-specific input.

---

## 1. Instructions to the receiving agent

You are the primary bootstrap agent. Do not begin product implementation until the static bootstrap gates, bootstrap merge audit, and protected-branch installation pass. The first small foundation task is the live commissioning exercise; do not begin the second task until the full acceptance checklist passes.

Your first actions are:

1. Inspect the repository without changing it.
2. Preserve all existing user work and unrelated modifications.
3. Ask the owner only for values that cannot be discovered safely.
4. Choose the operating profile before adding machinery. Default to PRACTICAL unless a STRICT trigger below is present or the owner explicitly requests high assurance.
5. Create a dedicated bootstrap branch. Never bootstrap directly on the default branch.
6. For PRACTICAL, create or adapt only the common planning/queue/decision artifacts and the repository's real CI path. For STRICT, instantiate the complete reference layout below.
7. Replace every `{{PLACEHOLDER}}` in generated repository artifacts; fail if any remain. Keep this source guide outside the target repository or exclude its exact filename from the scan.
8. Add project-specific CI commands without weakening existing tests.
9. Run the checks required by the chosen profile. A STRICT bootstrap always requires the full governance suite and a read-only independent verifier.
10. Use the repository's normal protected PR path for PRACTICAL. For STRICT, commission the live governance workflows on a draft PR.
11. Install dedicated governance App/ruleset/attempt-store controls only for STRICT, and only after their status producers exist on the default branch.
12. Do not begin ordinary product work until the chosen profile's bootstrap acceptance conditions pass.

If the repository already has governance files, reconcile them deliberately. Do not silently overwrite stricter controls.

## 1A. Risk-proportional operating profiles

Governance is a means to ship the correct product safely. It is not a second product
that every feature must continuously expand. Verification cost must be proportional
to the consequence and reversibility of the change being accepted.

### PRACTICAL — default for ordinary product development

Use PRACTICAL unless STRICT is explicitly selected or a strict trigger applies.

The minimum durable surface is:

- the real project plan or roadmap;
- an ordered TODO/work queue;
- a completion/progress record;
- an owner-visible decision/deferred-work record;
- the repository's existing branch protection, CI, tests, and ordinary PR review.

Do **not** introduce a dedicated governance App, immutable attempt refs, body-bound
verifier payloads, extra status producers, or a parallel test framework merely
because this guide can describe them.

Routine loop:

```text
inspect -> implement -> focused tests -> project CI -> review -> merge -> next task
```

Adjacent small routine tasks may be completed in one bounded branch/PR when they
touch the same area, preserve per-task acceptance evidence, and the owner has not
required one-PR-per-task isolation.

### REVIEWED — material but ordinary engineering risk

Use REVIEWED for changes with meaningful compatibility, data-model, cross-module,
or hard-to-reverse correctness risk that do not cross a STRICT boundary.

REVIEWED adds a fresh independent read-only review of the stable exact diff and
its relevant evidence. It does not automatically require the STRICT publication,
attempt-store, finalizer, or release machinery.

### STRICT — high-assurance boundary

Use the full fail-closed protocol in sections 2–19 for governance/security
controls, authentication/authorization, release publication, provenance/signing,
protected-state mutation, destructive migration, irreversible data loss risk, or
another owner-declared high-assurance boundary.

A receiving repository may classify additional surfaces as STRICT. An agent may
escalate a task to a higher tier when evidence warrants it; it must not silently
downgrade an owner/project classification or an existing stricter control.

### What may block the current task

A finding blocks the current task only when at least one of these is true:

1. a declared acceptance criterion is not met;
2. a relevant regression, build, test, or required CI gate fails;
3. the finding exposes a material correctness, security, data-loss, compatibility,
   or release risk in the changed scope;
4. the finding invalidates evidence required by the selected governance profile.

Useful improvements outside that boundary are recorded as deferred work/backlog.
They do not expand the current task merely because they were discovered during
verification.

Do not create a new benchmark suite, evidence format, governance subsystem,
framework, or refactor inside a task unless its acceptance criteria require it,
it is necessary to close a blocking defect, or the owner explicitly authorizes
that scope.

### Governance budget

Prefer the cheapest evidence that can falsify the relevant failure mode:

- deterministic focused tests before broad agent review;
- affected checks before a full suite when wider evidence remains valid;
- one final reconciliation instead of repeated full audits;
- release-grade provenance only at release/high-risk boundaries.

If governance work repeatedly costs more than the product change while finding no
material risk, reclassify the process rather than normalizing the overhead.

Sections 2–19 below are the **STRICT reference implementation** unless a section
explicitly says otherwise. PRACTICAL or REVIEWED projects must not claim STRICT's
attempt-history, provenance, or fail-closed publication guarantees unless they
actually implement and commission those controls.

---

## 2. Bootstrap variables

Resolve and record these values before creating files:

| Variable | Meaning | Example |
|---|---|---|
| `{{PROJECT_NAME}}` | Human-readable project name | `Atlas` |
| `{{TASK_PREFIX}}` | Uppercase task prefix | `ATL` |
| `{{DEFAULT_BRANCH}}` | Protected default branch | `main` |
| `{{REPOSITORY}}` | GitHub `owner/repository` | `owner/atlas` |
| `{{PROJECT_CI_COMMAND}}` | Complete project verification command | `./.governance/project-ci.sh` |
| `{{ACTIONS_CHECKOUT_SHA}}` | Reviewed full commit SHA for `actions/checkout` | A 40-character commit SHA |
| `{{TRUSTED_STATUS_INTEGRATION_ID}}` | Numeric GitHub App integration ID observed for the trusted status producer | GitHub Actions integration ID |
| `{{FINAL_STATUS_INTEGRATION_ID}}` | Dedicated governance App integration ID; must differ from generic GitHub Actions | Observed installed App ID |
| `{{ACTIONS_CREATE_APP_TOKEN_SHA}}` | Reviewed immutable revision of `actions/create-github-app-token` | A 40-character commit SHA |
| `{{GOVERNANCE_APP_BOT_LOGIN}}` | Dedicated App's observed bot login | `atlas-governance[bot]` |
| `{{PRIMARY_LANGUAGE}}` | Main implementation language | `C++`, `Python`, `Rust` |
| `{{VERSION_SOURCE}}` | Single authored version source | `pyproject.toml`, `Cargo.toml`, CMake project version |
| `{{FIRST_TASK_ID}}` | Initial FIFO-front task | `ATL-M0-001` |
| `{{SECOND_TASK_ID}}` | Next task, used to commission the pop | `ATL-M0-002` |

Mandatory validation:

```bash
rg -n '\{\{[A-Z0-9_]+\}\}' . --glob '!UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md'
```

Bootstrap is incomplete while any placeholder remains in a generated or governed file. Resolve the current immutable action SHA from the official action repository; do not replace it with a mutable tag such as `v4`. Observe the trusted producer's integration ID from live bootstrap status evidence rather than guessing it.

The dedicated governance App is an explicit prerequisite. Install it only on
the target repository with contents/statuses write; keep its private key in a
`governance-trusted` environment restricted to the **exact protected default
branch**, never merely all protected branches/tags. Store its numeric App ID as
the environment variable `GOVERNANCE_APP_ID`, and pin its RSA public key under the controlled
governance package for public record verification. Only reviewed default-branch
publisher and validator jobs may request that environment or use the App key.
The key also signs domain-separated attempt records. The runtime must deliberately
pin and test its RSA-SHA256 implementation (for example a reviewed OpenSSL helper);
the executable model does not implement cryptography. App/environment/key setup
requires explicit owner authorization and live negative commissioning before
finalization is enabled. No such installation is performed by this source guide.

Read `action.yml` at the exact reviewed token-action revision and validate every
configured input against that interface before bootstrap. These templates use
the required `app-id` and `private-key` inputs. A newer README can describe a
different interface; a full SHA pin alone does not prove input compatibility.

Angle-bracket tokens have two classes:

- Runtime instructions such as `<CURRENT-TODO-FRONT-ID>` in MASTER_PROMPT and the PR template intentionally tell contributors what to enter for each task.
- Bootstrap scaffolding in PLAN, TODO, and `policy.py` must be fully replaced before the bootstrap commit.

Run this second check and inspect every hit:

```bash
rg -n '<[^>]+>' PLAN.md TODO.md tools/governance/project_governance/policy.py
```

The initial `_No completed implementation tasks yet._` PROGRESS sentinel is valid and is atomically replaced by the first completion record. `_No post-plan decisions yet._` is a valid DECISIONS empty state. `_Queue complete._` is valid only after the final trusted transition. The placeholder `.governance/project-ci.sh` that exits with `ERROR: project CI adapter is not configured` must never reach the bootstrap PR.

---

## 3. Required repository layout

The complete layout below is the **STRICT** reference layout. A PRACTICAL project
may keep its existing repository structure and add only the common plan/queue/
progress/decision artifacts that are missing; it should not install unused
privileged workflows or credentials.

Create or adapt this structure for STRICT:

```text
.
├── AGENTS.md
├── INVARIANTS.md
├── MASTER_PROMPT.md
├── PLAN.md
├── plans/
│   └── amendments/
│       └── README.md
├── TODO.md
├── PROGRESS.md
├── DECISIONS.md
├── CONTRIBUTING.md
├── .governance/
│   └── project-ci.sh
├── .github/
│   ├── pull_request_template.md
│   └── workflows/
│       ├── build-and-test.yml
│       ├── governance-pr.yml
│       ├── queue-finalize.yml
│       ├── plan-amend-finalize.yml
│       ├── governance-final.yml
│       └── main-audit.yml
├── docs/
│   └── GOVERNANCE_AUTOMATION.md
└── tools/
    └── governance/
        ├── README.md
        ├── project_governance/
        │   ├── __init__.py
        │   ├── __main__.py
        │   ├── commands.py
        │   ├── core.py
        │   ├── github_api.py
        │   └── policy.py
        └── tests/
            ├── test_commands.py
            ├── test_core.py
            ├── test_github_api.py
            └── test_workflow_permissions.py
```

The Python governance package must use only the standard library unless the repository deliberately vendors and locks additional dependencies.

---

## 4. Normative `AGENTS.md` template

```markdown
# {{PROJECT_NAME}} Agent Instructions

These instructions apply to the entire repository.

## Required reading before work

Read in full, in this order:

1. `INVARIANTS.md`
2. `PLAN.md`
3. every accepted `plans/amendments/PA-*.md` file in numeric order
4. `MASTER_PROMPT.md`
5. the front task in `TODO.md`
6. the newest relevant records in `PROGRESS.md`
7. relevant records in `DECISIONS.md`

## Verification proportionality

- Classify work as PRACTICAL routine, REVIEWED, or STRICT before choosing the verification path.
- PRACTICAL routine work does not require a separate independent verifier unless project policy or evidence raises the risk tier.
- REVIEWED and STRICT work require a fresh read-only independent review of the stable exact change and relevant evidence.
- The primary agent owns implementation; a required verifier must not edit files, commit, push, comment, finalize, merge, or mutate external state.
- A verifier finding blocks the current task only when it violates acceptance, breaks a relevant required gate, exposes material risk in changed scope, or invalidates required evidence.
- Non-blocking improvements go to deferred work/backlog; they do not enlarge the active task.
- If a required independent agent is unavailable, perform and disclose a clearly separated second-pass audit unless the selected STRICT policy explicitly requires a distinct principal.

## Operational reliability

- Verify the repository root, remote identity, branch/head and relevant paths before acting. Read the actual CI adapter and command prerequisites; discover filenames instead of guessing them. Recheck volatile facts after a checkout or context change.
- Keep a compact working note with those facts, unresolved assumptions and links to existing evidence. Reuse an existing task note or a local ignored file; verify exclusion before storing private context. Notes never grant authorization or satisfy completion gates.
- Check external interfaces at the pinned revision and with the intended credential role. Do not assume every token exposes the same fields or that an acknowledged write is immediately visible. Use only the protocol's permitted bounded readback.
- Record each noticed mistake briefly: observed failure, impact, sanitized evidence, known cause or unknown, correction and any related earlier incident. Include verifier/helper mistakes; exclude expected negative tests. Preserve earlier entries and append resolutions. Never log credentials or private response bodies in public artifacts.
- Before repeating a failed operation, identify the newly verified fact or concrete correction and whether repetition is permitted. Stop the unchanged affected action when neither exists; continue independent authorized work. An ambiguous remote write requires the existing read-only recovery path, never an invented retry or compensating write.
- Before closing a correction that can plausibly share a root cause across callers, workflows, privileged entry points, or consumers, identify the affected boundaries and verify them together. Do not turn every local change into a repository-wide audit without a concrete propagation reason. Use actual contracts and valid/invalid cases for tests and verifier expectations.
- Plan verification by affected boundary. Avoid duplicate full audits when their evidence remains applicable; preserve attribution and perform focused checks for new findings. Follow the task lifecycle's exact-head and canonical-body invalidation rules: a new head needs its own evidence, and a substantive body change needs refreshed policy and verifier acceptance. A body-only change does not itself require rerunning an unchanged-source build whose evidence still qualifies. Efficiency never permits reuse of invalid completion evidence.
- Check actual account, reviewer and permission prerequisites early. Use existing authorization; ask only for missing authority or inputs. Do not introduce unnecessary dependencies, weaken receiving controls, or expand scope outside the queue/amendment rules.
- Before public release, inspect the reviewed artifact, reachable history, commit attribution and release/ref metadata. Report preparation, execution and accepted completion distinctly; claim only outcomes supported by retained evidence.

## Non-negotiable repository rules

- `PLAN.md` is the immutable baseline plan after bootstrap merge. Never edit, reformat, rename, or regenerate it.
- Accepted `plans/amendments/PA-*.md` files are append-only history: new files may be added only through the amendment protocol; existing files may never be edited, deleted, renamed, or replaced.
- The effective roadmap is `PLAN.md` plus accepted plan amendments in numeric order.
- `TODO.md` is a FIFO queue. Work only on its front task.
- `PROGRESS.md` uses push-front semantics. The newest verified record is first.
- Only trusted automation mutates `TODO.md` and `PROGRESS.md` after bootstrap.
- Never develop directly on `{{DEFAULT_BRANCH}}`.
- In STRICT, use one branch and pull request per queue-front task unless the owner explicitly changes scope. In PRACTICAL, adjacent routine tasks may be batched when each task's acceptance evidence remains explicit; REVIEWED/STRICT tasks are not silently folded into a routine batch.
- Never weaken requirements, invariants, tests, datasets, or evidence boundaries to make work pass.
- Never reuse CI, verifier, finalizer, status, or ledger evidence from a different PR or commit SHA.
- The implementer does not self-approve.
- Never merge or write directly to the protected/default branch without explicit owner authorization.

The complete execution and finalization protocol is normative in `MASTER_PROMPT.md`.
```

---

## 5. Normative `INVARIANTS.md` template

```markdown
# {{PROJECT_NAME}} Invariants

## Repository state

1. The default branch is protected and changed through reviewed pull requests.
2. `PLAN.md` is the immutable baseline plan after bootstrap.
3. Accepted `plans/amendments/PA-*.md` files are immutable historical records; evolution adds new amendment files and never rewrites old ones.
4. The effective roadmap is the baseline plan plus accepted amendments in numeric order.
5. `TODO.md` contains pending work only and is consumed front-first.
6. On the protected default branch, `PROGRESS.md` contains accepted work only. Independent verification is required when the selected assurance tier requires it. Under STRICT, a PR-branch ledger record is a candidate until final validation and authorized protected merge; its mere presence is not completion.
7. A task ID cannot exist in both TODO and PROGRESS.
8. A completion transition changes TODO and PROGRESS atomically.
9. Before PR-branch ref publication, a rejected completion or amendment attempt leaves that branch's governed ledgers byte-for-byte unchanged. After publication, failure preserves the one atomic candidate commit without accepting it; ambiguous publication is UNKNOWN and must not be retried. Neither finalizer mutates the default branch.
10. Only trusted automation owns post-bootstrap TODO/PROGRESS ledger mutation.

## Evidence

11. Completion evidence is bound to one exact implementation commit SHA.
12. When independent verification is required, implementation and verifier run identities are distinct.
13. Required checks come from one trusted workflow run and check suite.
14. Status evidence is producer-bound, PR-bound, SHA-bound, and result-bound.
15. Missing, skipped, cancelled, timed-out, stale, red, or inconclusive evidence is failure.
16. Chat statements are not durable repository evidence.

## Engineering

17. Public behavior is typed, versioned where applicable, bounded, and tested.
18. Size, count, allocation, parsing, serialization, and arithmetic boundaries fail safely.
19. A version has one authored source of truth: `{{VERSION_SOURCE}}`.
20. Generated artifacts are reproducible or explicitly excluded from authority.
21. Temporary-owner and lifetime boundaries are tested when the language permits unsafe references.
22. Security or correctness controls cannot be weakened without explicit owner authorization and a decision record.

## Change control

23. Under STRICT, ordinary work discovered during a task is declared in the PR's canonical queue-additions section, independently verified, owner-authorized by the finalizer comment, appended to the back of TODO, and recorded in a new immutable plan-amendment file by the same trusted finalizer transition. It is never inserted ahead of the current front.
24. Under STRICT v0.x, owner-initiated roadmap expansion uses the dedicated additive plan-amendment protocol and does not rewrite, reorder, cancel, or silently weaken existing baseline/amendment tasks. PRACTICAL projects may use ordinary owner-recorded defer/reprioritize/cancel decisions in their normal project tooling, but must not claim STRICT queue-transition guarantees for those operations.
25. Critical governance correctness/security repairs are STRICT: they require explicit owner authorization, their own branch/PR, independent verification, and a decision record.
26. STRICT finalizers never rewrite partially finalized branches. Their durable admission history is retained under protected immutable attempt refs even if another writer changes the PR ref; a missing or changed candidate ref blocks completion. Recovery uses a fresh branch and PR from current default branch and entirely fresh evidence.
27. A non-blocking discovery does not expand the active task. Record it as deferred work unless it violates current acceptance, a relevant required gate, a material changed-scope risk, or required governance evidence.
28. Governance machinery, benchmark expansion, evidence formats, and broad refactors are product scope too. Add them to the active task only when required to close a blocker or explicitly authorized by the owner.
```

---

## 6. Normative `MASTER_PROMPT.md` template

````markdown
# {{PROJECT_NAME}} Execution Protocol

> This execution/finalization protocol is the **STRICT** profile. PRACTICAL
> routine work uses the shorter product loop defined in section 1A; REVIEWED
> adds independent review without automatically inheriting STRICT publication
> machinery.

## Roles

### Owner

Defines scope, authorizes exceptional governance repairs, and controls protected-branch policy.

### Implementer

Works only on the FIFO-front task, owns the task branch, produces tests and exact-head evidence, and never self-approves.

### Independent verifier

Required for REVIEWED and STRICT work. Performs a fresh read-only audit of the exact implementation head. It cannot mutate repository or GitHub state.

### Trusted finalizer

Runs only from code already present on the protected default branch. For ordinary tasks it validates evidence, atomically pops TODO, push-fronts PROGRESS, records any verified queue additions as a new immutable plan amendment, creates the bot-owned ledger commit, and dispatches final validation. A separate trusted amendment finalizer applies owner-initiated additive amendments.

## STRICT task lifecycle

1. Confirm the front task and clean working state.
2. Create one task branch from current `{{DEFAULT_BRANCH}}`.
3. Record a unique implementer-run identity in the PR body.
4. Implement only the authorized atomic scope.
5. Run project CI, governance tests, and relevant adversarial checks.
6. Push a stable implementation head and open a draft PR.
7. Wait for exact-head CI success.
8. Finalize the PR body, including exact-head evidence and either `None.` or canonical discovered queue additions; mark it ready.
9. After every head/body/ready change, dispatch `governance-pr.yml` on `{{DEFAULT_BRANCH}}` with the exact PR number and implementation head. Wait for that default-branch run to complete successfully and verify its producer, code SHA, target SHA and status binding. An automatic PR-event green status alone is insufficient completion evidence.
10. Request independent verification of the exact implementation head **and the entire final canonical PR body**.
11. Resolve every material finding. Any head change or change to canonical PR-body bytes invalidates the verifier payload and returns the lifecycle to step 7 or 8 as applicable. Normalization-equivalent body edits do not change this digest, but edited-event policy checks must still finish.
12. Post exactly one finalizer command using the verifier's fresh body-bound payload.
13. Wait for the bot ledger commit and all final statuses.
14. Independently audit the ledger-only commit when risk warrants it.
15. Merge through protected-branch rules.
16. Verify post-merge project CI, main audit, queue front, progress record, and ruleset.

## Failure recovery and verification work

Follow the operational reliability rules in AGENTS.md for implementer and
verifier work. After an unexpected failure, preserve a small sanitized diagnostic,
read the actual affected state, and distinguish a product defect from an incorrect
command, helper expectation, external behavior or an unknown cause. Before another
attempt, state what verified premise changed and why the next action is allowed.
Changing a command's spelling alone does not make an admitted operation retryable.

Assign one independent verifier to the final full reconciliation and retain its
attributed result. A later auxiliary-check failure calls for the affected check,
unless it undermines the wider evidence. Refresh invalidated head/canonical-body
evidence according to the task lifecycle, and perform all required post-merge/external gates. Diagnostic
notes are not trusted attempt records and cannot mutate TODO/PROGRESS or the plan.
If progress needs missing authority or an unavailable capability, report that
specific blocker and continue independent authorized work; do not add an approval
loop for routine corrections already within scope.

## Pull request metadata

The PR body contains exactly one of each:

```text
Task ID: `<CURRENT-TODO-FRONT-ID>`
Implementer run: `<globally unique run identity>`
```

## Independent verifier payload

Only a PASS verifier may supply this exact six-line command:

```text
/project finalize
task: <CURRENT-TODO-FRONT-ID>
head: <40-character implementation SHA>
result: PASS
verifier-run: <globally unique verifier identity>
evidence: <concise reproducible evidence>; queue-additions: <none or comma-separated IDs in PR order>; pr-body-sha256: <64 lowercase hex>
```

The comment targets the implementation SHA, not a later merge or ledger SHA. The verifier hashes the **entire canonical final PR body** using the following `canonical_pr_body` contract. Read the API body's decoded string, convert CRLF and lone CR to LF, remove trailing LF characters only, append exactly one final LF, then encode strict UTF-8. Do not trim spaces/tabs, collapse internal blank lines, reorder content, or normalize Unicode.

```python
def canonical_pr_body(body: str) -> bytes:
    normalized = body.replace("\r\n", "\n").replace("\r", "\n")
    return (normalized.rstrip("\n") + "\n").encode("utf-8")
```

Compute SHA-256 over those bytes. The ordered queue-additions ID suffix and full-body digest must both match the current canonical body. This binds Task ID, implementer run, outcome, scope, evidence, risks, and every queue-addition field. Changes to canonical PR-body bytes invalidate the verifier payload. EOL-style changes and extra terminal LF characters alone are normalization-equivalent and do not invalidate this digest. This is canonical-content binding, not raw-byte or edit-history binding: editing and later restoring the same canonical content cannot be detected by this digest alone. Missing/non-string API bodies, malformed metadata, stale head SHA, or any other failed gate must still be rejected. Every body consumer uses this same function; no consumer may apply broader whitespace normalization.

## Completion gates

Completion requires all of the following:

- task is still TODO front;
- PR is open, ready, same-repository, and targets `{{DEFAULT_BRANCH}}`;
- branch is current with the default branch;
- ordinary implementation diff does not manually change PLAN, accepted plan amendments, TODO/PROGRESS, or protected automation;
- exact required CI checks passed on the implementation SHA;
- policy status passed with trusted producer provenance;
- verifier PASS is fresh, owner-authorized, exact-SHA, and distinct from implementer run;
- trusted finalizer creates a sole-parent bot ledger commit;
- ledger commit changes only TODO and PROGRESS, plus exactly one new `plans/amendments/PA-*.md` file when verified queue additions are present;
- any discovered tasks are appended behind every previously pending task and recorded byte-for-byte in that new amendment file in the same ledger commit;
- final policy and final-ledger statuses pass;
- complete protected attempt history identifies the sole admitted publication and validation producers, with READY decisions and no failed or ambiguous prerequisite;
- all review threads are resolved;
- protected merge succeeds without weakening the ruleset.

## Publication states and failure recovery

For both task and amendment finalization, distinguish commit-object creation from **publication**, which occurs when the PR branch ref advances to the candidate ledger commit. Creating an unreachable Git object alone does not change the branch's ledgers.

- **UNPUBLISHED:** the ref has not advanced. A rejected attempt leaves PR-branch ledger bytes unchanged. This guarantee covers this attempt's writes, not unrelated concurrent actors.
- **PUBLISHED_UNVERIFIED:** exactly one atomic candidate commit is reachable on the PR branch, but all final evidence is not yet established. A later failure preserves that commit; it must not be accepted as completion or merged. Known failure uses fresh-branch recovery, never a second ledger mutation on the failed branch.
- **FINALIZED:** fresh read-only evidence establishes every required final gate on the exact candidate head. The branch is eligible for an explicitly authorized protected merge, not automatically merged. A later post-merge audit remains mandatory.
- **UNKNOWN** is an observation state, not success: a lost publication, dispatch, or final-status response may conceal a completed remote action. Do not retry a ledger mutation, force-reset the branch, or publish compensating success. A later read-only reconciliation establishes what happened. A proven success may be recognized only with all exact-head gates; otherwise keep it blocked and recover on a fresh branch.

Neither finalizer writes the protected default branch. Candidate TODO/PROGRESS state is not the default branch's accepted project state. The no-remote-call boundaries after attempting final dispatch or final success publication still apply; reconciliation runs separately, not as a trailing call in that invocation.

Before the first ref-publication attempt, acquire the durable create-only admission defined in the governance package contract. The same PR never receives a second admission, even under a different run ID, run attempt, source SHA, body digest or candidate commit. Validation has a separate one-shot admission inside that same history. A definitive FAILED decision is terminal; a missing decision after admission is blocked, never permission to replay. Only a READY decision plus the admitted producer's exact successful evidence may be recognized by read-only reconciliation. Rejected duplicates perform no status/comment/ref mutation, so they cannot poison the legitimate attempt. GitHub Actions concurrency is an efficiency measure, not this admission boundary.

Preservation here constrains trusted finalizer writes. The default-branch ruleset alone does not protect PR branch refs from an implementer. Protected immutable attempt refs retain the selected candidate commit and its history; all success consumers recheck the current PR head. This does not prevent a branch writer from denying service by moving their PR ref.

Never manually edit a bot ledger, forge a success status, reuse stale evidence, or force-reset a partially finalized branch.

If live commissioning exposes a governance bug:

1. stop the task merge;
2. preserve the failed PR unchanged;
3. obtain explicit owner authorization for a critical governance repair;
4. fix it in a separate PR from current default branch;
5. independently verify and merge the repair through a narrowly documented procedure;
6. restore and re-read the full ruleset;
7. close the failed task PR unmerged;
8. replay only pre-finalizer implementation commits onto a fresh branch from current default branch;
9. produce entirely new CI, policy, verifier, finalizer, status, and ledger evidence.
````

---

## 7. `PLAN.md` baseline template

Write the entire roadmap that is known at bootstrap time. Use stable IDs and testable acceptance criteria. `PLAN.md` is the immutable baseline, not a claim that future discovery is impossible. Later additive scope belongs in append-only plan amendments.

```markdown
# {{PROJECT_NAME}} Baseline Plan

> Immutable after bootstrap merge. The effective roadmap is this baseline plus accepted `plans/amendments/PA-*.md` files in numeric order.

## M0 — Foundation

### {{FIRST_TASK_ID}} — <first atomic outcome>

**Outcome**

<One observable outcome.>

**Acceptance**

- <Testable criterion>
- <Testable criterion>

### {{SECOND_TASK_ID}} — <second atomic outcome>

**Outcome**

<One observable outcome.>

**Acceptance**

- <Testable criterion>

## Later milestones

<Continue with stable task IDs.>
```

After PLAN content is final but **before** the bootstrap commit and PR, compute and pin its exact blob hash in `tools/governance/project_governance/policy.py`:

```bash
git hash-object PLAN.md
```

The bootstrap commit must already contain the real hash. The baseline PLAN and the pinned constant then freeze together; pinning is never a post-bootstrap edit. Roadmap evolution happens through new amendment files, never by changing this hash.

---
> **Profile note:** Sections 7A–13 are part of the STRICT reference implementation unless stated otherwise. PRACTICAL projects may use ordinary owner-recorded roadmap and queue decisions with their existing CI/PR process, but must not claim the exact projection/provenance guarantees below.


## 7A. Append-only plan amendments

Plan immutability protects historical intent, but it must not make legitimate future discovery impossible. Use an append-only event model:

```text
Effective roadmap = PLAN.md + PA-0001.md + PA-0002.md + ...
```

Create `plans/amendments/README.md` explaining that accepted amendment files are immutable. Amendment IDs are monotonically increasing and gap-free at acceptance time: `PA-0001`, `PA-0002`, and so on. Version 0.x amendments are deliberately **additive only**. They may introduce new task IDs and append those tasks to the back of TODO; they may not rewrite, reorder, cancel, or weaken existing work. A later governance version may add destructive/superseding operations only with a separately specified and tested protocol.

Canonical amendment file:

```markdown
# PA-0001 — <short roadmap extension title>

Status: accepted
Source: <owner-initiated | discovered-during TASK-ID>
Pull request: #<number>
Implementation/source SHA: `<40-char SHA or none for owner-initiated proposal>`

## Rationale

<Why this work was not part of the bootstrap baseline and why it is now necessary.>

## Added tasks

### <NEW-TASK-ID> — <title>

Milestone: <milestone>

Outcome:
<one observable outcome>

Acceptance:
- <testable criterion>

Evidence:
- <exact finding, requirement, issue, test, or owner decision>
```

Two creation paths are valid:

1. **Discovered during ordinary implementation.** The existing task PR declares canonical queue additions. After exact-head verification and owner finalizer authorization, the trusted finalizer appends the tasks to TODO and creates the next amendment file in the same bot-owned atomic ledger commit. The amendment content must be reconstructed deterministically from the verified PR body and durable evidence. The generated amendment's `## Rationale` section is rendered deterministically as ordered `<TASK-ID>: <Rationale>` entries copied from those verified queue-addition blocks.
2. **Owner-initiated roadmap extension.** A dedicated plan-amendment PR adds exactly one next-sequence `PA-*.md` proposal and no TODO/PROGRESS edits. Dispatch the policy workflow from `{{DEFAULT_BRANCH}}` against its exact proposal head, as required by the task lifecycle. After exact-head CI, trusted default-branch policy success and independent verification, the owner posts the canonical `/project amend-plan` command. Trusted automation appends the amendment's task blocks to the back of TODO in one bot commit and validates that projection before merge.

A dedicated owner-initiated amendment PR body contains exactly one of each:

```text
Plan amendment: `<PA-NNNN>`
Implementer run: `<globally unique proposer/implementer identity>`
```

Canonical verifier payload for owner-initiated amendments:

```text
/project amend-plan
amendment: <PA-NNNN>
head: <40-character amendment proposal SHA>
result: PASS
verifier-run: <globally unique verifier identity>
evidence: <concise reproducible evidence>; pr-body-sha256: <64 lowercase hex>
```

The amendment finalizer must require: the next amendment ID; a single newly added amendment file; no modification/deletion/rename of prior amendments; unique never-used task IDs across baseline PLAN, all amendments, TODO, and PROGRESS; non-empty rationale/outcome/acceptance/evidence; exact-head CI and policy provenance; a ready same-repository PR current with the default branch; owner/member authorization; verifier/implementer identity separation; and a canonical_pr_body digest match. It creates a sole-parent bot commit that changes only `TODO.md`, with the exact bytes returned by `project_amendment` below. Pending tasks are preserved and new blocks are appended; an exact terminal region is replaced, never retained beside the new blocks. The publication-state and failure-recovery contract in MASTER_PROMPT applies equally to amendments.

### Shared amendment projection: `project_amendment`

Implement one pure `project_amendment(before_todo, new_blocks)` routine in the trusted core. Its inputs are the immutable proposal parent's TODO and a non-empty, ordered sequence of independently verified canonical new task blocks. Validate the next amendment ID, global never-reuse task namespace and the additive-only proposal before invoking it.

Parse the TODO header/queue contract separately from its task region. Classify that region structurally, not by searching for the sentinel string anywhere in the file (the contract itself may mention it).

The exact framing is strict UTF-8 without BOM, NUL or CR. The header starts with `# `, ends with the existing header bytes followed by `\n\n`, and contains no task heading. One unique `<!-- governance:tasks -->\n\n` marker ends that header/contract prefix; no task occurs before it. The region starts immediately afterward. Each task block starts at its `### TASK-ID — title` line, has a nonempty body and ends in **exactly one LF**, never two. It contains no second task heading, standalone sentinel or reserved region marker. The target's semantic parser additionally enforces its task-ID prefix and required outcome/acceptance/evidence fields; framing acceptance alone is not semantic acceptance. Existing baseline tasks retain their baseline body format; new amendment blocks retain the canonical amendment body format above.

Between adjacent task blocks insert **one additional LF**, `b"\n"`; with the block's own final LF this gives exactly two LF bytes before the next heading. Do not strip or normalize task contents. The exact terminal region is `b"_Queue complete._\n"`, without a separator or other trailing bytes.

1. **Pending:** preserve the entire existing TODO byte sequence and task order; append the canonical separator and new blocks at the back.
2. **Terminal:** require the task region to be exactly `_Queue complete._` with its canonical final LF; preserve the header/contract bytes and replace only that region with the new blocks.
3. **Invalid:** reject missing/malformed/empty regions, sentinel-plus-task mixtures, duplicate task IDs, or non-canonical task blocks. Do not silently repair input or write any file.

The trusted amendment finalizer, trusted amendment-ledger mode in `validate-pr`, `validate-final`, and `audit-main` must all reconstruct the same bytes through `project_amendment`. `self-check` shares its region parser and pending/terminal classification; a local self-check alone does not certify provenance or completion. Reject any candidate differing from the reconstructed bytes, including changed header text, changed old task content/order, retained terminal sentinel, missing additions, or extra files. The existing exact-path/parent/bot/provenance/authorization gates are unchanged. An owner amendment changes only TODO and never records a task completion in PROGRESS.

No plan-amendment path may insert work ahead of the current TODO front. Urgent security/governance repair remains the explicit exceptional repair protocol rather than a hidden priority bypass.

The following reference is the normative framing/parser/projection algorithm. A target may port it, but every consumer must share the same implementation and pass literal golden byte vectors. In this source repository it is exercised directly by `tests/test_projection.py`; its inclusion here makes the standalone guide and Skill self-contained.

```python
"""Normative byte framing; target repositories also validate task semantics."""
import re

MARKER = b"<!-- governance:tasks -->\n\n"
TERMINAL = b"_Queue complete._\n"
TASK_HEADER = re.compile(r"### ([A-Z][A-Z0-9]*-[A-Z0-9]+-[0-9]{3}) — (\S[^\n]*)\n")


def _text(value: bytes) -> str:
    if not isinstance(value, bytes):
        raise ValueError("expected bytes")
    try:
        text = value.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ValueError("invalid UTF-8") from error
    if "\r" in text or "\x00" in text or "\ufeff" in text:
        raise ValueError("noncanonical encoding")
    return text


def task_id(block: bytes) -> str:
    text = _text(block)
    match = TASK_HEADER.match(text)
    if not match or not block.endswith(b"\n") or block.endswith(b"\n\n"):
        raise ValueError("task header or final LF")
    body = text[match.end():]
    if not body.strip("\n") or re.search(r"^### |^_Queue complete\._$", body, re.M):
        raise ValueError("empty or mixed task block")
    if "<!-- governance:tasks -->" in text:
        raise ValueError("reserved marker in task")
    return match.group(1)


def parse_todo(before: bytes) -> tuple[bytes, tuple[bytes, ...]]:
    _text(before)
    if before.count(b"<!-- governance:tasks -->") != 1 or MARKER not in before:
        raise ValueError("missing or ambiguous task region")
    header, region = before.split(MARKER)
    if not header.startswith(b"# ") or not header.endswith(b"\n\n"):
        raise ValueError("header framing")
    if re.search(br"^### ", header, re.M):
        raise ValueError("task outside region")
    prefix = header + MARKER
    if region == TERMINAL:
        return prefix, ()
    starts = [m.start() for m in re.finditer(br"^### ", region, re.M)]
    if not starts or starts[0] != 0:
        raise ValueError("invalid task region")
    blocks = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(region)
        block = region[start:end]
        if index + 1 < len(starts):
            if not block.endswith(b"\n\n"):
                raise ValueError("missing block separator")
            block = block[:-1]  # Remove exactly the separator LF, never trim.
        task_id(block)
        blocks.append(block)
    ids = [task_id(block) for block in blocks]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate task ID")
    return prefix, tuple(blocks)


def project_amendment(before_todo: bytes, new_blocks: list[bytes]) -> bytes:
    header, pending = parse_todo(before_todo)
    if not isinstance(new_blocks, (list, tuple)) or not new_blocks:
        raise ValueError("nonempty ordered additions required")
    ids = [task_id(block) for block in (*pending, *new_blocks)]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate task ID")
    rendered = b"\n".join(new_blocks)
    return before_todo + b"\n" + rendered if pending else header + rendered
```

Literal framing examples (the abbreviated bodies illustrate framing only; semantic task validation remains mandatory): with `H = b"# Queue\n\n<!-- governance:tasks -->\n\n"`, `A = "### AG-M0-001 — First\n\nOutcome:\nOne.\n".encode("utf-8")` and `B = "### AG-M0-002 — Second\n\nOutcome:\nTwo.\n".encode("utf-8")`, pending `H + A` plus `[B]` produces `H + A + b"\n" + B`. Terminal `H + b"_Queue complete._\n"` plus `[A, B]` produces those same bytes. Terminal plus `[A]` produces exactly `H + A`. Adding another LF, omitting that separator, or removing any block's final LF is an error.

---

## 8. `TODO.md` template

```markdown
# {{PROJECT_NAME}} Work Queue

> Operational semantics: FIFO, front-only execution. This file contains pending work only.

## Queue contract

- Only the first task is active.
- Completed work is removed entirely.
- New work is appended to the back only by trusted task finalization or trusted plan-amendment finalization from independently verified canonical evidence.
- A blocked task cannot be silently skipped.
- Task IDs are stable and never reused.
- Post-bootstrap TODO mutation belongs only to trusted automation; humans and implementation agents never edit it directly.
- After the final task, the TODO task region contains exactly `_Queue complete._`; this is a valid terminal state, not a parser error.
- A later owner-initiated additive amendment may reactivate a terminal queue only through trusted amendment finalization, replacing that exact sentinel with canonical new task blocks.

---

<!-- governance:tasks -->

### {{FIRST_TASK_ID}} — <first task title>

**Outcome**

<Copy exactly from PLAN.>

**Acceptance**

- <Copy exactly from PLAN.>

### {{SECOND_TASK_ID}} — <second task title>

**Outcome**

<Copy exactly from PLAN.>

**Acceptance**

- <Copy exactly from PLAN.>
```

The parser must treat the entire `### TASK-ID — title` block as the queue element, excluding the one separator LF between blocks. When finalization removes the last task and appends no discovered work, it must preserve the header and queue contract including the region marker, replace the task region with exactly `b"_Queue complete._\n"`, and report no current front. The ordinary FIFO pop and optional append use the same block framing and parser as `project_amendment`; do not leave a stale milestone/front label in the preserved header.

---

## 9. `PROGRESS.md` template

```markdown
# {{PROJECT_NAME}} Progress Ledger

> Operational semantics: push-front. The newest verified completion record is first.

## Ledger contract

- On the protected default branch, only accepted and independently verified work belongs here. A PR-branch record is a candidate and does not itself prove completed finalization; apply MASTER_PROMPT publication states.
- Existing records are immutable.
- Corrections are new records that reference the earlier record.
- Each ordinary record corresponds to exactly one task popped from TODO.
- Durable evidence identifies exact commits, PRs, checks, runs, and verifier identity.

## Records

_No completed implementation tasks yet._
```

The finalizer renders records in this canonical shape:

```markdown
### <UTC timestamp> — <task ID>: <title>

Milestone: <milestone>
Branch: `<branch>`
Pull request: #<number>
Commit: `<implementation SHA>`
Implementer: `<login>` / `<implementer run>`
Verifier: `<login>` / `<verifier run>`

Summary:
- <PR title or task outcome>

Changed artifacts:
- `<path>`

Acceptance evidence:
- Required implementation checks succeeded on `<implementation SHA>`.
- Structured verification comment #<comment ID>: <evidence>.
- Queue finalization was generated by the trusted governance workflow.

Tests and checks:
- project-tests: success
- governance-unit: success
- governance/policy: success

Known limitations / deferred work:
- See pull request #<number> body and review discussion.

Queue mutation:
- Popped: <task ID>
- Appended to back: <comma-separated task IDs or none>
- New front: <next task ID or none (queue complete)>
```

---

## 10. `DECISIONS.md` template

```markdown
# {{PROJECT_NAME}} Decision Ledger

This file records architectural decisions, justified deviations, replacements, and pivots discovered after implementation evidence exists.

## Rules

- Insert decisions newest-first.
- Never rewrite the baseline PLAN or an accepted amendment through a decision. Additive roadmap scope uses a new plan amendment.
- State context, evidence, decision, consequences, alternatives, and affected tasks.
- Invariant changes require explicit owner authorization.
- Superseded decisions remain in history.

## Decisions

_No post-plan decisions yet._
```

Canonical record:

```markdown
### ADR-0001 — <decision title>

Date: YYYY-MM-DD
Status: accepted
Supersedes: none
Related tasks/PRs: <IDs>

Context:
...

Evidence:
...

Decision:
...

Consequences:
- ...

Alternatives considered:
- ...
```

---

## 11. Pull request and contribution templates

### `.github/pull_request_template.md`

```markdown
Task ID: `<CURRENT-TODO-FRONT-ID>`

Implementer run: `<unique-run-identity>`

## Outcome

<What observable task outcome this PR implements.>

## Atomic scope

- <Included>
- <Explicitly excluded>

## Evidence

- Local project CI: pending
- Exact-head GitHub CI: pending
- Governance policy: pending
- Independent verifier: pending

## Risks and limitations

- <Known limitation or none>

Do not manually edit TODO.md or PROGRESS.md. Trusted finalization owns the completion transition.

If implementation evidence reveals necessary follow-up work, replace the final `None.` using this exact form. Each addition is appended behind all pending tasks and recorded in a new immutable plan amendment only after independent PASS and the owner's finalizer command:

#### Queue addition: `<NEW-TASK-ID>` — <title>

Milestone: <milestone>

Rationale:
<why this follow-up is necessary and was not already represented in the effective roadmap>

Outcome:
<one observable outcome>

Acceptance:
- <testable criterion>

Discovery evidence:
- <exact test, finding, issue, or artifact>

## Discovered queue additions

None.
```

### `CONTRIBUTING.md`

````markdown
# Contributing to {{PROJECT_NAME}}

1. Read AGENTS.md and its mandatory documents.
2. Work only on TODO front.
3. Branch from current `{{DEFAULT_BRANCH}}`.
4. Use one task branch and one PR.
5. Keep the PR draft until the exact implementation head and final body are ready; then mark ready, dispatch `governance-pr.yml` from `{{DEFAULT_BRANCH}}` for that exact PR/head, wait for trusted default-branch policy success, and request body-bound independent verification.
6. Never manually update the baseline PLAN, TODO, PROGRESS, or an accepted amendment. New amendment proposals use the dedicated amendment protocol.
7. Do not merge until all protected statuses and review threads pass.

Required local command:

```bash
{{PROJECT_CI_COMMAND}}
PYTHONPATH=tools/governance python3 -P -m unittest discover -s tools/governance/tests -p 'test_*.py'
PYTHONPATH=tools/governance python3 -P -m project_governance self-check --repo-root .
```
````

---

## 12. Project CI adapter

Create `.governance/project-ci.sh` and make it executable.

```bash
#!/usr/bin/env bash
set -euo pipefail

# Replace this section with the repository's authoritative clean verification.
# It must configure/build/test from repository-owned definitions.
# It must not download unpinned executable code or silently skip missing tools.

echo "ERROR: project CI adapter is not configured" >&2
exit 2
```

Bootstrap cannot pass while this placeholder adapter exits with error. Replace it with the project's real commands and verify it from a clean checkout.

---

## 13. GitHub Actions workflows

These workflows are complete structural templates. Keep the security boundary: workflows handling `pull_request_target`, comments, statuses, contents writes, or workflow dispatch must execute governance code from the protected default branch, never from the untrusted PR head.

Use Python 3.11 or later and invoke governance modules with `-P`. The workflow's
`PYTHONPATH` must contain only the protected `tools/governance` directory; it
must not contain the repository root or an empty entry. Otherwise ordinary
root-level Python files could shadow the trusted package or its imports before
any governance checks run. Keep executable entry points and imported repository
code under protected governance paths. Verify this with harmless root module
shadows in a credential-free subprocess test on the hosted runtime. The `-P`
option also applies to inline Python preparation steps in the trusted job,
since those can alter the workspace used by a later privileged step. It
removes Python's automatic working-directory insertion; it does not
sanitize an unsafe explicit `PYTHONPATH`. See the [Python command-line reference](https://docs.python.org/3/using/cmdline.html#cmdoption-P).

### `.github/workflows/build-and-test.yml`

```yaml
name: build-and-test

on:
  pull_request:
    branches: [{{DEFAULT_BRANCH}}]
  push:
    branches: [{{DEFAULT_BRANCH}}]

permissions:
  contents: read

concurrency:
  group: build-and-test-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  project-tests:
    name: project-tests
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@{{ACTIONS_CHECKOUT_SHA}}
        with:
          ref: ${{ github.event.pull_request.head.sha || github.sha }}
          persist-credentials: false
      - name: Verify exact tested checkout
        env:
          EXPECTED_SHA: ${{ github.event.pull_request.head.sha || github.sha }}
        run: test "$(git rev-parse HEAD)" = "$EXPECTED_SHA"
      - name: Run authoritative project CI
        run: ./.governance/project-ci.sh

  governance-unit:
    name: governance-unit
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@{{ACTIONS_CHECKOUT_SHA}}
        with:
          ref: ${{ github.event.pull_request.head.sha || github.sha }}
          persist-credentials: false
      - name: Verify exact tested checkout
        env:
          EXPECTED_SHA: ${{ github.event.pull_request.head.sha || github.sha }}
        run: test "$(git rev-parse HEAD)" = "$EXPECTED_SHA"
      - name: Unit tests
        env:
          PYTHONPATH: tools/governance
        run: python3 -P -m unittest discover -s tools/governance/tests -p 'test_*.py'
      - name: Repository self-check
        if: github.event_name == 'push'
        env:
          PYTHONPATH: tools/governance
        run: python3 -P -m project_governance self-check --repo-root .
```

The raw repository self-check validates a materialized queue, so this build step
runs on protected-default-branch pushes. An amendment proposal intentionally adds
its PA file before the trusted finalizer updates TODO; treating that source tree
as already applied would reject valid proposals. Every PR still requires the
trusted `governance/policy` status: task mode validates the source queue, and
amendment mode validates the proposal against the current base and self-checks
the shared projected result. Unit tests and authoritative project CI run on every
PR. Bootstrap additionally requires local and independent baseline self-check
before merge. This separation does not authorize a PR to edit ledgers or skip
policy, source-check, finalizer or post-merge audit gates.

### `.github/workflows/governance-pr.yml`

```yaml
name: governance-policy

on:
  pull_request_target:
    branches: [{{DEFAULT_BRANCH}}]
    types: [opened, reopened, synchronize, edited, ready_for_review]
  workflow_dispatch:
    inputs:
      pr_number:
> **Profile note:** The workflow and governance-package contracts in this part implement STRICT. They are not mandatory plumbing for PRACTICAL routine development.

        description: Pull request number
        required: true
        type: string
      head_sha:
        description: Exact pull-request head SHA
        required: true
        type: string

permissions:
  actions: read
  checks: read
  contents: read
  pull-requests: read
  statuses: write

concurrency:
  group: governance-policy-${{ inputs.pr_number || github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  policy:
    name: policy
    if: github.ref == format('refs/heads/{0}', github.event.repository.default_branch)
    runs-on: ubuntu-latest
    steps:
      - name: Check out trusted governance code
        uses: actions/checkout@{{ACTIONS_CHECKOUT_SHA}}
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - name: Validate queue-front and protected-file policy
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PYTHONPATH: tools/governance
          REPOSITORY: ${{ github.repository }}
          PR_NUMBER: ${{ inputs.pr_number || github.event.pull_request.number }}
          HEAD_SHA: ${{ inputs.head_sha || github.event.pull_request.head.sha }}
        run: >-
          python3 -P -m project_governance validate-pr
          --repository "$REPOSITORY"
          --pr-number "$PR_NUMBER"
          --head-sha "$HEAD_SHA"
```

### `.github/workflows/queue-finalize.yml`

```yaml
name: queue-finalize

on:
  issue_comment:
    types: [created]

permissions:
  actions: write
  checks: read
  contents: write
  issues: write
  pull-requests: write
  statuses: write

concurrency:
  group: queue-finalize-${{ github.event.issue.number }}
  cancel-in-progress: false

jobs:
  finalize:
    name: finalize
    if: >-
      github.event.issue.pull_request &&
      startsWith(github.event.comment.body, '/project finalize')
    runs-on: ubuntu-latest
    environment: governance-trusted
    steps:
      - name: Acquire isolated governance credential
        id: governance-token
        uses: actions/create-github-app-token@{{ACTIONS_CREATE_APP_TOKEN_SHA}}
        with:
          app-id: ${{ vars.GOVERNANCE_APP_ID }}
          private-key: ${{ secrets.GOVERNANCE_APP_PRIVATE_KEY }}
          permission-contents: write
          permission-statuses: write
          skip-token-revoke: true
      - name: Check out trusted finalizer
        uses: actions/checkout@{{ACTIONS_CHECKOUT_SHA}}
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - name: Validate evidence and atomically finalize queue ledgers
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GOVERNANCE_TOKEN: ${{ steps.governance-token.outputs.token }}
          GOVERNANCE_APP_PRIVATE_KEY: ${{ secrets.GOVERNANCE_APP_PRIVATE_KEY }}
          PYTHONPATH: tools/governance
        run: >-
          python3 -P -m project_governance finalize
          --event-path "$GITHUB_EVENT_PATH"
```

### `.github/workflows/plan-amend-finalize.yml`

```yaml
name: plan-amend-finalize

on:
  issue_comment:
    types: [created]

permissions:
  actions: write
  checks: read
  contents: write
  issues: write
  pull-requests: write
  statuses: write

concurrency:
  group: plan-amend-finalize-${{ github.event.issue.number }}
  cancel-in-progress: false

jobs:
  finalize-amendment:
    name: finalize-amendment
    if: >-
      github.event.issue.pull_request &&
      startsWith(github.event.comment.body, '/project amend-plan')
    runs-on: ubuntu-latest
    environment: governance-trusted
    steps:
      - name: Acquire isolated governance credential
        id: governance-token
        uses: actions/create-github-app-token@{{ACTIONS_CREATE_APP_TOKEN_SHA}}
        with:
          app-id: ${{ vars.GOVERNANCE_APP_ID }}
          private-key: ${{ secrets.GOVERNANCE_APP_PRIVATE_KEY }}
          permission-contents: write
          permission-statuses: write
          skip-token-revoke: true
      - name: Check out trusted amendment finalizer
        uses: actions/checkout@{{ACTIONS_CHECKOUT_SHA}}
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - name: Validate amendment evidence and append TODO projection
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GOVERNANCE_TOKEN: ${{ steps.governance-token.outputs.token }}
          GOVERNANCE_APP_PRIVATE_KEY: ${{ secrets.GOVERNANCE_APP_PRIVATE_KEY }}
          PYTHONPATH: tools/governance
        run: >-
          python3 -P -m project_governance finalize-amendment
          --event-path "$GITHUB_EVENT_PATH"
```

### `.github/workflows/governance-final.yml`

```yaml
name: governance-final

on:
  workflow_dispatch:
    inputs:
      pr_number:
        description: Pull request number
        required: true
        type: string
      head_sha:
        description: Exact finalizer commit SHA
        required: true
        type: string

permissions:
  actions: read
  checks: read
  contents: write
  issues: write
  pull-requests: write
  statuses: write

concurrency:
  group: governance-final-${{ inputs.pr_number }}
  cancel-in-progress: false

jobs:
  queue-finalized:
    name: queue-finalized
    runs-on: ubuntu-latest
    environment: governance-trusted
    steps:
      - name: Acquire isolated governance credential
        id: governance-token
        uses: actions/create-github-app-token@{{ACTIONS_CREATE_APP_TOKEN_SHA}}
        with:
          app-id: ${{ vars.GOVERNANCE_APP_ID }}
          private-key: ${{ secrets.GOVERNANCE_APP_PRIVATE_KEY }}
          permission-contents: write
          permission-statuses: write
          skip-token-revoke: true
      - name: Check out trusted validator
        uses: actions/checkout@{{ACTIONS_CHECKOUT_SHA}}
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - name: Validate bot commit and ledger transition
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GOVERNANCE_TOKEN: ${{ steps.governance-token.outputs.token }}
          GOVERNANCE_APP_PRIVATE_KEY: ${{ secrets.GOVERNANCE_APP_PRIVATE_KEY }}
          PYTHONPATH: tools/governance
          REPOSITORY: ${{ github.repository }}
          PR_NUMBER: ${{ inputs.pr_number }}
          HEAD_SHA: ${{ inputs.head_sha }}
        run: >-
          python3 -P -m project_governance validate-final
          --repository "$REPOSITORY"
          --pr-number "$PR_NUMBER"
          --head-sha "$HEAD_SHA"
```

The credential action is pinned and scoped to the current repository. Disable its
post-job token revocation to preserve the no-remote-call boundary; rely on the
short-lived installation token's expiry, never persist it, and expose it only to
the trusted command. No post-step may use the credential or publish a compensating
status. The App key is an environment secret, never a repository-wide secret.

### `.github/workflows/main-audit.yml`

```yaml
name: main-audit

on:
  push:
    branches: [{{DEFAULT_BRANCH}}]
  workflow_dispatch:
    inputs:
      before_sha:
        description: Existing main range start, for read-only historical audit
        required: true
        type: string
      after_sha:
        description: Existing main range end, for read-only historical audit
        required: true
        type: string

permissions:
  actions: read
  checks: read
  contents: read
  pull-requests: read
  statuses: read

concurrency:
  group: main-audit
  cancel-in-progress: false

jobs:
  audit:
    name: audit
    if: github.ref == format('refs/heads/{0}', github.event.repository.default_branch)
    runs-on: ubuntu-latest
    steps:
      - name: Check out full history
        uses: actions/checkout@{{ACTIONS_CHECKOUT_SHA}}
        with:
          fetch-depth: 0
          ref: ${{ github.sha }}
          persist-credentials: false
      - name: Prepare bounded read-only audit range
        run: |
          python3 -P - <<'PY'
          import json, os, re, subprocess
          from pathlib import Path
          event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
          if os.environ['GITHUB_EVENT_NAME'] == 'workflow_dispatch':
              before, after = (event['inputs'][key] for key in ('before_sha', 'after_sha'))
              if not all(re.fullmatch('[0-9a-f]{40}', value) for value in (before, after)) or before == after:
                  raise SystemExit('Invalid historical audit range')
              subprocess.run(['git', 'merge-base', '--is-ancestor', before, after], check=True)
              subprocess.run(['git', 'merge-base', '--is-ancestor', after, 'HEAD'], check=True)
              event = dict(repository=event['repository'], ref=os.environ['GITHUB_REF'],
                           forced=False, deleted=False, before=before, after=after)
          (Path(os.environ['RUNNER_TEMP'])/'governance-audit.json').write_text(json.dumps(event))
          PY
      - name: Audit baseline plan, amendments, and queue/progress transition
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PYTHONPATH: tools/governance
        run: >-
          python3 -P -m project_governance audit-main
          --event-path "$RUNNER_TEMP/governance-audit.json"
          --repo-root .
```

---

## 14. Governance package contract

The receiving agent must implement `tools/governance/project_governance` against this exact interface. Do not invent weaker semantics.

### CLI

```text
python -P -m project_governance self-check --repo-root PATH
python -P -m project_governance validate-pr --repository OWNER/REPO --pr-number N --head-sha SHA
python -P -m project_governance finalize --event-path PATH
python -P -m project_governance finalize-amendment --event-path PATH
python -P -m project_governance validate-final --repository OWNER/REPO --pr-number N --head-sha SHA
python -P -m project_governance audit-main --event-path PATH --repo-root PATH
```

### `policy.py` constants

```python
DEFAULT_BRANCH = "{{DEFAULT_BRANCH}}"
TASK_ID_PATTERN = r"{{TASK_PREFIX}}-[A-Z0-9]+-[0-9]{3}"
PLAN_PATH = "PLAN.md"
PLAN_AMENDMENTS_PREFIX = "plans/amendments/"
TODO_PATH = "TODO.md"
PROGRESS_PATH = "PROGRESS.md"
PLAN_BLOB_SHA = "<replace after bootstrap content is final>"

IMMUTABLE_PATHS = frozenset({"PLAN.md"})
# Existing files under PLAN_AMENDMENTS_PREFIX are immutable; only the next new PA-NNNN path may be created in amendment mode.
AUTOMATION_OWNED_PATHS = frozenset({"TODO.md", "PROGRESS.md"})
GOVERNANCE_CONTROLLED_PATHS = frozenset({
    "AGENTS.md",
    "INVARIANTS.md",
    "MASTER_PROMPT.md",
    "CONTRIBUTING.md",
    ".governance/project-ci.sh",
    ".github/pull_request_template.md",
    "docs/GOVERNANCE_AUTOMATION.md",
    "tools/governance/README.md",
})
GOVERNANCE_CONTROLLED_PREFIXES = (
    ".governance/",
    ".github/workflows/",
    "tools/governance/",
)

REQUIRED_IMPLEMENTATION_CHECKS = (
    "project-tests",
    "governance-unit",
)

POLICY_STATUS_CONTEXT = "governance/policy"
IMPLEMENTATION_STATUS_CONTEXT = "governance/implementation-verified"
FINALIZED_STATUS_CONTEXT = "governance/queue-finalized"
STATUS_CREATOR = "github-actions[bot]"
FINAL_STATUS_CREATOR = "{{GOVERNANCE_APP_BOT_LOGIN}}"
FINAL_STATUS_INTEGRATION_ID = {{FINAL_STATUS_INTEGRATION_ID}}
BUILD_WORKFLOW_PATH = ".github/workflows/build-and-test.yml"
POLICY_WORKFLOW = "governance-pr.yml"
FINAL_WORKFLOW = "governance-final.yml"
```

### Parser rules

- Parse task blocks by exact `### TASK-ID — title` headers.
- Parse accepted amendment files by strict `PA-NNNN` sequence and reject gaps at acceptance, duplicate IDs, modified historical files, or task definitions that are not canonical.
- Treat task IDs across baseline PLAN, all amendments, TODO, and PROGRESS as one global never-reuse namespace.
- Reject duplicate IDs, malformed order, or IDs in both TODO and PROGRESS.
- Accept an empty queue only as the exact `_Queue complete._` terminal sentinel; it has no front and ordinary task work must stop.
- Parse PR metadata with exactly one `Task ID:` and one `Implementer run:` field.
- Parse the PR's final discovered queue-additions section as either exact `None.` or canonical blocks. Require unique never-used IDs, non-empty outcome/acceptance/evidence, and append-only order.
- Use `canonical_pr_body` exactly as defined in MASTER_PROMPT for the entire API body and all task/amendment verification. Require both the SHA-256 digest and the ordered addition IDs where applicable. Reject changed canonical bytes; normalization-equivalent EOL/terminal-LF edits are not digest invalidations. Reject missing/non-string bodies and malformed metadata independently.
- Parse finalizer comments only when all six lines match exactly.
- Require 40 lowercase hexadecimal characters for commit SHAs.
- Use canonical UTF-8 and deterministic newline handling.
- Render progress records in one canonical form and compare byte-for-byte during final validation.

### `validate-pr`

It must fetch the PR through GitHub API and select exactly one fail-closed mode from the supplied current head: ordinary implementation head, owner-initiated plan-amendment proposal head, trusted task-ledger head, or trusted amendment-ledger head. It must never execute PR code in either privileged event context.

Before any status write, require the policy workflow's exact default-branch ref
and expected workflow identity, with event `pull_request_target` or
`workflow_dispatch`. Manual dispatch against a feature branch or tag must be
rejected before executing governance or emitting a status. The immutable
`github.sha` checkout is trusted only together with that ref/context gate;
dispatch SHA alone does not imply default-branch code. Consumers independently
verify policy run provenance and that its code SHA was accepted on the protected
default branch; a copied status description cannot establish that fact.

Use an explicit `workflow_dispatch` run selected from `{{DEFAULT_BRANCH}}` as
the authoritative pre-finalization policy evidence for both tasks and amendments.
The automatic `pull_request_target` check provides early feedback but is not a
substitute for that evidence. GitHub's workflow-run API `head_sha` and the
execution context's `github.sha` are different fields: commissioning observed
a PR-target run whose API SHA named the PR source while trusted checkout used
the base revision. Never infer the executing governance code from a PR-event
API head SHA or bypass the default-branch ancestry gate to accommodate it.

For the dispatched run, require the exact workflow path, repository identity,
`workflow_dispatch` event, default-branch selection, accepted default-branch
code SHA and successful run attempt. Independently bind its status creator,
description and target URL to the exact candidate SHA and PR. Recheck this
evidence before admission. Dispatching a preliminary check does not consume an
attempt; it does not authorize a retry after a publication/validation claim.

#### Implementation-head mode

1. Require open state, expected base, same-repository head, exact supplied head SHA, and one queue-front task ID.
2. Reject changes to every `IMMUTABLE_PATHS`, `AUTOMATION_OWNED_PATHS`, `GOVERNANCE_CONTROLLED_PATHS`, and `GOVERNANCE_CONTROLLED_PREFIXES` match. `DECISIONS.md` may change in an ordinary task only when it records an owner-approved implementation decision without weakening this contract.
3. Require the task named in the PR to equal TODO front from the base branch.
4. Require a unique implementer-run value.

#### Plan-amendment proposal mode

This mode is additive-only and cannot be used as a general protected-file exception.

1. Require open, ready, same-repository PR state, expected base, exact supplied head SHA, and a current branch containing the default-branch head.
2. Require exactly one newly added path under `plans/amendments/` named with the next gap-free `PA-NNNN` ID; reject modification, deletion, or rename of every historical amendment.
3. Require no TODO, PROGRESS, PLAN, workflow, governance-package, or other protected-file change on the proposal head.
4. Parse every added task and require globally unique never-used task IDs, canonical outcome/acceptance/evidence, and additive-only semantics.
5. Require a unique proposer/implementer-run identity in PR metadata so the independent verifier identity can be proven distinct.

#### Trusted amendment-ledger mode

After `/project amend-plan`, trusted automation advances the amendment PR branch by one bot commit. Require one parent, exact message `chore(governance): apply <PA-ID>`, trusted signed bot identity, parent-to-head changed paths exactly `TODO.md`, and byte-for-byte equality with `project_amendment` applied to the immutable proposal parent's TODO and verified additions. For pending input preserve all old TODO bytes and order, then append; for the exact terminal input preserve header/contract and replace only the sentinel region. Reject malformed or mixed input. Require producer-bound verified status tied to the exact amendment proposal parent and the same `canonical_pr_body` digest. A policy PASS at this stage does not by itself change PUBLISHED_UNVERIFIED into FINALIZED.

#### Trusted ledger-head mode

This mode exists because the ordinary task finalizer advances the same PR branch from the implementation SHA to a bot ledger SHA and dispatches policy again. It is not a general protected-file exception.

1. Require all common PR/base/repository/task/implementer checks from implementation-head mode.
2. Require exactly one full parent SHA and exactly the commit message `chore(governance): finalize <TASK-ID>`.
3. Require the complete signed bot author/committer identity defined below.
4. Require parent-to-head changed paths to be exactly TODO.md and PROGRESS.md when there are no queue additions; when verified queue additions exist, require exactly TODO.md, PROGRESS.md, and the next single `plans/amendments/PA-NNNN.md` path.
5. Reconstruct byte-for-byte the one FIFO pop, optional verified back append, optional deterministic amendment record, or exact terminal sentinel, plus one canonical push-front record using the immutable implementation parent and live PR/finalizer evidence.
6. Require the trusted producer-bound `governance/implementation-verified` success status on the ledger head, whose description names the exact implementation parent.
7. Reject every other protected-file combination, parent count, identity, message, task, record, or status.

In every mode, publish `governance/policy=success` only after every applicable check passes. Publish failure on the exact supplied SHA for every validation error. Tests must prove that a human-authored ledger lookalike, an extra changed path, a wrong parent, a modified historical amendment, and a spoofed verified status cannot enter a trusted post-finalizer mode.

### Trusted implementation evidence

The finalizer must require:

- the latest required check run for every required name;
- `status=completed` and `conclusion=success`;
- exact implementation `head_sha`;
- trusted GitHub Actions application slug;
- trusted GitHub Actions details URL belonging to `{{REPOSITORY}}`;
- one common workflow run ID and check-suite ID;
- workflow path `BUILD_WORKFLOW_PATH`;
- event `pull_request`;
- exact immutable top-level workflow `head_sha`;
- successful workflow result;
- exact repository and head-repository names;
- association with the expected PR number.

Do **not** bind historical evidence to `pull_requests[].head.sha`; GitHub may update that nested projection after the finalizer advances the same PR branch. The top-level workflow `head_sha` is the immutable implementation binding.

After a PR merges, GitHub can clear both workflow-run and check-suite
`pull_requests` lists. Open-PR/finalizer/merge-readiness validation still requires
those direct associations. Only a read-only audit of an authenticated merged
ledger may handle two explicitly empty lists by checking all of the following:

- retain every exact source, trusted App, workflow/event, repository, success and
  common run/suite check above; malformed or conflicting association lists fail;
- validate the current closed, merged PR and its unchanged full-body binding;
- bind its merge commit to exactly the prior base and ledger, with an identical
  ledger tree, and bind the ledger's sole parent to the implementation source;
- require both run and suite head branches to match that PR's original branch;
- require the run creation/start and both selected check completions to be no later than
  the immutable owner authorization, which must be no later than the merge;
- paginate the source commit's associated PRs and require exactly one match for
  that PR number, matching repository, main base, branch, ledger and merge SHA.

A branch name, source SHA alone, missing field or an unrelated PR is insufficient.
This does not recreate evidence or allocate an attempt. A historical main audit
may run current protected-default-branch code through a read-only dispatch over
an existing ancestor range; retain the original failed run and label the new
result as a historical audit rather than changing the old conclusion.


### Status provenance

Read paginated statuses from:

```text
GET /repos/{owner}/{repo}/commits/{sha}/statuses
```

Do not use the combined `/commits/{sha}/status` representation when creator provenance is required.

For policy and implementation statuses, validate the newest matching status by numeric ID. For `governance/queue-finalized`, inspect the complete candidate-bound history below first; newest-status selection cannot supersede failure or allocate another attempt. Reconciliation, merge-readiness checks and `audit-main` use this same predicate. Every selected status still requires:

- exact context;
- `state=success`;
- creator login `github-actions[bot]` for policy/implementation, dedicated `FINAL_STATUS_CREATOR` and `FINAL_STATUS_INTEGRATION_ID` for final statuses;
- canonical PR target URL when applicable;
- exact evidence description.

### Durable one-shot attempt history

Use a create-only Git reference store in the target repository. This is an additional commissioning requirement, not a service already supplied by this source repository. The store uses the four fixed refs `refs/tags/governance-attempts/v1/<numeric-repository-id>/<pr-number>/{publish,validate}/{claim,outcome}`. A claim binds the full immutable source SHA, selected ledger SHA, canonical body digest, task/amendment operation, repository/PR, and authenticated producer identity. That identity includes workflow path, trusted code SHA, workflow run ID and run attempt. The scope key intentionally excludes all caller-selected attempt IDs and even the source SHA: once admitted, the PR cannot allocate another slot by changing any of those values. A fresh candidate needs a fresh branch and PR, current default-branch base and entirely fresh evidence.

Each ref points to an immutable record commit containing the signed envelope defined below. Preserve the selected ledger commit as a parent of the claim's record commit, retaining its objects even if the PR ref is later changed. The ledger commit itself still has its required sole implementation parent. Outcomes bind the identical candidate and producer as their claim. Only CLAIM, READY and FAILED are permitted; READY authorizes one final dispatch/status attempt, it does not assert completion. There is no update, delete, expiry, lease renewal, reset or takeover operation.

The wire envelope has exactly `payload` and `signature` keys. The signature is strict base64 RSA-PKCS1-v1_5/SHA-256 over `b"AGENT-GOVERNANCE-RECORD-V1\n"` followed by the payload's canonical JSON bytes: UTF-8, sorted keys, compact separators, `ensure_ascii=False`, no floats, one final LF. Reject duplicate/unknown keys, invalid types and noncanonical encoding. Verify against the pinned governance App RSA public key, never a key provided by the record. A generic `github-actions[bot]` commit signature is insufficient. The payload has exactly these fields:

```text
schema: integer 1
repository_id, pr_number: positive integers
source_sha, ledger_sha: full lowercase 40-hex strings
body_sha256: lowercase 64-hex string
operation: "task" | "amendment"
slot: "publish/claim" | "publish/outcome" | "validate/claim" | "validate/outcome"
event: "CLAIM" | "READY" | "FAILED", constrained by slot
producer: {integration_id, login, workflow_path, code_sha, run_id, run_attempt}
authorization: {comment_id, implementer_run, verifier_run}
claim_object_sha: null for claims, otherwise the exact same-phase claim object SHA
publication_ready_object_sha: null for publish slots, exact publish READY object SHA for validate slots
audit_comment_id: positive integer for READY, otherwise null
```

All IDs/counts are positive integers; names/run identities are nonempty strings; code/object SHAs are full lowercase 40-hex strings. `integration_id`/`login` equal the pinned dedicated App. `workflow_path` is exactly the configured publisher (task or amendment) or final-validator path appropriate to the slot. `code_sha` is the exact checked-out governance revision already accepted on the protected default branch. The signer obtains workflow/run/attempt from authenticated runner context and verifies them with GitHub's run API; it never accepts them from dispatch inputs, PR content or caller-supplied record data. It validates original command ownership, source/body binding and distinct implementer/verifier identities before signing a claim. Sign READY only after checking its exact preceding audit comment's author, content, candidate/run binding and timestamp. Consumers repeat those signature, role, authorization and audit bindings. Missing API evidence blocks acceptance. The reference model below is the reduced state-machine view of already-authenticated records; its `other_gates_pass` input includes these full wire-level checks.

Before use, install and read back an active **tag** ruleset matching `refs/tags/governance-attempts/**/*`, with update and deletion restricted and **no bypass actors**. Creation remains possible; every created record must independently pass trusted producer checks. Unauthorized slot squatting is a denial of service that fails closed. An ordinary writer cannot turn it into accepted evidence. The adapter must verify the rule is still active, the exact returned ref name, object bytes, record schema, dedicated-key signature, correct role's workflow on protected default-branch code, run/attempt provenance and original owner/verifier authorization. An untrusted payload's `trusted` field is never evidence; the boolean in the executable model is adapter output only. Pin the repository's numeric identity, do not trust owner/name alone across transfers. Verify all four exact refs; a partial listing, API error or ambiguous read is not absence.

GitHub's ruleset API hides `bypass_actors` from callers without ruleset-write
access. An omitted field is **not an empty bypass list**. Do not give the
finalizer administrative write permission to work around this. Before governed
attempts exist, an authenticated owner-side administrative readback must pin an
attestation in protected default-branch configuration: numeric repository and
ruleset IDs; name, source/type, target, enforcement, complete conditions/rules;
explicit empty bypass list; creation/update timestamps; and a GitHub server-time
fence after the entire last mutation second. Re-read the complete configuration
after that fence and require equality. This owner collection is read-only; its
administrative credential never enters a PR or runtime job.

Minimal runtime readers compare every visible field and both timestamps exactly
with that pinned baseline. If `bypass_actors` is present, require exactly `[]`;
null or malformed data fails. Documented omission may use only that unchanged
owner attestation, never a PR-supplied replacement. This is an attested baseline
plus a provider change-token assumption, not live observation of hidden actors.
Commission the actual limited-token responses: hidden bypass add/remove (also
add-and-restore within a later single second), enforcement disable/restore and
delete/recreate must all invalidate the baseline. GitHub documentation does not
guarantee every required timestamp behavior; missing/stale/inconsistent metadata
or failed negative trials blocks commissioning. Complete those trials before
accepting the final baseline. A deployment that cannot establish this assumption
needs a separately reviewed protection-proof mechanism.

Protection drift invalidates trust in affected attempt histories even after the
settings are restored. Never automatically refresh the attestation or reuse
those histories. Preserve the failure; an explicit owner recovery must use fresh
branches/PRs and fresh evidence. Malicious repository administration remains
outside the threat model. See the official
[ruleset read API](https://docs.github.com/en/rest/repos/rules#get-a-repository-ruleset)
for the hidden-field permission boundary.

Atomically create the claim ref using GitHub's **create reference** operation, never check-then-update. Require an acknowledged creation of that exact object before doing work. Conflict, timeout or an existing claim permits no mutating work; reading an existing claim never grants its ownership to a restarted process. An ambiguous claim creation followed by no acknowledged admission performs no downstream side effects. If it did not commit, the first later successful claim is still the first admitted attempt. Commission concurrent creates and protection against updates/deletes on GitHub; the local SQLite test adapter demonstrates the contract only.

The publication claimant alone may advance the PR ref, observe required policy evidence, and create its finalizer audit. It then atomically creates `publish/outcome=READY` and requires its acknowledgement before its last call, final workflow dispatch. Known pre-dispatch failure instead creates `publish/outcome=FAILED`; ambiguous effects or process death may leave only the claim. None permits another publication. The validation claimant requires the exact publication READY and preceding audit, then revalidates all live gates and writes its final audit. Only afterward may it create `validate/outcome=READY` and, after acknowledgement, attempt the final success status as its last remote call. Known earlier failure instead creates `validate/outcome=FAILED`. A lost/uncommitted failure-record write still leaves the claim blocking replay. No exception handler may replace an outcome or issue a further call after the final dispatch/success attempt. Cancellation is treated like process death, not renewed admission; duplicate dispatch must not cancel the original workflow.

Every success consumer requires all four authenticated records, identical candidate bindings, two READY outcomes, the admitted validator's exact successful status, all paginated status history, and all existing final evidence gates. Sort matching statuses by ascending numeric ID. Only the admitted publisher's initial PENDING is permitted before SUCCESS; PENDING after success, missing success, any FAILURE/error, or a different producer is rejection. Bind the final status description to the admitted run ID and run attempt and verify that workflow's provenance; a later status from another producer/attempt cannot substitute. Final statuses (including initial PENDING) use the dedicated App installation token, and the required merge context is bound to that App's integration ID. Generic Actions statuses with the same name cannot satisfy that protected gate. All privileged App-token access is confined to the reviewed default-branch jobs and exact-branch environment above; if that isolation cannot be established, block commissioning. The producer's exclusive credential plus signed READY authenticates the final success assertion; a caller-controlled description alone never does. Any matching trusted failure, malformed/untrusted record, absent claim/outcome, incomplete history or inconsistent evidence blocks acceptance regardless of newer successes. A rejected duplicate emits no failure status. A separate read-only reconciliation can recognize a success whose response was lost, or report that it remains unproven; it never writes records/statuses, resumes work or repeats dispatch. The primitive below specifies these decisions; `work` and `last_call` are supplied only by trusted workflow code after authorization, never from a PR. All final success consumers must use this history predicate in addition to their other gates.

```python
"""Executable protocol model, not a GitHub adapter or authentication service.

Store.create must atomically create an immutable authenticated record or raise;
Store.read must return a complete authenticated snapshot or raise. The adapter,
never PR data, supplies producer trust and the workflow/run/attempt identity.
"""
from dataclasses import dataclass
import re


class Rejected(ValueError):
    pass


class Unknown(RuntimeError):
    pass


@dataclass(frozen=True)
class Candidate:
    repository_id: int
    pr: int
    source: str
    ledger: str
    body_sha256: str
    operation: str

    def __post_init__(self):
        if (type(self.repository_id) is not int or self.repository_id <= 0
                or type(self.pr) is not int or self.pr <= 0
                or self.operation not in ("task", "amendment")):
            raise Rejected("invalid scope")
        for value, length in ((self.source, 40), (self.ledger, 40), (self.body_sha256, 64)):
            if not isinstance(value, str) or not re.fullmatch(rf"[0-9a-f]{{{length}}}", value):
                raise Rejected("invalid digest")
        if self.source == self.ledger:
            raise Rejected("ledger must differ from source")

    @property
    def key(self):
        # A different run, body, operation or ledger does not create a fresh slot.
        return f"v1/{self.repository_id}/{self.pr}"


@dataclass(frozen=True)
class Record:
    candidate: Candidate
    owner: str  # Authenticated workflow path + trusted code SHA + run ID + attempt.
    event: str
    trusted: bool  # Adapter output after provenance verification, not wire input.


def checked_history(store, candidate):
    records = store.read(candidate.key)
    allowed = {f"{phase}/{kind}" for phase in ("publish", "validate")
               for kind in ("claim", "outcome")}
    if not isinstance(records, dict) or not set(records) <= allowed:
        raise Rejected("malformed history")
    for slot, record in records.items():
        if (not isinstance(record, Record) or record.trusted is not True
                or record.candidate != candidate or not isinstance(record.owner, str)
                or not record.owner or record.event not in ("CLAIM", "READY", "FAILED")):
            raise Rejected("untrusted or mismatched history")
        if slot.endswith("/claim"):
            if record.event != "CLAIM":
                raise Rejected("invalid admission")
        else:
            claim = records.get(slot.replace("/outcome", "/claim"))
            if (claim is None or claim.owner != record.owner
                    or record.event not in ("READY", "FAILED")):
                raise Rejected("outcome without its admitted producer")
    if any(slot.startswith("validate/") for slot in records):
        ready = records.get("publish/outcome")
        if ready is None or ready.event != "READY":
            raise Rejected("validation without authorized dispatch")
    return records


def run_phase(store, candidate, phase, owner, work, last_call):
    """Only an acknowledged first claim may work; no call follows last_call.

    publish work: exact ref publication, verified policy, finalizer audit.
    validate work: all exact final gates and durable final audit comment.
    last_call: final dispatch (publish) or success status (validate).
    Admission/provenance errors and duplicates never publish a failure status.
    """
    if phase not in ("publish", "validate") or not isinstance(owner, str) or not owner:
        raise Rejected("invalid caller")
    try:
        records = checked_history(store, candidate)
        if phase == "validate":
            if records.get("publish/outcome") is None or records["publish/outcome"].event != "READY":
                return "REJECTED"
        if f"{phase}/claim" in records:
            return "REJECTED"
        store.create(candidate.key, f"{phase}/claim", Record(candidate, owner, "CLAIM", True))
    except Rejected:
        return "REJECTED"
    except Exception:
        return "UNKNOWN"  # No acknowledged ownership; do not mutate anything else.
    try:
        work()
    except Unknown:
        return "UNKNOWN"  # A surviving claim is sufficient to prohibit replay.
    except Exception:
        try:
            store.create(candidate.key, f"{phase}/outcome", Record(candidate, owner, "FAILED", True))
        except Exception:
            return "UNKNOWN"  # The immutable claim still prevents replay.
        return "FAILED"
    try:
        store.create(candidate.key, f"{phase}/outcome", Record(candidate, owner, "READY", True))
    except Exception:
        return "UNKNOWN"  # Includes an ambiguous READY write: never proceed.
    try:
        last_call()
    except Exception:
        return "UNKNOWN"
    return "SENT"  # Transport acknowledgement alone is not FINALIZED.


def reconciled_success(store, candidate, statuses, *, other_gates_pass, complete):
    """Read-only: all status pages and all other live gates are mandatory inputs.

    statuses are authenticated Record values with PENDING/SUCCESS/FAILURE events for
    governance/queue-finalized on this exact candidate, including historical ones.
    """
    if other_gates_pass is not True or complete is not True:
        return False
    try:
        records = checked_history(store, candidate)
    except Exception:
        return False
    if len(records) != 4 or any(records[f"{p}/outcome"].event != "READY" for p in ("publish", "validate")):
        return False
    owner = records["validate/claim"].owner
    publisher = records["publish/claim"].owner
    if not statuses:
        return False
    success = False
    for status in statuses:
        if (not isinstance(status, Record) or status.trusted is not True
                or status.candidate != candidate):
            return False
        if status.event == "PENDING" and status.owner == publisher and not success:
            continue  # Only the initial publisher pending, in ascending ID order.
        if status.event == "SUCCESS" and status.owner == owner:
            success = True
        else:
            return False
    return success
```

GitHub's [reference API](https://docs.github.com/en/rest/git/refs) provides creation and fast-forward updates; `force=false` alone is **not compare-and-swap** against an expected old SHA. The publication workflow must recheck the parent immediately before its one update, never overwrite divergent work, and reject any mismatched authoritative branch-ref head afterward. This guarantees neither exclusion of unrelated branch writers nor atomic expected-old-SHA comparison. The durable admission prevents a second governance publication; all consumers check exact current state. [Tag rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) and producer checks are additional trust boundaries that require live commissioning. Neither is inferred from a green local model test.

#### Readback after acknowledged publication

Commissioning observed a PR API response still naming the source after an
acknowledged forward ref update, followed by the candidate on a later read.
Treat the PR projection separately from the authoritative Git ref. Only after
one exact acknowledged publication may its admitted invocation use a bounded
read-only observation phase (at most 31 observations within a 30-second deadline,
with at most one second between reads and bounded transport timeouts). Do not
accept a result returned after the deadline.

On every observation, verify repository identity/default branch, PR identity,
same-repository head/base, exact branch name, canonical URL, ready/open lifecycle,
metadata and unchanged canonical full-body digest. The exact branch ref must
already point to the candidate commit. A rollback to source, different ref head,
different PR head other than the original source, malformed response, body or
identity drift is rejection, never a reason to wait. Only an otherwise valid PR
projection still naming the original source while its Git ref names the candidate
may be observed again. No branch update, status, audit comment or dispatch occurs
inside this observation phase. All statuses remain blocked until PR and branch
ref both name the exact candidate and every other check passes.

Timeout or a known validation failure follows the existing immutable FAILED
outcome path; ambiguous transport follows UNKNOWN. Neither resumes a failed
invocation nor authorizes another mutation/admission. Generic PR validation and
all later acceptance gates keep their strict exact-head requirements. Emit fixed,
reviewed stage/reason codes for these refusals, never raw API responses,
credentials, arbitrary exception messages or user-controlled diagnostic text.

### `finalize`

It must:
> **Profile note:** This part continues the STRICT finalization, audit, test, ruleset, and commissioning contract.


1. accept only a new issue comment on an open, ready PR;
2. require an owner/member-authorized association configured by policy;
3. parse the exact finalizer command;
4. require task ID equals TODO front and comment head equals current implementation head;
5. require the implementation branch to contain the current default-branch head and be zero commits behind immediately before finalization;
6. require verifier-run differs from implementer-run;
7. reconstruct trusted CI and policy evidence on the implementation SHA;
8. parse the current PR body, recompute the canonical full-body SHA-256 and ordered queue-addition IDs, and reject any mismatch with the verifier payload or any duplicate anywhere in baseline PLAN, accepted plan amendments, TODO, or PROGRESS;
9. compute the TODO front pop, optional back append, terminal sentinel if needed, PROGRESS push-front, and—when queue additions exist—the next deterministic immutable plan-amendment file entirely in memory;
10. create one candidate atomic GitHub API commit object with exactly TODO/PROGRESS and, only when additions exist, the one new amendment file; creating this object is still UNPUBLISHED until the ref advances;
11. use exact message `chore(governance): finalize <TASK-ID>` and one full implementation parent SHA;
12. acquire and acknowledge the protected create-only publication claim for this PR and candidate before any branch/status/comment mutation; reject duplicate, malformed or ambiguous admission without emitting a failure status. Recheck the parent, then attempt one fast-forward ref update with `force=false` and verify both authoritative ref and PR projection through the bounded readback phase above. This is not an expected-old-SHA compare-and-swap; divergent/concurrently changed state fails closed. An ambiguous result is UNKNOWN without a second ledger mutation; confirmed publication enters PUBLISHED_UNVERIFIED;
13. set implementation-verified success on the new ledger SHA with canonical PR URL and parent-SHA description;
14. set policy and queue-finalized pending on the ledger SHA;
15. dispatch the policy workflow from the protected default branch, bind its returned/run evidence to the ledger SHA, and wait for trusted policy success;
16. create the durable finalizer audit comment;
17. create and acknowledge the immutable publication READY outcome, then dispatch the final workflow as the finalizer's last fallible remote action and return without any later API call;
18. fail without a second ledger mutation if any action before the final dispatch fails. Apply MASTER_PROMPT publication states: reject without changing PR ledgers before publication, preserve a published candidate after later failure, and report UNKNOWN on an ambiguous response. The admitted producer records a terminal FAILED outcome on known failure before READY; a lost failure record or process death leaves the immutable claim blocking replay. A failure status is diagnostic only and may be emitted solely by the admitted producer before its last-call boundary. No exception path overwrites READY or makes a call after final dispatch. A later read-only reconciliation must establish complete attempt history and all other gates before recognizing FINALIZED; a dispatch response alone is not completion.

### `finalize-amendment`

It must:

1. accept only `/project amend-plan` on an open, ready, same-repository PR in plan-amendment proposal mode;
2. require owner/member authorization and exact next `PA-NNNN`;
3. bind the command to the current amendment proposal SHA and full canonical PR-body digest;
4. require exact-head project/governance checks and trusted policy provenance;
5. require verifier-run differs from proposer/implementer-run;
6. re-parse the amendment file and reject any task ID already present in baseline PLAN, prior amendments, TODO, or PROGRESS;
7. require the branch to contain current default branch and be zero commits behind immediately before mutation;
8. compute the TODO projection entirely in memory through `project_amendment`: append behind pending tasks without changing their bytes/order, or replace only the exact terminal sentinel region while preserving header/contract; reject malformed/mixed input;
9. create one candidate sole-parent bot commit object changing only TODO.md, with exact message `chore(governance): apply <PA-ID>`; this is UNPUBLISHED until ref advancement;
10. acquire the same protected create-only publication admission before any branch/status/comment mutation, recheck the proposal parent, then attempt one `force=false` fast-forward ref update and verify the observed candidate through the same bounded readback phase as ordinary finalization; this is not compare-and-swap. Confirmed publication enters PUBLISHED_UNVERIFIED and an ambiguous result is UNKNOWN, never permission for a second mutation;
11. publish the producer-bound verified/pending statuses required by policy and follow the same policy wait, durable finalizer audit, immutable publication READY, last-call dispatch, validation admission, final audit and immutable validation READY ordering as ordinary finalization;
12. never mutate PLAN.md or any previously accepted amendment file.

A failed or ambiguous amendment finalization follows MASTER_PROMPT publication states. Before publication its rejection leaves PR-branch TODO unchanged; afterward preserve the candidate commit without accepting completion. UNKNOWN requires separate read-only reconciliation, not retry or rollback. Known failure recovery uses a fresh branch and fresh evidence. Never attempt a second TODO mutation or write PROGRESS/default-branch state.

### Trusted finalizer commit identity

On GitHub.com, validate the observed signed Actions API-commit model:

- mapped author login `github-actions[bot]`;
- mapped committer login `web-flow`;
- Git author `github-actions[bot]` with canonical bot noreply email;
- Git committer `GitHub <noreply@github.com>`;
- GitHub verification `verified=true`, `reason=valid`;
- exact commit message;
- one full implementation parent SHA;
- producer-bound implementation-verified status on the ledger head.

If the repository is hosted outside GitHub.com, commission and pin that provider's actual signed bot identity instead of guessing.

### `validate-final`

It must reconstruct and compare all evidence again from live GitHub state, including the exact successful ledger-policy run/status and the durable finalizer audit comment that must predate this workflow dispatch. For owner amendments, reconstruct TODO through `project_amendment`; every full-body digest is computed through `canonical_pr_body`. A candidate stays PUBLISHED_UNVERIFIED until all final gates are established; policy success or the presence of a PROGRESS record alone is insufficient.

Order remote side effects through the one-shot validation protocol as follows:

1. verify complete protected publication history and acknowledge the first validation claim; duplicate, ambiguous or invalid admission returns without any status/comment mutation;
2. validate everything;
3. write the durable final audit comment;
4. create and acknowledge the immutable validation READY outcome bound to that audit and the admitted workflow run/attempt;
5. publish `governance/queue-finalized=success` as the last fallible remote action, bound to that admitted producer.

If validation or the comment fails before READY, this invocation must not publish success; record the immutable FAILED outcome without hiding the original error. A lost failure-record response or process death leaves the claim blocking any subsequent admission. Failure-status publication is diagnostic, not the terminal-history mechanism, and is optional for the admitted producer before READY. After attempting final success publication, make no further remote call or compensating write. A lost response is UNKNOWN until separate read-only reconciliation of complete attempt history and all exact-head gates, not proof of either failure or completion. Preserve the candidate commit in all post-publication failure paths. No later run, rerun, edited body, alternate candidate identity or newer status can repair this PR's missing/FAILED outcome.

### `audit-main`

On every default-branch push:

- verify the baseline PLAN blob hash;
- verify every accepted plan amendment remains byte-identical to its introduction commit and the amendment sequence is canonical;
- allow an ordinary task merge only when the merged PR contains a valid trusted ledger commit tied to the implementation parent;
- allow an owner-initiated amendment merge only when the amendment proposal and its bot TODO projection equal `project_amendment`, including the exact terminal-reactivation branch, and all amendment evidence satisfies the protocol;
- reconstruct the exact FIFO pop, optional verified back append, optional generated amendment record, terminal sentinel, and push-front progress record; use `canonical_pr_body` for body-bound evidence and reject any merged candidate lacking established FINALIZED evidence;
- reconstruct and authenticate all four protected attempt refs and the admitted validator's complete status history through the shared reconciliation predicate; fail on unavailable/incomplete history, terminal failure or substituted producers, even if a newer status is green;
- reject manual, multiple, missing, reordered, or malformed ledger transitions;
- support a narrowly documented bootstrap exception only for the first governance installation;
- never add broad exceptions merely to make historical red runs disappear.

---

## 15. Mandatory STRICT governance tests

The test suite must cover at least:

### Queue and ledger

- exact FIFO pop;
- push-front insertion;
- zero, one, and multiple canonical discovered tasks appended strictly at the back during the same finalizer transition;
- malformed, duplicate, previously used, or verifier-unreported queue additions rejected;
- changes to canonical PR-body bytes in metadata, scope, evidence, risks, queue-addition content, internal whitespace, or order invalidate the verifier full-body digest;
- CRLF/lone-CR versus LF and extra terminal LF characters alone produce equal canonical bytes/digests; trailing spaces/tabs, internal blank lines and Unicode changes are not normalized away;
- all body consumers agree with the exact `canonical_pr_body` algorithm; invalid metadata or missing bodies remain rejected even when a digest is supplied;
- final task with no additions renders and parses the exact queue-complete sentinel and a `none` progress front;
- existing progress bytes preserved;
- duplicate/overlapping IDs rejected;
- malformed queue and any non-canonical empty representation rejected;
- pre-publication rejection leaves both PR-ledger inputs unchanged; creating unreachable commit objects does not constitute publication;
- fault injection after ref publication preserves exactly one atomic candidate transition and never certifies completion, mutates the default branch, or causes a second ledger mutation;
- acknowledged publication with a stale PR projection then the exact candidate passes only after both PR and authoritative ref agree; permanent staleness times out, while a third head, ref rollback, changed body/lifecycle/repository or malformed response fails without a readback retry or status; these tests use the actual PR validator and separate ref/PR observations, not a synchronously updated PR mock;
- ambiguous ref/dispatch/final-status responses produce UNKNOWN observations; no retries or compensating writes occur across the specified last-call boundaries;
- durable first-admission races admit exactly one producer; restart, rerun, fabricated attempt ID, changed source/body/ledger or operation cannot allocate another slot on the same PR;
- known failure, uncommitted/committed lost failure records and process death cannot be superseded by later success; UNKNOWN reconciliation is read-only and recognizes success only if all exact evidence already exists;
- rejected duplicates neither cancel nor poison the original in-flight or successful attempt;
- exact canonical record reconstruction;
- wrong SHA, branch, PR, paths, checks, comment ID, or run identities rejected.
- every exact protected path and prefix is rejected on an implementation head;
- DECISIONS-only owner-approved records do not create a general governance-file exception.

### Plan evolution

- baseline PLAN hash remains unchanged forever after bootstrap;
- existing amendment edit/delete/rename is rejected;
- gap, duplicate, malformed, or out-of-order amendment IDs are rejected;
- amendment task IDs already used anywhere are rejected;
- owner-initiated amendment proposal cannot edit TODO/PROGRESS directly;
- amendment finalizer appends tasks strictly to the back and changes only TODO.md;
- owner-initiated amendment reopens an exact terminal `_Queue complete._` state by replacing only the sentinel task region, while preserving the TODO header/contract;
- `project_amendment` is shared by the finalizer, trusted amendment-ledger policy, final validation and main audit; self-check uses the same pending/terminal parser;
- literal UTF-8 byte vectors cover one/multiple additions for pending and terminal input, one separator LF and one block-final LF; extra/missing separators, CR, malformed encoding, misplaced markers and sentinel/task mixtures fail closed;
- mutated headers, changed old tasks/order, retained sentinel, malformed empty state and extra files are rejected in all applicable validators;
- ordinary queue additions generate exactly one deterministic next amendment file in the task finalizer commit;
- zero queue additions generate no amendment file;
- amendment rejection before ref publication leaves PR-branch TODO unchanged; failure afterward retains one candidate TODO projection without PROGRESS/default-branch changes or a second mutation;
- an amendment cannot insert ahead of the current front or weaken an existing task.

### CI and workflow provenance

- missing, cancelled, skipped, timed-out, or failed checks rejected;
- untrusted check application rejected;
- wrong run ID, suite ID, workflow, event, top-level head SHA, repository, head repository, PR number, or result rejected;
- multiple workflow runs/suites rejected;
- changed nested PR head accepted only while immutable top-level head and PR number remain exact.

### Status provenance

- paginated `/statuses` endpoint used;
- newest matching numeric status ID selected for policy/implementation; final success additionally requires complete immutable attempt history and the admitted run/attempt, never latest-status-only selection;
- missing/untrusted creator rejected;
- wrong target URL or description rejected;
- selected terminal evidence must be success; initial publisher pending is handled only by the complete final-history rule below.
- ruleset payload binds every required context to the configured trusted integration ID.
- complete final-status history accepts publisher PENDING followed by admitted-validator SUCCESS and rejects pending-after-success, other producers and any historical failure;
- wrong App, forged record signature, duplicate/unknown JSON keys, wrong slot/claim/audit/authorization/run binding and a public key supplied by the record are rejected;
- a generic Actions token cannot satisfy the App-bound final merge gate, and a PR-ref job cannot retrieve the exact-default-branch environment secret.
- limited-token ruleset responses omit hidden bypass actors without being mistaken for an empty list; a protected owner attestation binds every visible field and a whole-second server-time fence. Hidden bypass changes/restoration and rule deletion/recreation invalidate that baseline, and drift never triggers automatic re-attestation of old attempt history.

### Finalizer commit

- exact signed bot identity accepted;
- wrong mapped author/committer rejected;
- wrong Git author email rejected;
- wrong Git committer rejected;
- missing/invalid signature rejected;
- wrong message or parent count rejected;
- spoofed implementation status rejected.

### Permissions and ordering

- every workflow whose code calls `add_comment` has `pull-requests: write`;
- finalizer dispatches and observes ledger policy success, then writes its durable comment, then attempts final-workflow dispatch as its last remote call;
- policy failure or finalizer-comment denial prevents final-workflow dispatch and final success;
- no finalizer remote call occurs after the final-workflow dispatch attempt, including on an ambiguous dispatch error;
- comment is recorded before final success status;
- simulated comment denial publishes no success and makes the admitted attempt terminal; even failure-record write loss cannot grant another admission (a failure status is optional diagnostic output);
- after attempting final success status publication there is no further remote call, even when its response is ambiguous; later reconciliation is a separate read-only operation.

### Repository self-check

- pinned baseline PLAN hash;
- canonical immutable amendment sequence and global task-ID uniqueness;
- exactly one queue front, or the exact terminal queue-complete sentinel, parsed with the same region classification used by `project_amendment`; structural validity alone is not FINALIZED evidence;
- TODO/PROGRESS disjointness;
- deterministic output suitable for CI.

---

## 16. `docs/GOVERNANCE_AUTOMATION.md` content requirements

Document, in repository-specific language:

- authoritative files and their ownership;
- immutable baseline PLAN plus append-only plan-amendment semantics and the effective-roadmap projection;
- FIFO, verified back-append, terminal empty-queue, push-front semantics and the single `project_amendment` projection used by every amendment consumer;
- task branch/PR lifecycle;
- PR metadata and finalizer command;
- exact `canonical_pr_body` hashing, queue-addition ID binding, canonical-content invalidation and explicitly permitted normalization equivalences (not raw-byte/edit-history binding);
- required check/status contexts;
- implementer/verifier separation;
- trusted-main execution boundary;
- exact commit/status/workflow provenance;
- UNPUBLISHED, PUBLISHED_UNVERIFIED, FINALIZED and UNKNOWN publication observations, branch-specific failure guarantees, last-call boundaries and fresh-branch recovery rules;
- bootstrap exception and its removal;
- local commands;
- protected-branch ruleset;
- protected immutable attempt-tag ruleset, create-only store adapter, authenticated phase-specific producers, record retention, one-shot admission, and read-only reconciliation;
- live commissioning procedure.

The document explains the implementation. It cannot override AGENTS, INVARIANTS, the baseline PLAN, accepted plan amendments, or MASTER_PROMPT.

---

## 17. Protected default-branch ruleset

After bootstrap workflows are present on `{{DEFAULT_BRANCH}}`, create a ruleset equivalent to:

```json
{
  "name": "Protect_Default_Branch",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "conditions": {
    "ref_name": {
      "include": ["~DEFAULT_BRANCH"],
      "exclude": []
    }
  },
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {
      "type": "pull_request",
      "parameters": {
        "allowed_merge_methods": ["merge"],
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_approving_review_count": 0,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "do_not_enforce_on_create": false,
        "strict_required_status_checks_policy": true,
        "required_status_checks": [
          {
            "context": "governance/policy",
            "integration_id": {{TRUSTED_STATUS_INTEGRATION_ID}}
          },
          {
            "context": "governance/implementation-verified",
            "integration_id": {{TRUSTED_STATUS_INTEGRATION_ID}}
          },
          {
            "context": "governance/queue-finalized",
            "integration_id": {{FINAL_STATUS_INTEGRATION_ID}}
          }
        ]
      }
    }
  ]
}
```

Also verify repository Actions settings allow the trusted workflows the declared write permissions.

Verify merge-only behavior from the effective default-branch pull-request rule:
its `allowed_merge_methods` must be exactly `["merge"]`. GitHub may omit the
repository's `allow_merge_commit`, `allow_squash_merge` and `allow_rebase_merge`
fields from a read-only workflow token's response. If all three are absent,
the live effective rule establishes the governed branch's merge restriction;
do not grant write permissions just to expose repository settings. If any field
is present, require the complete exact boolean tuple `(true, false, false)` as
well. Missing or broader effective method rules, partial/conflicting settings,
and any missing existing protection still reject. Verify this path with the
actual read-only hosted audit identity during commissioning.

Install a separate active tag ruleset before either finalizer is enabled: match `refs/tags/governance-attempts/**/*`, restrict updates and deletion, leave creation allowed, and give no actor a bypass. Re-read the effective rule and live-test concurrent creation, denied modification/deletion (including by the App), invalid producer rejection and durable retrieval. The dedicated App needs contents/statuses write for immutable records and final statuses; keep its token separate from `GITHUB_TOKEN` used for the existing signed ledger-commit model and other API calls. `audit-main` and merge-readiness/reconciliation need read access to records and GitHub run/status provenance. Prove that a generic Actions token cannot satisfy the required final context even when its description copies the admitted run. Prove that a PR-branch workflow cannot acquire the App key/token from the exact-default-branch environment. If the hosting plan cannot enforce these protections, this contract cannot be commissioned there. Do not replace this gate with a local file, expiring Actions artifact or concurrency group.

Do not keep a permanent human bypass. If a critical commissioning repair cannot satisfy task-only statuses, any temporary bypass must be:

- explicitly owner-authorized;
- one named user or team only;
- pull-request-only;
- applied immediately before an exact-SHA merge;
- removed immediately after merge;
- followed by a full ruleset re-read proving no other rule changed.

---

## 18. Bootstrap and live commissioning sequence

### Phase A — Local bootstrap

1. Finalize baseline PLAN/TODO/PROGRESS initial content and create `plans/amendments/README.md`.
2. Pin PLAN hash.
3. Configure the real project CI adapter.
4. Run project CI.
5. Run governance unit tests and self-check.
6. Parse every YAML workflow.
7. Search for remaining placeholders.
8. Request independent verifier PASS.

### Phase B — Bootstrap PR

1. Push bootstrap branch.
2. Open draft PR.
3. Verify build/test workflow on exact head.
4. Verify no untrusted PR code runs with write tokens.
5. Merge only under an explicit bootstrap exception documented in PROGRESS and DECISIONS.
6. Confirm post-merge build and main audit behavior.

### Phase C — Ruleset installation

1. Install the active no-bypass ruleset.
2. Re-fetch it from GitHub.
3. Confirm default-branch condition, strict checks, each required context's trusted `integration_id`, thread resolution, deletion, non-fast-forward, merge-only policy, and empty bypass list.

### Phase D — First real task commissioning

The first ordinary task is also a live governance integration test. Verify all of these, not only local unit tests:

- policy status creator/URL/description;
- workflow run and check-suite provenance;
- exact implementation SHA;
- finalizer comment authorization;
- GitHub API commit mapped author/committer/signature;
- finalizer post-commit PR comment permission;
- historical workflow nested-head mutation behavior;
- final validator PR comment permission;
- comment-before-success ordering;
- policy-success-before-finalizer-comment-before-final-dispatch ordering, with no finalizer call after dispatch;
- bot ledger exact governed diff and sole parent (TODO/PROGRESS, plus one amendment file only when additions exist);
- final required statuses;
- protected merge without bypass;
- main audit and main project CI.

Treat any mismatch as a commissioning bug, not as permission to weaken evidence.

---

## 19. Final STRICT bootstrap acceptance checklist

The receiving agent may declare bootstrap complete only when all boxes are true:

- [ ] No `{{PLACEHOLDER}}` remains in generated repository artifacts; the source guide is outside the repository or explicitly excluded.
- [ ] No bootstrap-only angle token remains in PLAN, TODO, or policy constants; valid runtime/sentinel forms were reviewed explicitly.
- [ ] PLAN contains the complete roadmap known at bootstrap time, is explicitly the immutable baseline, and its hash is pinned.
- [ ] `plans/amendments/` exists, its append-only contract is documented, and no accepted amendment can be modified in place.
- [ ] TODO front and next task exist and match the effective roadmap (baseline plus accepted amendments).
- [ ] PROGRESS has only the documented bootstrap record or is empty before bootstrap merge.
- [ ] DECISIONS contains every owner-authorized exception.
- [ ] Project CI adapter performs a real clean verification.
- [ ] Governance tests cover all mandatory cases.
- [ ] Repository self-check passes.
- [ ] Every workflow YAML parses.
- [ ] Independent verifier passed the exact bootstrap head.
- [ ] Trusted workflows exist on the default branch.
- [ ] Protected ruleset is active and has no bypass.
- [ ] Three governance status contexts are required and strict.
- [ ] Every required status context is bound to the observed trusted integration ID.
- [ ] Review-thread resolution is required.
- [ ] First live task exercised the full finalizer path.
- [ ] Verifier evidence uses `canonical_pr_body` and ordered queue-addition IDs; changed canonical bytes invalidate it and normalization-equivalent EOL/terminal-LF edits do not.
- [ ] Bot commit identity and status provenance were observed, not assumed.
- [ ] Both comment-producing workflows can create durable PR comments.
- [ ] Finalizer policy wait, audit comment, and final dispatch ordering is tested; no finalizer API call follows the dispatch attempt.
- [ ] Final success publication is the last attempted remote action; an ambiguous response causes no compensating write.
- [ ] All amendment consumers agree on `project_amendment` for pending, exact-terminal and malformed inputs.
- [ ] Pre-publication rejection, post-publication failure and UNKNOWN responses obey their branch-specific guarantees without a second mutation or false completion.
- [ ] Protected attempt-tag ruleset and authenticated create-only adapter are live-tested; duplicate/concurrent admission, terminal failure, lost records and read-only UNKNOWN reconciliation cannot fabricate completion.
- [ ] Main audit and project CI pass after the first task merge.
- [ ] `TODO.md` advanced exactly one task and `PROGRESS.md` gained exactly one newest-first record.
- [ ] If the first live task declared queue additions, the same trusted finalizer commit created exactly one canonical next plan-amendment file; otherwise it created none.

---

## 20. Compact handoff prompt

After adding this guide to a new conversation, the owner may say:

```text
Read UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md in full and treat it as the bootstrap specification.
Inspect the repository first. Ask only for unresolved bootstrap variables.
Create the governance system on a dedicated bootstrap branch, including all docs,
tests, GitHub Actions workflows, ruleset payload, and live commissioning evidence.
Do not begin ordinary product work until bootstrap acceptance and independent
verification pass. Never write directly to the protected default branch.
```

---

## 21. Deliberate project-specific choices

This guide does not decide the following for every project. The receiving agent must make them explicit and record them:

- actual clean build/test/lint/security commands;
- compiler/runtime/platform matrix;
- benchmark requirements;
- data and artifact retention;
- release/version format;
- code-owner and review-count policy;
- fork contribution policy;
- self-hosted GitHub Enterprise bot identity differences;
- milestone and task decomposition;
- whether a later governance version should support supersede/cancel/reorder amendments beyond the additive-only v0.x model;
- language-specific lifetime, fuzzing, property, model, migration, or compatibility tests.

Generic governance is not a substitute for project-specific correctness criteria. It makes those criteria durable, ordered, independently verified, and fail-closed.
