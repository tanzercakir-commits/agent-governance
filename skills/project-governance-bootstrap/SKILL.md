---
name: project-governance-bootstrap
description: Prepare or audit repository governance for AI-assisted projects with an immutable plan, ordered tasks, independent review and exact-commit evidence. Use when the user requests project governance setup or an audit of an existing governance workflow.
license: MIT
---

# Project Governance Bootstrap

Use this skill when the user wants repository-enforced process rather than prompt-only discipline.

This is a bootstrap specification, not an installed enforcement service. Keep
the user's scope and existing authorization boundaries: preparing files does
not authorize protected merges, settings changes, secret installation or public
release. Report local preparation separately from live commissioning.

## Core stance

Do not assume the coding agent will always remember or obey process. Put acceptance conditions in repository-owned artifacts, CI policy, durable evidence and protected-branch rules. Missing or ambiguous evidence fails closed.

## Required reference

Before making governance changes, read [`references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md`](references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md) in full. It is the normative bootstrap specification bundled with this skill.

## Workflow

1. Inspect the target repository without changing it. Preserve unrelated work.
2. Discover all bootstrap variables that can be safely discovered. Ask only for unresolved values.
3. Create a dedicated bootstrap branch; never bootstrap directly on the default branch.
4. Instantiate the required normative files, governance package, workflows, project-CI adapter and ruleset payload from the reference guide.
5. Treat `PLAN.md` as the immutable baseline. Configure `plans/amendments/` as append-only roadmap evolution; do not solve future discovery by making PLAN mutable.
6. Keep TODO front-only/FIFO and PROGRESS completion-only. Normal task agents must not manually mutate either ledger.
7. Pin external action revisions and bind CI/status evidence to trusted provenance and exact SHAs.
8. Run local project CI, governance unit tests, self-checks, YAML parsing and placeholder scans.
9. Request a read-only independent verifier on the exact stable bootstrap head. The verifier must not mutate state.
10. Commission the live GitHub workflows on a draft PR, then install/re-read protected-branch rules only after the status producers exist.
11. Exercise the first real task end-to-end. Treat any mismatch between the spec and live GitHub behavior as a commissioning bug, not permission to weaken evidence.

## Non-negotiable behaviors

- Do not rewrite a failed governance run into success.
- Do not reuse verifier, CI, status, run, suite, PR or SHA evidence from another state.
- Do not weaken tests/invariants/policy to get green.
- Do not let the implementer self-approve.
- Do not edit the baseline PLAN after bootstrap or an accepted amendment after merge.
- Do not insert ordinary newly discovered work ahead of the current TODO front.
- Do not claim completion from chat text. Require durable repository evidence.

## Existing repositories

If governance files already exist, reconcile deliberately and preserve stricter controls. Never silently overwrite them with this template.

## Output

At the end of bootstrap, report the exact branch/PR/head, local checks, independent-verifier result, live status producers, protected ruleset state, queue front, and any remaining blockers. Do not claim the project is governed until the full acceptance checklist in the reference guide passes.
