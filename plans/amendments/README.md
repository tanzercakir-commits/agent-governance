# Plan amendments

`PLAN.md` is the immutable bootstrap baseline. This directory is the append-only history of accepted roadmap growth.

## Contract

- IDs are `PA-0001`, `PA-0002`, ... and are accepted in gap-free numeric order.
- A merged amendment file is immutable: never edit, delete, rename, or replace it.
- v0.x amendments are additive only. They may introduce new globally unique task IDs and append them to the back of `TODO.md`.
- They may not reorder the queue, insert ahead of the current front, cancel existing work, or weaken existing acceptance criteria.
- Work discovered during a normal task is materialized here by trusted finalization.
- Owner-initiated roadmap growth uses a dedicated amendment PR and trusted `/project amend-plan` finalization.
- If `TODO.md` is already at the exact `_Queue complete._` terminal state, a trusted owner-initiated amendment may reactivate it by replacing only that sentinel task region with the newly accepted canonical task blocks.

The effective roadmap is:

```text
PLAN.md + PA-0001.md + PA-0002.md + ...
```

The history stays immutable; the future may grow.
