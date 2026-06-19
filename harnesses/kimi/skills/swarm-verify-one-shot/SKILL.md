---
name: swarm-verify-one-shot
description: One-command entrypoint that invokes the complete swarm-verify suite for a task, including dependency skills, master orchestration, setup, investigation, TDD/runtime QA, swarms, and closeout. Use when the user wants the full workflow from one Kimi skill invocation.
---

# Swarm Verify One Shot

Use this as the single-command entrypoint. Treat the user's text after the skill name as the task.

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

## Invoke The Full Suite

Load and apply every swarm-verify skill in this order:

1. `swarm-verify`
2. `swarm-verify-setup`
3. `swarm-verify-investigate`
4. `swarm-verify-tdd-qa`
5. `swarm-verify-swarms`
6. `swarm-verify-closeout`

Do not skip a listed skill because this entrypoint is "one-shot". One-shot means the user invokes one skill; internally, the full suite still runs.

Also read `swarm-verify/references/master-swarm-verification-prompt.md` when present. It is the parity source. If a detail is present there and absent here, follow the reference unless the user explicitly overrides it.

## Execution Contract

Execute the task end to end under the complete swarm-verify rules:

- Before each meaningful action, briefly justify it and challenge why it might be wrong.
- Save the raw user request to `user-task.md` before rewriting, summarizing, or planning from memory.
- Keep all plan, phase, task, subtask, issue, blocker, evidence, map, and report artifacts outside the repo.
- Phase 0: create the artifact root, plan directory, `plan.md`, master task CSV, issue/blocker Markdown and CSV ledgers, phase directories, task directories, subtask ledgers, and reports directory.
- Phase 1: run a codebase/task orientation audit before implementation. Create reusable living maps for scope, codebase, flows, commands/tests, risks, unknowns, and out-of-scope areas.
- Keep maps current. Maps may change at any time when evidence changes; track each material update in both Markdown and CSV under `maps/`.
- Phase 2: investigate source truth, current behavior, expected behavior, issue origin, edge cases, baseline commands, and failing evidence before implementation.
- Split work into phases, tasks, and subtasks with explicit order and dependencies. Do not run dependent work before prerequisites are done.
- Use safe swarms for parallelism only. Do not parallelize overlapping files, systems, data, dashboards, databases, browsers, servers, deployments, migrations, queues, or dependent subtasks.
- For behavior changes, use TDD: failing test first, smallest fix, passing test after.
- Run relevant unit, integration, smoke, runtime, and Playwright/browser-visible QA. Solve discovered edge cases.
- After every task, run one adversarial reviewer per subtask, then one judge/verifier per subtask. Only implement judge-approved recommendations.
- After every phase, run one adversarial reviewer per task, then one judge/verifier per task. Do not close a phase until each task is approved complete, approved deferred, or blocked with evidence.
- Keep ledgers, logs, and evidence current as work happens.
- Make one descriptive commit per completed task only after verification passes and commits are allowed.
- Do not push unless explicitly asked.

## Plan Changes

You may add, remove, split, merge, or reorder phases, tasks, or subtasks when new evidence proves the current plan incomplete or wrong.

When changing the plan:

- justify the change briefly
- update all affected Markdown logs and CSV ledgers
- update dependencies
- preserve superseded history instead of deleting it
- run adversarial and judge/verifier review for material plan changes before implementing them

If a previous pass was wrong, state what was wrong, preserve the old evidence, add corrected evidence, update the verdict, and add regression tests or verification so the mistake is not repeated.

## Closeout Bar

Do not claim completion until `swarm-verify-closeout` has produced concise but substantive Markdown reports covering:

- what was done
- what still needs verification
- current blockers and open issues
- gaps between the original user request and completed work
- map artifacts and map-change coverage
- new issues found and fixed
- new issues found and not fixed
- exact verification commands and runtime QA evidence

Golden rule: evidence before assertions. Never say "it works" without verification command output and runtime proof.
