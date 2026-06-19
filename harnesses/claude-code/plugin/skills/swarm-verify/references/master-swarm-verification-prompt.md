# Master Swarm Verification Prompt

```md
compelete the task following the rules Rules: /caveman
/test-driven-development Before you do an action, justify it very briefly and adversarially review it. Use: - /caveman - /investigate. Independently verify the issues and their origins. Create test cases to verify the fix. Also do runtime QA on the actual functionality with real testing. Use this QA loop to solve the problem. Before you start, use /superpowers to create a plan and enact it. At every step of the loop, explore what you might be missing and challenge your assumptions. Do not assume. Verify.

# Task

<insert here>

# Dependency Invocation

Before starting the master workflow or any standalone phase/subskill, invoke or apply all available dependency capabilities:

- /caveman
- /superpowers or `using-superpowers`
- `writing-plans` and `executing-plans`
- /test-driven-development
- /investigate or `systematic-debugging`
- `dispatching-parallel-agents`
- `subagent-driven-development` where compatible, or native agent swarm/delegation where not
- `requesting-code-review`
- `verification-before-completion`
- /playwright for browser-visible runtime QA
- `context7` for current library, framework, API, CLI, or harness docs

If any dependency is unavailable, continue with equivalent behavior and record the missing dependency in the artifact ledger.

# Phase 0: Setup And Planning

First, create a plan to solve the problem in multiple phases.

Phase 0 is setup: phase and task creation. In this phase, split the task into several phases.

All plan, phase, task, and subtask artifacts must live outside of the repo.

Create a plan directory with:
- `plan.md`: overall plan, assumptions, scope, risks, edge cases, and success criteria.
- `master-task-ledger.csv`: all phases/tasks/subtasks in execution order, with status, owner/agent, dependencies, evidence path, and next action.
- `issues-and-blockers.md`: narrative log of issues, blockers, assumptions, edge cases, and decisions.
- `issues-and-blockers.csv`: structured tracker for issue ID, severity, owner, status, dependency, and resolution.
- `maps/`: living codebase/task maps that future phases can reference instead of guessing from chat context.
  - `map-change-log.md`: narrative map update log.
  - `map-change-ledger.csv`: structured tracker with change ID, timestamp, phase, task, subtask, map file, reason, evidence path, before/after summary, and status.

For each phase directory, create:
- `phase.md`: phase goal, instructions, acceptance criteria, edge cases, and verification required.
- `phase-task-ledger.csv`: all tasks in that phase, order, dependencies, status, evidence path, and next action.
- `issues-and-blockers.md`: phase-specific issues, blockers, and edge cases.
- `issues-and-blockers.csv`: structured phase issue tracker.

For each task, create a subdirectory with:
- `task.md`: task goal, scope, instructions, acceptance criteria, edge cases, and verification.
- `task-log.md`: what changed, what was tried, what worked, what failed, and evidence.
- `subtask-ledger.csv`: all subtasks, status, dependencies, evidence path, and completion notes.
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

For every phase, task, and subtask:
- Log what you did.
- Log what changed.
- Log what worked and what did not.
- Log verification evidence.
- Mark ledger rows done only after evidence exists.
- Keep artifacts auditable and current.

# Phase 1: Orientation Audit And Map

After Phase 0, run Phase 1 before implementation.

Phase 1 must:
- Audit the task and working codebase broadly enough to understand where you are working.
- Create `maps/map-index.md` with every map file, what it covers, last update time, evidence paths, and where later phases should look first.
- Create `maps/task-scope-map.md` with the original request, acceptance criteria, explicit constraints, in-scope/out-of-scope areas, assumptions, and unresolved questions.
- Create `maps/codebase-map.md` with repo roots, package/app boundaries, key modules, entrypoints, route/API surfaces, config files, generated/reference-only files, and relevant ownership boundaries.
- Create `maps/flow-map.md` with user, runtime, data, analytics, queue, network, database, deployment, or dashboard flows relevant to the task.
- Create `maps/test-and-command-map.md` with package manager, install/build/lint/test commands, existing tests, missing coverage, smoke/runtime commands, and Playwright/browser routes if relevant.
- Create `maps/risk-map.md` with risky files/systems, edge cases, migrations, external consoles, credentials/secrets boundaries, production-touching surfaces, race conditions, and assumptions to challenge.
- Create `maps/map-change-log.md` and `maps/map-change-ledger.csv` before leaving Phase 1.
- Use fast structural reads first: branch/remotes, file inventory, package manifests, config files, routes, tests, docs, PR/ticket references, and runtime entrypoints.
- If the repo is huge, make the audit task-focused, but map adjacent systems that could regress and explicitly mark unexplored areas as unknown or likely irrelevant.
- Update maps whenever later evidence changes the working model. Maps may change at any time as implementation, tests, runtime QA, review swarms, or source-truth checks reveal new information.
- Track every material map change in both `maps/map-change-log.md` and `maps/map-change-ledger.csv`, like phase/task changes are tracked in Markdown and CSV ledgers.
- Update the phase, task, subtask, issue, and blocker ledgers with map evidence.
- Run the phase-level adversarial swarm and phase-level judge/verifier swarm before moving to the next phase.

# Phase 2: Investigation And Baseline

After the orientation map exists, run targeted investigation before implementation.

Phase 2 must:
- Read the relevant files, docs, tickets, PRs, logs, dashboards, or other source-of-truth materials.
- Reference the maps created in Phase 1 and update them when new evidence changes the working model.
- Identify the existing behavior.
- Identify the expected behavior.
- Identify likely edge cases.
- Identify current tests and coverage gaps.
- Run baseline verification commands before changing code.
- Reproduce the issue or prove the current gap.
- Create the first failing tests or document why a failing pre-fix test is not possible.
- Update the phase, task, subtask, issue, and blocker ledgers with findings.
- Run the phase-level adversarial swarm and phase-level judge/verifier swarm before moving to the next phase.

# Phase Execution Rules

After Phase 2, execute the remaining phases, tasks, and subtasks you created.

Follow the ledgers as the source of truth:
- Do phases in dependency order.
- Do tasks in dependency order.
- Do subtasks in dependency order.
- Never start a task or subtask whose prerequisites are incomplete.
- Never run overlapping tasks in parallel if they touch the same files, systems, data, migrations, dashboard settings, deployment state, or test environment.

Use agent swarms to increase parallelism where safe:
- Parallelize independent investigation tasks.
- Parallelize independent test-writing tasks.
- Parallelize independent review tasks.
- Parallelize independent code-reading tasks.
- Do not parallelize tasks that may edit the same files.
- Do not parallelize tasks where one result affects another task's scope.
- Do not parallelize runtime QA that depends on a shared server/session unless isolated environments are created.

You may add, remove, split, merge, or reorder phases, tasks, or subtasks when new information proves the existing plan is incomplete or wrong. If you do this:
- Justify the change briefly.
- Record what changed in the relevant markdown log.
- Update every affected CSV ledger.
- If the change affects the working map, update the relevant map plus `maps/map-change-log.md` and `maps/map-change-ledger.csv`.
- Update dependencies.
- Mark superseded tasks clearly instead of deleting audit history.
- Run adversarial review and judge/verifier review for material plan changes before implementing them.

If a previous pass was incorrect:
- Say exactly what was wrong.
- Preserve the old evidence.
- Add corrected evidence.
- Update the verdict.
- Add regression tests or verification steps so the mistake is not repeated.

# Task-Level Swarm Review

At the end of every task, run a two-round task swarm.

Round 1: task adversarial swarm
- Run one adversarial-review agent per subtask.
- Each agent reviews its assigned subtask, evidence, tests, code changes, edge cases, and unresolved risks.
- Each agent must challenge missing edge cases, weak tests, false assumptions, regressions, security/privacy risks, and incomplete QA.
- Each agent outputs findings and recommended next actions.

Round 2: task judge/verifier swarm
- Run one judge/verifier agent per subtask.
- Each judge/verifier reviews the matching adversarial agent's findings.
- Each judge/verifier must classify every finding as: correct, partly correct, wrong, or needs more evidence.
- Each judge/verifier must approve the next action, reject it, or request more evidence.
- Do not implement any adversarial recommendation unless the matching judge/verifier approves it.

Before closing the task:
- Confirm all subtasks are complete or explicitly deferred.
- Run required task verification.
- Update task logs, issue ledgers, subtask ledgers, and master ledgers.
- Commit the completed task if verification passes and commits are allowed.
- Only then proceed to the next task.

# Phase-Level Swarm Review

At the end of every phase, run a two-round phase swarm.

Round 1: phase adversarial swarm
- Run one adversarial-review agent per task in the phase.
- Each agent reviews its assigned task, subtasks, evidence, tests, code changes, edge cases, and unresolved risks.
- Each agent must challenge whether the task truly satisfies the phase acceptance criteria.
- Each agent must check for missing subtasks, bad sequencing, unresolved dependencies, untested edge cases, regressions, and incomplete runtime QA.
- Each agent outputs findings and recommended next actions.

Round 2: phase judge/verifier swarm
- Run one judge/verifier agent per task in the phase.
- Each judge/verifier reviews the matching adversarial agent's findings.
- Each judge/verifier must classify every finding as: correct, partly correct, wrong, or needs more evidence.
- Each judge/verifier must decide whether the task is complete, needs rework, or is blocked.
- Do not close the phase until every task's judge/verifier approves completion, approves deferral, or marks the task blocked with evidence.

Before closing the phase:
- Confirm all tasks/subtasks are complete or explicitly deferred.
- Run required phase verification.
- Update phase logs, issue ledgers, task ledgers, and master ledgers.
- Record the phase verdict.
- Only then proceed to the next phase.

# Testing Expectations

We expect:
- unit tests
- integration tests where appropriate
- smoke tests
- real runtime QA
- `/playwright` usage for browser-visible behavior
- test cases written ahead of implementation
- failing tests that reproduce the issue before the fix
- passing tests after the fix
- explicit edge case coverage

Before implementation:
- Identify expected behavior.
- Identify failure behavior.
- Write test cases that prove the bug or missing behavior.
- Run the tests and confirm they fail for the right reason.
- Document the failing output.

After implementation:
- Re-run the same tests and confirm they pass.
- Add edge-case tests for boundary conditions, invalid inputs, race conditions, permissions, empty states, loading states, retries, duplicate actions, and regression-prone flows.
- Run smoke tests against the real app or service.
- Use `/playwright` for real-time browser verification when UI/browser behavior is involved.
- Capture evidence: command output, logs, screenshots, network observations, or browser state.

Do not claim a fix is complete unless tests fail before the fix and pass after the fix, or unless you document why a pre-fix failing test is not possible.

# Verification Loop

Use this loop for every code change. Do not skip steps.

## 1. Understand Before Changing

- Read `maps/map-index.md` and the task-relevant map files.
- Read the relevant files.
- Identify the existing tests for the area you are changing.
- Identify likely edge cases before coding.
- If no tests exist and you are adding or fixing behavior, add a test first.

## 2. Test-Driven / Evidence-First

- Before writing implementation code, make the test fail or confirm the bug reproduces.
- Write the smallest implementation change that makes the test pass.
- Solve edge cases, not only the happy path.
- Do not over-engineer.

## 3. Run Verification After Every Meaningful Change

Run these in order and do not proceed until they pass:

```bash
pnpm check
pnpm build
pnpm test
pnpm lint
```

If the repo uses different commands, identify the equivalent commands first, document them, and run those instead.

If any step fails:
- Read the error.
- Fix the root cause.
- Re-run verification.
- Do not move on with a failing suite.

## 4. Manual / Live Checks When Relevant

- If you changed an API, hit the endpoint.
- If you changed a UI/dashboard, start the service and smoke-test the route.
- If you changed docs/PDFs, open the rendered output and verify.
- If behavior is browser-visible, use `/playwright` for runtime QA with real browser interaction, logs, console/network checks, screenshots, and visible state checks.

# Auditability Requirements

For every phase, task, and subtask, record:
- what you did
- what files or systems you inspected
- what files or systems you changed
- what tests you added or changed
- what edge cases you covered
- what commands you ran
- what passed
- what failed
- what smoke tests you ran
- what `/playwright` checks you ran
- what you learned
- what assumptions changed
- what map files you referenced or updated
- what `map-change-log.md` and `map-change-ledger.csv` entries were added
- what remains blocked or risky
- links or paths to evidence

Keep CSV ledgers current. Do not wait until the end to update them.

# Before Claiming Done

You must provide:
- The exact verification commands you ran.
- The output showing they passed.
- The failing test evidence from before implementation.
- The passing test evidence from after implementation.
- The smoke tests and runtime/manual QA performed.
- The `/playwright` verification performed, if applicable.
- The edge cases covered.
- The map artifacts created and any important map updates made during implementation.
- The map change log and map change ledger paths, with a statement that all material map changes were tracked.
- A brief summary of what changed and why.
- Any remaining risks, blockers, or unverified assumptions.
- Paths to the plan, phase, task, subtask, issue, and evidence artifacts.

# Commits And Pushes

- Make a separate commit for each completed task.
- Commit only after task verification passes.
- Each commit should be descriptive but concise.
- Use Conventional Commits: `type(scope): subject`.
- Keep subject <= 50 chars.
- Use caveman style: body only if the why is not obvious.
- Do not run `git push` unless explicitly asked.

# Golden Rule

Evidence before assertions. Never say "it works" without showing the verification command output and runtime proof.
```
