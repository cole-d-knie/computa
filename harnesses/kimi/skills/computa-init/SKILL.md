---
name: computa-init
description: Initialize shared Computa project structure for computa-make-no-mistakes, computa-4d-chess, computa-export-control, and architecture-docs work. Use when starting any Computa session or when a project needs docs/computa-artifacts, session ledgers, gitignore handling, or shared artifact directories created before planning.
---

# Computa Init

Use this as the shared initializer for every Computa layer. It creates project-local artifact structure and makes it safe for multiple independent sessions to coexist in the same project.

## Root Rules

Use the invocation root as the project root unless the user provides a more specific root. If invoked inside a git repo, prefer the git top-level so one repo has one Computa artifact root.

Create `docs/` if it does not exist. Then create or reuse:

- `docs/computa-artifacts/`
- `docs/computa-artifacts/artifact-index.md`
- `docs/computa-artifacts/session-ledger.csv`
- `docs/computa-artifacts/activity-log.csv`
- `docs/computa-artifacts/execution-queue.csv`
- `docs/computa-artifacts/execution-queue.md`
- `docs/computa-artifacts/secrets-needed/`
- `docs/computa-artifacts/secrets-needed/index.md`
- `docs/computa-artifacts/secrets-needed/secrets-needed.csv`
- `docs/computa-artifacts/secrets-needed/computer-use-prompts/`
- `docs/computa-artifacts/export-control/`
- `docs/computa-artifacts/4d-chess/`
- `docs/computa-artifacts/computa/`
- `docs/computa-artifacts/shared/`

If `docs/computa-artifacts/` is inside a git repo, ensure it is ignored. Add the correct relative `.gitignore` entry, usually `/docs/computa-artifacts/`, without duplicating an existing equivalent entry. If the invocation root is not inside a git repo, create the artifacts anyway and skip gitignore work.

## Session Model

Never overwrite prior sessions. Create a new session directory for each invocation:

- Export Control: `docs/computa-artifacts/export-control/EC-YYYYMMDD-HHMMSS-slug/`
- 4D Chess: `docs/computa-artifacts/4d-chess/4D-YYYYMMDD-HHMMSS-slug/`
- Computa Make No Mistakes: `docs/computa-artifacts/computa/CMN-YYYYMMDD-HHMMSS-slug/`

Nested sessions live under their parent session:

- Export Control child 4D sessions: `<EC-session>/4d-chess/4D-.../`
- 4D child Computa sessions: `<4D-session>/computa/CMN-.../`

Register every session, standalone or nested, in `docs/computa-artifacts/session-ledger.csv` with:

`session_id,layer,parent_session_id,status,invocation_root,session_path,user_task_path,started_at,completed_at,task_slug,summary_path,next_action`

## Activity Log

Maintain `docs/computa-artifacts/activity-log.csv` as the root resume log for every Export Control, 4D Chess, and Computa session in the project, including nested child sessions.

Create it with this header:

`timestamp,session_id,layer,parent_session_id,event_type,scope_type,scope_id,scope_name,status,artifact_path,evidence_path,next_action,notes`

Append a row immediately when a resumable unit starts, finishes, blocks, defers, or changes materially. Do not wait until closeout. Do not duplicate subtask-level detail here; subtasks are already tracked inside task directories. This root log is for session, campaign, Super-Phase, phase, and task resume points.

Required events:

- Queue: `queue_initialized`, `queue_expanded`, `queue_item_started`, `queue_item_completed`, `queue_item_blocked`, `queue_item_deferred`, `queue_item_superseded`.
- Export Control: `session_started`, `research_task_started`, `research_task_completed`, `research_task_blocked`, `audit_suite_started`, `audit_task_started`, `audit_task_completed`, `audit_task_blocked`, `audit_suite_completed`, `audit_suite_blocked`, `campaign_started`, `campaign_completed`, `campaign_blocked`, `security_closeout_started`, `security_closeout_completed`, `security_closeout_blocked`, `security_closeout_deferred`, `session_completed`, `session_blocked`.
- 4D Chess: `session_started`, `super_phase_created`, `super_phase_started`, `super_phase_completed`, `super_phase_blocked`, `security_checkpoint_started`, `security_checkpoint_completed`, `security_checkpoint_blocked`, `security_checkpoint_deferred`, `session_completed`, `session_blocked`.
- Computa Make No Mistakes: `session_started`, `phase_started`, `task_started`, `task_completed`, `phase_completed`, `phase_blocked`, `session_completed`, `session_blocked`.
- Cross-layer secrets: `secret_needed_added`, `secret_needed_updated`, `secret_configured`, `secret_verification_blocked`.

Use `artifact_path` for the directory or file a fresh agent should open first, `evidence_path` for proof of the status when available, and `next_action` for the exact resume instruction. If a crash happens, `computa-resume` must be able to identify the latest unfinished top-level or nested work from this CSV plus the session ledger.

## Raw Task Capture

Immediately save `user-task.md` in the new session before summarizing or planning. Include:

- raw user request
- timestamp
- skill/invocation name
- invocation root and repo/path
- base branch and working branch when applicable
- explicit permissions, exclusions, and do-not-touch areas
- parent session ID when applicable
- initial assumptions and ambiguities

## Execution Queue

Initialize `docs/computa-artifacts/execution-queue.csv` with:

`queue_id,parent_queue_id,session_id,layer,scope_type,scope_id,scope_name,skill,action,priority,status,dependencies,non_overlap_key,allowed_parallelism,required_outputs,review_gate,artifact_path,evidence_path,next_action,created_at,started_at,completed_at,notes`

Initialize `docs/computa-artifacts/execution-queue.md` as a short human-readable index of active queue items, dependency rules, blocked items, and safe next action.

Append `queue_initialized` to `activity-log.csv` when these files are created. Do not overwrite existing queues.

When a session is created, create session-local `execution-queue.csv` and `execution-queue.md` inside that session. Orchestration skills must use `computa-execution-queue` to expand child skills, campaigns, Super-Phases, phases, tasks, reviews, docs hooks, and closeout gates into these queues before executing them.

## Shared Indexes

Maintain `docs/computa-artifacts/artifact-index.md` as a concise map of active and recent sessions. Include each session path, layer, status, parent, current next action, and where a fresh agent should start.

Use `docs/computa-artifacts/shared/` only for evidence that truly spans sessions. Keep session-specific artifacts inside the session that produced them.

## Secrets Needed

Use `computa-secrets-needed` whenever any Export Control, 4D Chess, Computa, phase, task, or subtask needs an API key, OAuth client, webhook secret, model-provider key, dashboard credential, deployment secret, or other private configuration.

Record secret requirements in `docs/computa-artifacts/secrets-needed/`. Include target env paths, platform secret targets, code paths, what can be built with placeholders, what verification remains blocked, and a safe `@Computer` prompt for a future logged-in credential handoff. Never store actual secret values in artifacts, logs, terminal output, reports, screenshots, or git.

## Architecture Docs

Architecture docs live at `docs/architecture/`, as a sibling of `docs/computa-artifacts/`. Never place the actual architecture docs inside `docs/computa-artifacts/`.

Do not create architecture docs by default unless requested or invoked by a docs skill. If a docs skill is active, create `docs/architecture/` through `computa-docs-architecture-init`.

If `docs/architecture/` already exists, do not treat it as automatically true. Later Computa layers must read it first for orientation, then verify claims against the codebase.
