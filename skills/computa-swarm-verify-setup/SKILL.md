---
name: computa-swarm-verify-setup
description: "Create Phase 0 setup artifacts for computa-swarm-verified work under computa-artifacts: project-local artifact root, gitignore handling, raw user-task capture, session ledgers, phase/task/subtask ledgers, dependency order, issue ledgers, evidence paths, modular component boundaries, and audit logs. Use when starting debugging/implementation tasks with small-medium scope, code edit, system addition, or moderate build-from-scratch task."
---

# Computa Swarm Verify Setup

Use this for Phase 0. Finish it before implementation.

## Required Dependency Skills

When this subskill is invoked directly, use or trigger all computa-swarm-verify dependencies when available:

- `computa-init`: project-local `docs/` and `docs/computa-artifacts/` initialization.
- `computa-speak`: prompt normalization after raw task capture.
- `computa-resume`: recover existing activity-log state when setup is invoked to continue a crashed session.
- `computa-secrets-needed`: root secret-requirement ledger and safe credential handoff prompt creation.
- `caveman`: terse, concrete communication.
- `using-superpowers`: start-of-task planning discipline.
- `writing-plans` and `executing-plans`: plan creation and execution.
- `test-driven-development`: fail-first implementation.
- `systematic-debugging` or `investigate`: root-cause investigation.
- `dispatching-parallel-agents` and `subagent-driven-development`: safe swarm parallelism.
- `requesting-code-review`: adversarial review.
- `verification-before-completion`: completion proof.
- `playwright`: browser-visible runtime QA.
- `context7`: current, version-specific docs for libraries, frameworks, APIs, CLIs, and harness behavior.

If any dependency is missing, continue with equivalent behavior and record the missing dependency in the artifact ledger.

## Artifact Root

Run `computa-init` when available. Create `docs/` if missing, then create or reuse `docs/computa-artifacts/` in the invocation root.

Invocation root rules:

- Use the explicit project/root path if the user gives one.
- Otherwise use the current working directory where the skill is invoked.
- If invoked from inside a git repo and no separate root is explicit, prefer the git top-level so one project has one artifact root.
- If the invocation root is inside a git repo, ensure the repo ignores the artifact directory. Add the relative path, such as `/docs/computa-artifacts/` or `/subdir/docs/computa-artifacts/`, to `.gitignore` if it is missing. Do not duplicate entries.
- If not inside a git repo, still create `docs/computa-artifacts/`; no gitignore action is needed.

Initialize or update:

- `docs/computa-artifacts/artifact-index.md`: what sessions exist and how to find current work.
- `docs/computa-artifacts/session-ledger.csv`: session_id, layer, parent_session_id, status, invocation_root, session_path, user_task_path, started_at, completed_at, task_slug, summary_path, next_action.
- `docs/computa-artifacts/activity-log.csv`: timestamped root resume log for sessions, campaigns, Super-Phases, phases, and tasks.
- `docs/computa-artifacts/secrets-needed/`: shared secret/API-key/private-config requirement ledger, per-secret Markdown files, and safe `@Computer` credential handoff prompts.
- `docs/computa-artifacts/export-control/`: standalone Export Control sessions.
- `docs/computa-artifacts/4d-chess/`: standalone 4D Chess sessions.
- `docs/computa-artifacts/computa/`: standalone Computa Make No Mistakes sessions.
- `docs/computa-artifacts/shared/`: optional shared evidence, source snapshots, or cross-session references.

Actual architecture docs belong in `docs/architecture/`, as a sibling of `docs/computa-artifacts/`. Do not create architecture docs inside `docs/computa-artifacts/`.

Create a new session directory for every invocation. Never overwrite an old session.

Session IDs:

- Export Control: `EC-YYYYMMDD-HHMMSS-slug`
- 4D Chess: `4D-YYYYMMDD-HHMMSS-slug`
- Computa Make No Mistakes: `CMN-YYYYMMDD-HHMMSS-slug`

Standalone Computa sessions live at `docs/computa-artifacts/computa/CMN-.../`.
If invoked by 4D Chess, Computa sessions live under the parent 4D session at `.../computa/CMN-.../`.
If invoked by Export Control through 4D Chess, Computa sessions live under the nested 4D session.
Every session, standalone or nested, must also be registered in `docs/computa-artifacts/session-ledger.csv` with its parent session ID when applicable.

Append a `session_started` row to `docs/computa-artifacts/activity-log.csv` immediately after the session directory exists.

Activity log header:

`timestamp,session_id,layer,parent_session_id,event_type,scope_type,scope_id,scope_name,status,artifact_path,evidence_path,next_action,notes`

Use this root CSV for resumable units only: sessions, Export Control campaigns, 4D Super-Phases, Computa phases, and Computa tasks. Do not log every subtask here; subtask progress belongs in the task-level `subtask-ledger.csv`.

Immediately create `user-task.md` in the session directory before summarizing or planning. Include:

- raw user request
- timestamp
- invocation text or skill name
- invocation root, repo/path, base branch, and parent session ID if known
- explicit permissions, exclusions, and do-not-touch constraints
- initial assumptions
- ambiguities and user input still needed

If the task is ambiguous, still save `user-task.md`, log the ambiguity, and ask only questions that truly block safe work.

After `user-task.md` exists, run `computa-speak` before any substantive planning, investigation, architecture design, or implementation. Save its output as `normalized-task.md` and `prompt-normalization-log.md` in the same session.

## Plan Directory

Create a plan directory with:

- `plan.md`: phases, assumptions, scope, risks, edge cases, success criteria, verification strategy.
- `master-task-ledger.csv`: every phase, task, and subtask in execution order with status, dependencies, owner/agent, evidence path, and next action.
- `issues-and-blockers.md`: narrative log of issues, blockers, assumptions, edge cases, decisions, and plan changes.
- `issues-and-blockers.csv`: structured tracker with issue ID, severity, owner, status, dependency, and resolution.
- `maps/`: living codebase/task maps created during Phase 1 and updated whenever later evidence changes the working model.
- `reports/`: final report directory for closeout.

When implementation is expected, include a modularity note in `plan.md`: which components/modules should exist, which existing modules should be reused, what files must not become catch-alls, and how the task will avoid giant files.

When any planned work may need API keys, OAuth credentials, webhook secrets, model-provider tokens, deployment secrets, dashboard credentials, or private config, include a secrets note in `plan.md` and use `computa-secrets-needed` before implementation. Plan to build with env var names, placeholders, mocks, fakes, provider adapters, contract tests, fixtures, dry-run modes, and missing-secret tests, while clearly marking only live-credential runtime/deploy verification blocked by missing private config.

## Map Directory

Initialize `maps/` during Phase 0 so Phase 1 can fill it before implementation.

Expected map artifacts:

- `map-index.md`: what maps exist, when they were last updated, and which phase/task last relied on them.
- `task-scope-map.md`: original request, explicit constraints, in-scope/out-of-scope areas, acceptance criteria, and unknowns.
- `codebase-map.md`: repo layout, important packages/modules, ownership boundaries, entrypoints, relevant files, generated files, and do-not-edit/reference-only areas.
- `flow-map.md`: runtime/user/data/control flows related to the task, with source files and external systems.
- `test-and-command-map.md`: package manager, test/build/lint commands, smoke/runtime commands, existing tests, gaps, and expected verification order.
- `risk-map.md`: risky areas, edge cases, dependencies, migrations, dashboards, credentials, production-touching surfaces, and assumptions to challenge.
- `secrets-map.md`: private config and API keys needed or possibly needed, related code paths, env files/platform targets, and verification blocked by missing secrets. If no secrets are needed, record that.
- `map-change-log.md`: narrative log of every map update, why it changed, what evidence caused it, and which task/phase used the updated map.
- `map-change-ledger.csv`: structured tracker with change ID, timestamp, phase, task, subtask, map file, reason, evidence path, before/after summary, and status.

Keep maps concise but complete enough that a fresh agent can resume without guessing from chat context.

Maps are living artifacts. They may change at any time when implementation, tests, runtime QA, review swarms, or new source evidence changes the working model. Track every map change in both `map-change-log.md` and `map-change-ledger.csv`, the same way phase/task work is tracked in Markdown and CSV ledgers.

## Phase Directories

Split the work into multiple phases. Phase 0 is setup. Phase 1 is orientation audit and map creation. Phase 2 is investigation and baseline. Later phases should reflect the task.

For each phase directory, create:

- `phase.md`: goal, instructions, acceptance criteria, edge cases, and verification required.
- `phase-task-ledger.csv`: phase tasks in order with dependencies, status, evidence path, owner/agent, and next action.
- `issues-and-blockers.md`: phase-specific issues, blockers, assumptions, and edge cases.
- `issues-and-blockers.csv`: structured phase issue tracker.

## Task Directories

For each task, create a task subdirectory with:

- `task.md`: goal, scope, instructions, acceptance criteria, edge cases, dependencies, and verification.
- `task-log.md`: what changed, what was tried, what worked, what failed, and evidence.
- `subtask-ledger.csv`: subtasks with status, dependencies, evidence path, and completion notes.
- `issues-and-blockers.md`: task-specific issues, blockers, and edge cases.
- `issues-and-blockers.csv`: structured task issue tracker.

For each subtask, create a subdirectory or ledger row with:

- clear description
- expected outcome
- dependencies
- edge cases to cover
- completion status
- evidence path
- issues encountered
- verification performed

## Ledger Rules

- Log every phase, task, and subtask.
- In addition to local ledgers, append `phase_started`, `task_started`, `task_completed`, `phase_completed`, `phase_blocked`, `session_completed`, and `session_blocked` rows to the root `docs/computa-artifacts/activity-log.csv` as those events happen.
- Mark rows done only after evidence exists.
- Preserve superseded plans and old evidence; do not delete audit history.
- Add new phases, tasks, or subtasks when evidence shows the plan is incomplete.
- Justify every plan change and update affected dependencies.
- Keep artifacts under `docs/computa-artifacts/`. If this directory is inside a git repo, keep it gitignored unless the user explicitly asks to track artifacts.
