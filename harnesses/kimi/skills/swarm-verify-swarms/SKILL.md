---
name: swarm-verify-swarms
description: "Run required swarm reviews for swarm-verified work: after every task and phase, dispatch one adversarial reviewer per subtask or task, then one judge/verifier per matching reviewer, approve or reject findings, and only implement approved recommendations."
---

# Swarm Verify Swarms

Use this after every task and every phase, and after material plan changes.

## Required Dependency Skills

When this subskill is invoked directly, use or trigger all Kimi-compatible swarm-verify dependencies when available:

- `caveman`: terse, concrete communication.
- `using-superpowers`: start-of-task planning discipline.
- `writing-plans` and `executing-plans`: plan creation and execution.
- `test-driven-development`: fail-first implementation.
- `systematic-debugging` or `investigate`: root-cause investigation.
- `dispatching-parallel-agents` or Kimi agent swarm/delegation: safe swarm parallelism.
- `requesting-code-review`: adversarial review.
- `verification-before-completion`: completion proof.
- `playwright`: browser-visible runtime QA.
- `context7`: current, version-specific docs for libraries, frameworks, APIs, CLIs, and harness behavior.

If any dependency is missing, continue with equivalent behavior and record the missing dependency in the artifact ledger.

Use Kimi agent swarm/delegation, parallel agent dispatch, and adversarial review when available.

## Parallelism Guard

Run swarms only on non-overlapping review work.

Do not parallelize agents that might edit the same files, mutate shared data, change dashboards, share browser sessions, share test servers, or depend on each other's unfinished findings.

## Task-Level Swarm

At the end of every task, run two rounds.

Round 1: task adversarial swarm

- Run one adversarial-review agent per subtask.
- Each agent reviews its subtask, evidence, tests, code changes, edge cases, and unresolved risks.
- Each agent challenges missing edge cases, weak tests, false assumptions, regressions, security/privacy risks, bad sequencing, and incomplete QA.
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
- commit the completed task only if verification passes and commits are allowed

## Phase-Level Swarm

At the end of every phase, run two rounds.

Round 1: phase adversarial swarm

- Run one adversarial-review agent per task in the phase.
- Each agent reviews its task, subtasks, evidence, tests, code changes, edge cases, and unresolved risks.
- Each challenges whether the task satisfies phase acceptance criteria.
- Each checks for missing subtasks, bad sequencing, unresolved dependencies, untested edge cases, regressions, and incomplete runtime QA.
- Each outputs findings and recommended next actions.

Round 2: phase judge/verifier swarm

- Run one judge/verifier agent per task in the phase.
- Each judge/verifier reviews the matching adversarial findings.
- Classify findings as `correct`, `partly correct`, `wrong`, or `needs more evidence`.
- Decide whether the task is complete, needs rework, or is blocked.
- Do not close the phase until every task is approved complete, approved deferred, or blocked with evidence.

Before closing the phase:

- confirm all tasks/subtasks are complete or explicitly deferred
- run required phase verification
- update phase logs, issue ledgers, task ledgers, and master ledgers
- record the phase verdict

## Plan-Change Swarm

For material plan changes, run a focused adversarial reviewer and judge/verifier on the proposed change before implementation.

The review must check:

- why the old plan was insufficient
- dependency impact
- audit history preservation
- new risks or blockers
- whether the proposed new work is within the original user request
