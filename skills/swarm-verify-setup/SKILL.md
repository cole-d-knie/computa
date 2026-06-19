---
name: swarm-verify-setup
description: "Create Phase 0 setup artifacts for swarm-verified work: external plan directory, raw user-task capture, phase/task/subtask ledgers, dependency order, issue ledgers, evidence paths, and audit logs. Use when starting any swarm-verify task or when planning artifacts must be auditable outside the repo."
---

# Swarm Verify Setup

Use this for Phase 0. Finish it before implementation.

## Artifact Root

Create an artifact root outside the repo. Use a stable, timestamped path that names the task.

Immediately create `user-task.md` in that root before summarizing or planning. Include:

- raw user request
- timestamp
- invocation text or skill name
- repo/path and base branch, if known
- explicit permissions, exclusions, and do-not-touch constraints
- initial assumptions
- ambiguities and user input still needed

If the task is ambiguous, still save `user-task.md`, log the ambiguity, and ask only questions that truly block safe work.

## Plan Directory

Create a plan directory with:

- `plan.md`: phases, assumptions, scope, risks, edge cases, success criteria, verification strategy.
- `master-task-ledger.csv`: every phase, task, and subtask in execution order with status, dependencies, owner/agent, evidence path, and next action.
- `issues-and-blockers.md`: narrative log of issues, blockers, assumptions, edge cases, decisions, and plan changes.
- `issues-and-blockers.csv`: structured tracker with issue ID, severity, owner, status, dependency, and resolution.
- `reports/`: final report directory for closeout.

## Phase Directories

Split the work into multiple phases. Phase 0 is setup. Phase 1 is investigation and baseline. Later phases should reflect the task.

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
- Mark rows done only after evidence exists.
- Preserve superseded plans and old evidence; do not delete audit history.
- Add new phases, tasks, or subtasks when evidence shows the plan is incomplete.
- Justify every plan change and update affected dependencies.
- Keep artifacts outside the repo unless the user explicitly asks otherwise.
