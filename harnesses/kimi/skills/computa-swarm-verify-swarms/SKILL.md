---
name: computa-swarm-verify-swarms
description: "Run required swarm reviews for computa-swarm-verified work: after every task and phase, dispatch one adversarial reviewer per subtask or task, then one judge/verifier per matching reviewer, check evidence, modularity, giant-file risk, regressions, and only implement approved recommendations."
---

# Computa Swarm Verify Swarms

Use this after every task and every phase, and after material plan changes.

## Required Dependency Skills

When this subskill is invoked directly, use or trigger all computa-swarm-verify dependencies when available:

- `caveman`: terse, concrete communication.
- `using-superpowers`: start-of-task planning discipline.
- `writing-plans` and `executing-plans`: plan creation and execution.
- `test-driven-development`: fail-first implementation.
- `systematic-debugging` or `investigate`: root-cause investigation.
- native agent swarm/delegation: safe swarm parallelism.
- `requesting-code-review`: adversarial review.
- `verification-before-completion`: completion proof.
- `playwright`: browser-visible runtime QA.
- `context7`: current, version-specific docs for libraries, frameworks, APIs, CLIs, and harness behavior.

If any dependency is missing, continue with equivalent behavior and record the missing dependency in the artifact ledger.

Use native agent swarm/delegation and `requesting-code-review` when available.

## Parallelism Guard

Run swarms only on non-overlapping review work.

Do not parallelize agents that might edit the same files, mutate shared data, change dashboards, share browser sessions, share test servers, or depend on each other's unfinished findings.

## Task-Level Swarm

At the end of every task, run two rounds.

Round 1: task adversarial swarm

- Run one adversarial-review agent per subtask.
- Each agent reviews its subtask, evidence, tests, code changes, edge cases, and unresolved risks.
- Each agent challenges missing edge cases, weak tests, false assumptions, regressions, security/privacy risks, bad sequencing, and incomplete QA.
- Each agent checks whether the implementation stayed small, modular, readable, and aligned with existing boundaries instead of creating giant files.
- Each outputs findings and recommended next actions.

Round 2: task judge/verifier swarm

- Run one judge/verifier agent per subtask.
- Each judge/verifier reviews the matching adversarial agent's findings.
- Classify every finding as `correct`, `partly correct`, `wrong`, or `needs more evidence`.
- Approve, reject, or request evidence for each next action.
- Do not implement adversarial recommendations unless the matching judge/verifier approves them.

Before closing the task:

- confirm all subtasks are complete or explicitly deferred
- run required task verification
- update task logs, issue ledgers, subtask ledgers, and master ledgers
- append `task_completed`, `task_blocked`, or `task_deferred` to the root `docs/computa-artifacts/activity-log.csv` with the task evidence and next action
- commit the completed task only if verification passes and commits are allowed

## Phase-Level Swarm

At the end of every phase, run two rounds.

Before the phase-level swarm, run `computa-make-no-mistakes-docs-update` or verify that it already ran for this phase. The phase review must include whether architecture docs were created, updated, no-op recorded, or blocked with evidence.

Round 1: phase adversarial swarm

- Run one adversarial-review agent per task in the phase.
- Each agent reviews its task, subtasks, evidence, tests, code changes, edge cases, and unresolved risks.
- Each challenges whether the task satisfies phase acceptance criteria.
- Each checks for missing subtasks, bad sequencing, unresolved dependencies, untested edge cases, regressions, and incomplete runtime QA.
- Each checks whether the phase introduced avoidable monoliths, oversized files, or mixed responsibilities.
- Each checks whether the docs update hook reflected phase ledger work in `docs/architecture/`, or correctly recorded a no-op/blocker.
- Each outputs findings and recommended next actions.

Round 2: phase judge/verifier swarm

- Run one judge/verifier agent per task in the phase.
- Each judge/verifier reviews the matching adversarial findings.
- Classify findings as `correct`, `partly correct`, `wrong`, or `needs more evidence`.
- Decide whether the task is complete, needs rework, or is blocked.
- Do not close the phase until every task is approved complete, approved deferred, or blocked with evidence.
- Do not close the phase if the architecture-docs hook is missing, stale, or unsupported by evidence.

Before closing the phase:

- confirm all tasks/subtasks are complete or explicitly deferred
- run required phase verification
- update phase logs, issue ledgers, task ledgers, and master ledgers
- record the phase verdict
- append `phase_completed`, `phase_blocked`, or `phase_deferred` to the root `docs/computa-artifacts/activity-log.csv` with the phase evidence and next action

## Plan-Change Swarm

For material plan changes, run a focused adversarial reviewer and judge/verifier on the proposed change before implementation.

The review must check:

- why the old plan was insufficient
- dependency impact
- audit history preservation
- new risks or blockers
- whether the proposed new work is within the original user request
