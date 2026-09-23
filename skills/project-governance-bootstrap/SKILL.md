---
name: project-governance-bootstrap
description: Prepare or audit risk-proportional repository governance for AI-assisted projects. Default ordinary product work to a practical CI/review loop and escalate to exact-commit fail-closed controls only for justified high-assurance boundaries.
license: MIT
---

# Project Governance Bootstrap

Use this skill when the user wants repository-enforced process rather than prompt-only discipline.

This is a bootstrap specification, not an installed enforcement service. Keep
the user's scope and existing authorization boundaries: preparing files does
not authorize protected merges, settings changes, secret installation or public
release. Report local preparation separately from live commissioning.

## Core stance

Governance must protect delivery, not become the dominant delivery workload.
Choose the lightest profile that preserves the real risk boundary.

- **PRACTICAL** is the default for ordinary product development.
- **REVIEWED** adds independent exact-change review for material engineering risk.
- **STRICT** uses the full fail-closed provenance/finalization protocol for
  governance, security, auth, release, protected-state, destructive, or
  owner-declared high-assurance boundaries.

Do not install STRICT machinery merely because it is available. Missing or
ambiguous evidence fails closed only for evidence that the selected profile
actually requires.

## Required reference

Before making governance changes, read [`references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md`](references/UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md) in full. It is the normative bootstrap specification bundled with this skill.

## Workflow

1. Inspect the target repository without changing it. Preserve unrelated work and stricter controls.
2. Classify the repository/change surface. Default to PRACTICAL unless a STRICT trigger exists or the owner explicitly requests high assurance.
3. For PRACTICAL, reuse the project's existing branch protection, CI and review path. Add only missing plan/queue/progress/decision artifacts; do not create privileged governance infrastructure by default.
4. For REVIEWED work, add one fresh read-only independent review of the stable exact diff and relevant evidence.
5. For STRICT, follow the complete reference guide: dedicated bootstrap branch, normative files, governance package, pinned workflows, project-CI adapter, provenance/status bindings, independent verifier, rulesets and commissioning.
6. Keep task scope bounded. A finding blocks only failed acceptance, a relevant required gate, material changed-scope risk, or invalid required evidence.
7. Record non-blocking improvements as deferred work instead of extending the active task.
8. In PRACTICAL, do not let a blocked front item freeze unrelated delivery: the owner may explicitly defer, cancel, reprioritize or supersede it with a durable decision. Agents never do this silently.
9. Allow bounded batching of adjacent PRACTICAL routine tasks when each task's acceptance remains explicit. Do not silently batch REVIEWED/STRICT work.
10. Prefer focused deterministic checks before broad review. Repeat a full audit only when new evidence invalidates it.
11. Report the selected profile and why; never claim STRICT guarantees from a PRACTICAL setup.

## Non-negotiable behaviors

- Do not weaken tests, invariants, acceptance criteria, or existing stricter controls to get green.
- Do not turn a useful but non-blocking improvement into a blocker for the current task.
- Do not create new governance/evidence/benchmark machinery inside a task unless it closes a real blocker or the owner authorizes that scope.
- When independent verification is required, do not let the implementer self-approve.
- Under STRICT, do not rewrite a failed governance run into success or reuse verifier/CI/status/run/suite/PR/SHA evidence from another state.
- Do not claim completion from chat text; use the durable evidence required by the selected profile.

## Existing repositories

If governance files already exist, reconcile deliberately and preserve stricter controls. Never silently overwrite them with this template.

## Output

Always report the selected profile, the risk reason, the checks actually required,
and remaining blockers. For STRICT, also report exact branch/PR/head, verifier
result, live status producers, protected ruleset state, queue front, and full
commissioning status. Do not claim STRICT governance until the final STRICT
acceptance checklist in the reference guide passes.
