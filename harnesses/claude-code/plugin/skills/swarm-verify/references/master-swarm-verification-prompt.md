# Master Swarm Verification Prompt

```md
compelete the task following the rules Rules: /caveman
/test-driven-development Before you do an action, justify it very briefly and adversarially review it. Use: - /caveman - /investigate. Independently verify the issues and their origins. Create test cases to verify the fix. Also do runtime QA on the actual functionality with real testing. Use this QA loop to solve the problem. Before you start, use /superpowers to create a plan and enact it. At every step of the loop, explore what you might be missing and challenge your assumptions. Do not assume. Verify.

# Task

<insert here>

This workflow can edit existing code, add functionality to an existing system, fix a Jira/task bug, or build a moderate project from scratch. For ultra-long autonomous projects use /computa-4d-chess. For massive research/strategy work that should decide what to build or what technologies to use before execution, use /computa-export-control. Export Control should produce `technical-spec/` before 4D campaign design when the work needs concrete engineering contracts, and `implementation-strategy/` before 4D when hard engineering issues, missing-key testability, migrations, provider integrations, concurrency/state risks, or rollout hazards could affect implementation. Existing-codebase Export Control should run the standalone audit suite (`security-audit`, `performance-audit`, and `ui-audit`) in documentation mode before final 4D campaign design. Every 4D Chess run must include final `SP-999-post-run-security-audit`, executed through `/computa-make-no-mistakes`, before marking the 4D session complete.

Prefer small, modular, readable components over gigantic files. Split by responsibility, keep APIs narrow, follow existing project boundaries, and avoid dumping unrelated behavior into one file.

# Dependency Invocation

Before starting the master workflow or any standalone phase/subskill, invoke or apply all available dependency capabilities:

- /caveman
- /computa-init if available
- /computa-speak immediately after raw request capture
- /computa-resume when recovering prior work from artifacts
- /computa-secrets-needed whenever API keys, OAuth credentials, webhook secrets, model-provider keys, deployment secrets, dashboard credentials, or private config are needed
- /computa-export-control-implementation-strategy before 4D campaigns when complex engineering challenges or missing-key testability need resolution
- /computa-make-no-mistakes-docs-update after every phase and during final closeout
- /security-audit inside final `SP-999-post-run-security-audit`, executed by `/computa-make-no-mistakes`, before 4D `session_completed`
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

All plan, phase, task, and subtask artifacts must live under `<invocation-root>/docs/computa-artifacts/`.

Run `computa-init` if available. Create `docs/` if missing. Create or reuse `docs/computa-artifacts/` in the invocation root. Use the explicit project/root path if the user provides one; otherwise use the current working directory, preferring the git top-level when invoked inside a git repo. If `docs/computa-artifacts/` is inside a git repo, add the correct relative path to `.gitignore` if missing. If not inside a git repo, no gitignore action is needed.

Architecture docs must live at `docs/architecture/`, as a sibling of `docs/computa-artifacts/`. Never put the actual architecture docs under `docs/computa-artifacts/`.

Initialize or update:
- `docs/computa-artifacts/artifact-index.md`
- `docs/computa-artifacts/session-ledger.csv`
- `docs/computa-artifacts/activity-log.csv`
- `docs/computa-artifacts/secrets-needed/`
- `docs/computa-artifacts/secrets-needed/index.md`
- `docs/computa-artifacts/secrets-needed/secrets-needed.csv`
- `docs/computa-artifacts/secrets-needed/computer-use-prompts/`
- `docs/computa-artifacts/export-control/`
- `docs/computa-artifacts/4d-chess/`
- `docs/computa-artifacts/computa/`
- `docs/computa-artifacts/shared/`

Create a new session for every invocation. Standalone Computa sessions use `docs/computa-artifacts/computa/CMN-YYYYMMDD-HHMMSS-slug/`. Computa sessions invoked by 4D Chess live under the parent 4D session at `.../computa/CMN-.../`. Every session must be registered in the root session ledger with its parent session ID when applicable.

Maintain `docs/computa-artifacts/activity-log.csv` as the root crash-recovery log with this header:

`timestamp,session_id,layer,parent_session_id,event_type,scope_type,scope_id,scope_name,status,artifact_path,evidence_path,next_action,notes`

Append rows as resumable units start, finish, block, defer, or materially change. Log sessions, Export Control campaigns, Export Control audit-suite tasks, 4D Super-Phases, 4D security audits, Computa phases, and Computa tasks. Do not log every subtask in this root CSV; subtask progress belongs in each task directory. Append `session_started` immediately when the session exists.

When any phase, task, subtask, Super-Phase, campaign, or research item needs an API key, OAuth credential, webhook secret, model-provider token, deployment secret, dashboard credential, or other private config, run `computa-secrets-needed` or equivalent immediately. Update `docs/computa-artifacts/secrets-needed/secrets-needed.csv`, create a per-secret Markdown file, create a safe `@Computer` handoff prompt, and append `secret_needed_added`, `secret_needed_updated`, `secret_configured`, or `secret_verification_blocked` to `activity-log.csv` as appropriate. Never store actual secret values in code, artifacts, logs, reports, screenshots, terminal output, or git.

Build as far as possible even when a secret is missing. Missing API keys or private config are a keyless-test-design problem, not a reason to stop. Use named env vars, placeholders, mocks, fakes, provider adapters, contract tests, fixture payloads, dry-run modes, feature guards, and missing-secret tests. Mark only runtime/deploy/platform verification that truly requires the credential as blocked.

Immediately after saving `user-task.md`, run `computa-speak` or equivalent. Save:
- `normalized-task.md`: concise AI-ready working prompt.
- `prompt-normalization-log.md`: spelling/wording fixes, preserved constraints, ambiguities, and confirmation that nothing substantive was dropped.

Downstream phases analyze `normalized-task.md` first and cross-check `user-task.md` whenever scope, permission, or acceptance criteria are in doubt.

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

Append `phase_started` to `activity-log.csv` before Phase 1 begins.

Phase 1 must:
- Audit the task and working codebase broadly enough to understand where you are working.
- If `docs/architecture/` exists, read it first for orientation, especially `README.md`, `ARCHITECTURE.md`, `AUDIT-REPORT.md`, and relevant module docs. Treat those docs as leads, then verify claims against source and mark stale, wrong, missing, or unknown docs.
- Create `maps/map-index.md` with every map file, what it covers, last update time, evidence paths, and where later phases should look first.
- Create `maps/architecture-docs-map.md` with docs files read, useful verified claims, stale/missing docs, and architecture-docs update needs.
- Create `maps/task-scope-map.md` with the original request, acceptance criteria, explicit constraints, in-scope/out-of-scope areas, assumptions, and unresolved questions.
- Create `maps/codebase-map.md` with repo roots, package/app boundaries, key modules, entrypoints, route/API surfaces, config files, generated/reference-only files, and relevant ownership boundaries.
- Create `maps/flow-map.md` with user, runtime, data, analytics, queue, network, database, deployment, or dashboard flows relevant to the task.
- Create `maps/test-and-command-map.md` with package manager, install/build/lint/test commands, existing tests, missing coverage, smoke/runtime commands, and Playwright/browser routes if relevant.
- Create `maps/risk-map.md` with risky files/systems, edge cases, migrations, external consoles, credentials/secrets boundaries, production-touching surfaces, race conditions, and assumptions to challenge.
- Create `maps/secrets-map.md` with required or possible API keys/private config, target env/platform paths, related code paths, owner actions, and verification blocked by missing credentials. State `none known` if no secrets are needed.
- Create `maps/modularity-map.md` with component/module boundaries, reusable helpers, files at risk of becoming too large, and recommended split points for readable implementation.
- Create `maps/map-change-log.md` and `maps/map-change-ledger.csv` before leaving Phase 1.
- Use fast structural reads first: branch/remotes, file inventory, package manifests, config files, routes, tests, docs, PR/ticket references, and runtime entrypoints.
- If the repo is huge, make the audit task-focused, but map adjacent systems that could regress and explicitly mark unexplored areas as unknown or likely irrelevant.
- Update maps whenever later evidence changes the working model. Maps may change at any time as implementation, tests, runtime QA, review swarms, or source-truth checks reveal new information.
- Track every material map change in both `maps/map-change-log.md` and `maps/map-change-ledger.csv`, like phase/task changes are tracked in Markdown and CSV ledgers.
- Update the phase, task, subtask, issue, and blocker ledgers with map evidence.
- Run the phase-level adversarial swarm and phase-level judge/verifier swarm before moving to the next phase.

# Phase 2: Investigation And Baseline

After the orientation map exists, run targeted investigation before implementation.

Append `phase_started` to `activity-log.csv` before Phase 2 begins.

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
- Append `phase_started`, `task_started`, `task_completed`, `phase_completed`, `phase_blocked`, `task_blocked`, or deferred equivalents to `activity-log.csv` as the work happens.
- Never start a task or subtask whose prerequisites are incomplete.
- Never run overlapping tasks in parallel if they touch the same files, systems, data, migrations, dashboard settings, deployment state, or test environment.
- Prefer small modular components and targeted files. If a task starts creating a giant file or mixed-responsibility module, split it into smaller components before continuing.
- If the task needs private config, update `docs/computa-artifacts/secrets-needed/` before implementation and keep the task moving with placeholders/mocks/fakes/provider adapters/contract tests/fixtures/dry-run modes/guards.

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
- Each agent must challenge avoidable giant files, mixed responsibilities, and poor component boundaries.
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
- Append `task_completed`, `task_blocked`, or `task_deferred` to `activity-log.csv` with evidence and next action.
- Commit the completed task if verification passes and commits are allowed.
- Only then proceed to the next task.

# Phase-Level Swarm Review

At the end of every phase, run a two-round phase swarm.

Before the phase swarm, run `computa-make-no-mistakes-docs-update` or equivalent. It must create `docs/architecture/`, update it, record a no-op, or document a blocker based on the phase ledgers and code truth. Do not close a phase with missing or stale docs-hook evidence.

Round 1: phase adversarial swarm
- Run one adversarial-review agent per task in the phase.
- Each agent reviews its assigned task, subtasks, evidence, tests, code changes, edge cases, and unresolved risks.
- Each agent must challenge whether the task truly satisfies the phase acceptance criteria.
- Each agent must check for missing subtasks, bad sequencing, unresolved dependencies, untested edge cases, regressions, and incomplete runtime QA.
- Each agent must check whether architecture docs were created, updated, no-op recorded, or blocked with evidence for this phase.
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
- Append `phase_completed`, `phase_blocked`, or `phase_deferred` to `activity-log.csv` with evidence and next action.
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
- Add missing-secret behavior tests when a feature depends on API keys or private config.
- For secret-dependent integrations, also test request construction, response parsing, validation, retries, error handling, synthetic webhook/event handling, provider adapter contracts, and missing/invalid credential paths without live credentials when possible.
- Keep implementations small, modular, and readable; test through narrow interfaces where possible.
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
- whether files/components stayed modular and readable
- what commands you ran
- what passed
- what failed
- what smoke tests you ran
- what `/playwright` checks you ran
- what you learned
- what assumptions changed
- what map files you referenced or updated
- what `map-change-log.md` and `map-change-ledger.csv` entries were added
- what secrets-needed entries were added or updated, and what verification remains blocked by missing private config
- what remains blocked or risky
- links or paths to evidence

Keep CSV ledgers current. Do not wait until the end to update them.

Keep `docs/computa-artifacts/activity-log.csv` current at the same time as local ledgers. It must be good enough for `/computa-resume` to identify the latest unfinished phase, task, Super-Phase, campaign, or session after a crash.

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
- Architecture docs status: created, updated, no-op, or blocked; exact docs paths; docs audit report path; and remaining docs gaps.
- Secrets-needed status: required private config, target env/platform paths, per-secret Markdown paths, safe `@Computer` prompt paths, configured/verified status, and any blocked runtime/deploy verification.
- A brief summary of what changed and why.
- Any remaining risks, blockers, or unverified assumptions.
- Paths to the plan, phase, task, subtask, issue, and evidence artifacts.
- Path to `docs/computa-artifacts/activity-log.csv`, confirmation it has the latest session/phase/task/security-audit status, and the latest resume point.
- A final `session_completed` or `session_blocked` row in `activity-log.csv` with the final report path and next action.

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
