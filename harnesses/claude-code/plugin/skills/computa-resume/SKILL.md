---
name: computa-resume
description: Inspect docs/computa-artifacts logs and ledgers to resume the latest Computa Export Control, 4D Chess, Computa Make No Mistakes, phase, task, Super-Phase, or campaign after a crash or context loss. Use when the user asks to resume, continue previous Computa work, find the latest active session, recover from an interrupted run, or identify the next action from activity-log.csv.
---

# Computa Resume

Use this to recover work from artifacts, not chat memory. It is read-only by default unless the user asks to continue execution.

## Inputs

Start at the invocation root. If inside a git repo, prefer the git top-level. Look for:

- `docs/computa-artifacts/activity-log.csv`
- `docs/computa-artifacts/session-ledger.csv`
- `docs/computa-artifacts/artifact-index.md`
- `docs/computa-artifacts/secrets-needed/secrets-needed.csv`
- `docs/computa-artifacts/secrets-needed/` per-secret Markdown files and `computer-use-prompts/`
- active Export Control, 4D Chess, and Computa session directories
- session-local ledgers, reports, handoffs, blocker logs, and maps referenced by the latest rows

If multiple artifact roots are possible, inspect the nearest root first, then parent roots. Do not cross into unrelated projects unless the user asks.

## Activity Log Contract

Expect `docs/computa-artifacts/activity-log.csv` with:

`timestamp,session_id,layer,parent_session_id,event_type,scope_type,scope_id,scope_name,status,artifact_path,evidence_path,next_action,notes`

This root log tracks resumable units only:

- sessions
- Export Control campaigns
- Export Control audit-suite tasks
- 4D Super-Phases
- 4D final security Super-Phase and nested security audits
- Computa phases
- Computa tasks
- research tasks and strategic design milestones
- cross-layer secret/private-config events

Do not expect subtask rows in the root log. For subtask progress, open the task directory referenced by the latest task event and read `subtask-ledger.csv`.

## Resume Procedure

1. Confirm the artifact root and read `session-ledger.csv`.
2. Read `activity-log.csv`, sorted by timestamp as recorded.
3. Read `secrets-needed/secrets-needed.csv` when present so missing private config, safe `@Computer` prompts, and blocked verification are visible before resuming.
4. Identify the latest active top-level session: a session with `session_started` and no matching `session_completed` or `session_blocked`, or the most recent blocked/deferred session if nothing is active.
5. Walk into nested children through `parent_session_id` to find the deepest active work item.
6. Prefer unfinished rows in this order: active task, active phase, active Computa session, active Super-Phase including `SP-999-post-run-security-audit`, active nested 4D security audit, active 4D session, active campaign, active Export Control audit suite, active Export Control session.
7. Open the referenced `artifact_path`, then read the relevant local ledger:
   - task: `task.md`, `task-log.md`, `subtask-ledger.csv`, task issues/blockers
   - phase: `phase.md`, `phase-task-ledger.csv`, phase issues/blockers
   - Computa session: `plan.md`, `master-task-ledger.csv`, `maps/`, `reports/`
   - Super-Phase: `super-phase.md`, `super-phase-ledger.csv`, `handoff.md`, nested Computa link
   - 4D final security Super-Phase: `super-phases/SP-999-post-run-security-audit/super-phase.md`, `computa-invocation.md`, nested Computa link, `security-audit/invocation.md`, `security-audit/security-audit-ledger.csv`, `.claude/vibecoder/security-<4d-session-id-or-slug>-progress.md`
   - 4D session: `super-phases/super-phase-ledger.csv`, `super-phases/handoff-index.md`, `reports/`
   - campaign: `campaigns/campaign-ledger.csv`, campaign prompt, child 4D link
   - Export Control audit suite: `standalone-audits/audit-suite-ledger.csv`, `standalone-audits/remediation-backlog.csv`, category audit directories, `standalone-audits/implementation-campaign-map.md`
   - Export Control session: `research-agenda.md`, `decision-matrix.md`, `campaigns/`, `reports/`
8. Check whether the latest item is genuinely incomplete, blocked, or complete-but-unclosed by comparing local ledgers and evidence paths.
9. Produce a concise resume report before executing anything.

## Resume Report

Write a report under `docs/computa-artifacts/resume/RESUME-YYYYMMDD-HHMMSS.md` when filesystem writes are allowed. If not, report in chat.

Include:

- artifact root
- latest top-level session and latest nested session
- current layer: export-control, export-control-audit-suite, 4d-chess, final-security-super-phase, nested-security-audit, computa, phase, task, or subtask context
- latest activity-log row
- current secrets-needed status, including whether missing API keys/private config block runtime/deploy verification and which safe `@Computer` prompt to use
- local ledgers opened
- inferred current status
- exact next action from the log or ledger
- exact skill to invoke next, such as `/computa-export-control`, `/computa-4d-chess`, or `/computa-make-no-mistakes`
- whether it is safe to resume automatically
- blockers, missing evidence, or ambiguous state
- files a fresh agent should read first

## Execution Policy

- If the user only asks "what was I working on" or "where do we resume", do not execute the task. Produce the resume report and stop.
- If the user asks to resume execution, continue from the deepest safe incomplete unit using the correct skill and artifact path.
- If the activity log and local ledgers conflict, trust concrete evidence and local ledgers over the last log row, then append a resume note only if execution is authorized.
- If the latest state is ambiguous, ask the smallest blocking question or present the safest resume options.
- Never mark work complete just because a log row says completed. Verify the corresponding evidence path and local ledger status.
- Never push, deploy, publish dashboard changes, or mutate external systems as part of resume unless the resumed task explicitly permits it.

Golden rule: artifacts are source truth; chat context is disposable.
