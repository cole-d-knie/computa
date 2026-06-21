# Computa Completion Artifact

Use this template whenever a queue item, phase, task, Super-Phase, 4D campaign, or Export Control campaign reaches a terminal state.

File name:

- `completion-<queue_id>.md` for execution-queue rows.
- `completion-<scope-id>.md` when no queue ID exists yet.

Place the file in the smallest relevant artifact directory:

- task completion: `<task>/completion-<queue_id>.md`
- phase completion: `<phase>/completion-<queue_id>.md`
- Super-Phase completion: `<super-phase>/completion-<queue_id>.md`
- campaign/session completion: `<session>/reports/completion-<queue_id>.md`

## Required Fields

- `queue_id`:
- `session_id`:
- `scope_type`:
- `scope_id`:
- `skill`:
- `terminal_status`: `complete`, `deferred`, `blocked`, or `superseded`
- `started_at`:
- `completed_at`:
- `artifact_path`:
- `evidence_path`:
- `commit_sha`:

## What Changed

List the code, docs, ledgers, configs, dashboards, external systems, or generated artifacts changed by this item.

## Verification

List exact commands, runtime checks, screenshots, reports, or reasons verification was blocked.

## Review Result

Summarize adversarial review and judge/verifier outcome for this item, or explain why the item is documentation-only or review-deferred.

## Next Action

State the next queue item, blocker, or resume point. Do not rely on chat context.
