---
name: swarm-verify
description: Execute a task with phased planning, raw task capture, external audit ledgers, TDD, investigation, runtime QA, Playwright checks, and two-round adversarial plus judge/verifier swarms after every task and phase. Use for requests like swarm verification loop, phase/task swarms, audit-ready implementation, or getting work ready to merge with strict evidence.
---

# Swarm Verify

Use this as the master orchestrator. Treat the user's text after the skill name as the task.

If the task is missing or too vague to test, ask only for the blocking objective, expected behavior, and repo/path. Otherwise start.

## Required Dependency Skills

Use or trigger these when available:

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

## Load Order

Read and apply these sub-skills in order:

1. `swarm-verify-setup`
2. `swarm-verify-investigate`
3. `swarm-verify-tdd-qa`
4. `swarm-verify-swarms`
5. `swarm-verify-closeout`

Also read `references/master-swarm-verification-prompt.md` when present. It is the parity source. If a detail is present there and absent here, follow the reference unless the user explicitly overrides it.

## Global Rules

- Before each meaningful action, briefly justify it and challenge why it might be wrong.
- Do not assume. Verify from source files, docs, PRs, tests, logs, dashboards, or runtime behavior.
- Save the raw user request to `user-task.md` before rewriting, summarizing, or planning from memory.
- Keep all plan, phase, task, subtask, issue, blocker, evidence, and report artifacts outside the repo.
- Use ledgers as the source of truth for order, dependencies, status, and evidence.
- Do phases, tasks, and subtasks only after prerequisites are complete.
- Use swarms for safe parallelism only. Do not parallelize overlapping files, systems, data, migrations, dashboards, deployment state, browsers, databases, queues, or test environments.
- Run TDD for behavior changes: failing test first, minimal fix, passing test after.
- Run runtime QA on actual functionality, not only static review.
- Use `playwright` for browser-visible behavior.
- Solve edge cases discovered during investigation.
- Keep audit logs current. Do not reconstruct them only at the end.
- Make one commit per completed task only after verification passes and commits are allowed.
- Do not push unless explicitly asked.

## Execution Flow

1. Phase 0: use `swarm-verify-setup` to create artifacts, preserve the raw request, split phases/tasks/subtasks, and initialize ledgers.
2. Phase 1: use `swarm-verify-investigate` to establish baseline truth, reproduce the issue or prove the gap, identify expected behavior, and create failing evidence.
3. Implementation phases: use `swarm-verify-tdd-qa` for test-first changes, smallest fixes, edge cases, unit/integration/smoke/runtime QA, and Playwright verification.
4. After every task and phase: use `swarm-verify-swarms` for adversarial review followed by judge/verifier review. Do not implement adversarial recommendations unless the matching judge/verifier approves.
5. Closeout: use `swarm-verify-closeout` to reconcile ledgers, create final reports, compare against `user-task.md`, record new fixed/unfixed issues, verify evidence, and state remaining gaps.

## Plan Changes

You may add, remove, split, merge, or reorder phases, tasks, or subtasks when new evidence proves the current plan incomplete or wrong.

When changing the plan:

- justify the change briefly
- update all affected markdown logs and CSV ledgers
- update dependencies
- preserve superseded history instead of deleting it
- run adversarial and judge/verifier review for material plan changes before implementing them

If a previous pass was wrong, state what was wrong, preserve the old evidence, add corrected evidence, update the verdict, and add regression tests or verification so the mistake is not repeated.

## Completion Bar

Do not claim completion unless there is evidence for:

- original user request captured in `user-task.md`
- phases/tasks/subtasks completed or explicitly deferred with rationale
- failing-before evidence or documented reason it was impossible
- passing-after evidence
- relevant unit, integration, smoke, runtime, and Playwright checks
- adversarial and judge/verifier swarms after each task and phase
- final reports with gaps, blockers, verification needs, and new fixed/unfixed issues

Golden rule: evidence before assertions. Never say "it works" without verification command output and runtime proof.
