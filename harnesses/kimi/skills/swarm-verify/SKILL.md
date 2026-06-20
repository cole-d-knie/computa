---
name: swarm-verify
description: Execute a medium-scope task, code edit, system addition, Jira task, bugfix, or moderate build-from-scratch project with phased planning, raw task capture, codebase/task maps, external audit ledgers, TDD, runtime QA, Playwright checks, modular implementation discipline, and adversarial plus judge/verifier swarms after every task and phase.
---

# Swarm Verify

Use this as the master orchestrator. Treat the user's text after the skill name as the task.

If the task is missing or too vague to test, ask only for the blocking objective, expected behavior, and repo/path. Otherwise start.

## Required Dependency Skills

Use or trigger these when available:

This same dependency set applies when any `swarm-verify-*` subskill is invoked directly.

- `computa-init`: project-local `docs/` and `docs/computa-artifacts/` initialization.
- `computa-speak`: prompt normalization from raw request to `normalized-task.md`.
- `computa-resume`: recover the latest session/phase/task from `activity-log.csv` when resuming prior work.
- `computa-secrets-needed`: safe ledger and handoff prompts for missing API keys, OAuth credentials, webhook secrets, model-provider keys, and deployment secrets.
- `computa-make-no-mistakes-docs-update`: architecture-doc update hook after every phase and final closeout.
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

## Load Order

Read and apply these sub-skills in order:

1. `swarm-verify-setup`
2. `computa-speak`
3. `swarm-verify-investigate`
4. `swarm-verify-tdd-qa`
5. `computa-make-no-mistakes-docs-update` at the end of each phase
6. `swarm-verify-swarms`
7. `swarm-verify-closeout`

Also read `references/master-swarm-verification-prompt.md` when present. It is the parity source. If a detail is present there and absent here, follow the reference unless the user explicitly overrides it.

## Global Rules

- Before each meaningful action, briefly justify it and challenge why it might be wrong.
- Do not assume. Verify from source files, docs, PRs, tests, logs, dashboards, or runtime behavior.
- Save the raw user request to `user-task.md` before rewriting, summarizing, or planning from memory.
- Run `computa-init` when available so `docs/`, `docs/computa-artifacts/`, and root ledgers exist before planning.
- Run `computa-speak` immediately after raw request capture. Use `normalized-task.md` as the working prompt, but keep `user-task.md` as source truth for scope and permissions.
- Keep all plan, phase, task, subtask, issue, blocker, evidence, and report artifacts in a session under `<invocation-root>/docs/computa-artifacts/`.
- Keep actual architecture docs at `docs/architecture/`, not under `docs/computa-artifacts/`.
- If this is standalone, use `docs/computa-artifacts/computa/CMN-.../`. If a parent 4D session invoked this run, use the parent session's `computa/CMN-.../` child directory.
- Register every session in `docs/computa-artifacts/session-ledger.csv` and gitignore `docs/computa-artifacts/` when it is inside a repo.
- Maintain `docs/computa-artifacts/activity-log.csv` as the root resume log. Append session, phase, and task start/finish/block rows as they happen; do not log subtask rows there.
- Before targeted implementation work, create and maintain a reusable codebase/task map so later phases can reference known entrypoints, flows, files, commands, risks, and unknowns.
- If `docs/architecture/` exists, read it first for orientation, then verify its claims against source during Phase 1. If it is missing and the codebase needs handoff docs, build it through `computa-docs-architecture`.
- Treat maps as living artifacts. They may change at any time when new evidence appears; track every map update in both Markdown and CSV under `maps/`.
- Use ledgers as the source of truth for order, dependencies, status, and evidence.
- Do phases, tasks, and subtasks only after prerequisites are complete.
- Use swarms for safe parallelism only. Do not parallelize overlapping files, systems, data, migrations, dashboards, deployment state, browsers, databases, queues, or test environments.
- Run TDD for behavior changes: failing test first, minimal fix, passing test after.
- Run runtime QA on actual functionality, not only static review.
- Use `playwright` for browser-visible behavior.
- Solve edge cases discovered during investigation.
- Prefer small, modular, readable components over gigantic files. Split by responsibility, use narrow interfaces, and avoid mixing unrelated concerns in one file.
- If any work needs an API key, OAuth credential, webhook secret, model-provider token, deployment secret, or dashboard/private config, use `computa-secrets-needed` immediately. Keep building with named env vars/placeholders/mocks/guards where safe, add missing-secret tests when applicable, and record the exact verification blocked by the missing secret.
- Never store secret values in code, artifacts, logs, reports, screenshots, terminal output, or git. Store only secret names, target env paths, platform targets, code paths, owner action, and the safe `@Computer` handoff prompt.
- Keep audit logs current. Do not reconstruct them only at the end.
- For every Computa phase and task, append the event to `activity-log.csv` at start and completion, for example `phase_started`, `task_started`, `task_completed`, `phase_completed`, or `phase_blocked`.
- Make one commit per completed task only after verification passes and commits are allowed.
- Do not push unless explicitly asked.

## Execution Flow

1. Phase 0: use `swarm-verify-setup` to create artifacts, preserve the raw request, split phases/tasks/subtasks, initialize ledgers, and append `session_started` to `activity-log.csv`.
2. Prompt normalization: use `computa-speak` to create `normalized-task.md`; downstream work analyzes it and cross-checks `user-task.md`.
3. Phase 1: use `swarm-verify-investigate` to run an orientation audit of the task and working codebase before implementation. Create a living `maps/` directory that later phases can reference.
4. Phase 2: continue `swarm-verify-investigate` to establish baseline truth, reproduce the issue or prove the gap, identify expected behavior, and create failing evidence.
5. Implementation phases: use `swarm-verify-tdd-qa` for test-first changes, smallest fixes, edge cases, unit/integration/smoke/runtime QA, and Playwright verification.
6. After every phase, use `computa-make-no-mistakes-docs-update` to create/update architecture docs from ledgers and source truth, or record a no-op/blocker with evidence.
7. After every task and phase: use `swarm-verify-swarms` for adversarial review followed by judge/verifier review. Do not implement adversarial recommendations unless the matching judge/verifier approves.
8. Closeout: use `swarm-verify-closeout` to reconcile ledgers, append final `session_completed` or `session_blocked` status to `activity-log.csv`, create final reports, compare against `user-task.md`, record new fixed/unfixed issues, verify docs status, verify evidence, and state remaining gaps.

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
- root `docs/computa-artifacts/activity-log.csv` exists and records session, phase, and task start/finish/block events needed for crash recovery
- current task/codebase map exists, is referenced by later work, and records entrypoints, relevant files, commands, tests, flows, risks, unknowns, and out-of-scope areas
- map change log and map change ledger exist and cover every material map update
- phases/tasks/subtasks completed or explicitly deferred with rationale
- failing-before evidence or documented reason it was impossible
- passing-after evidence
- relevant unit, integration, smoke, runtime, and Playwright checks
- adversarial and judge/verifier swarms after each task and phase
- architecture docs updated, created, no-op recorded, or blocked with evidence after every phase
- secrets-needed ledger and reports current, including target env/platform paths and any private-config verification blockers
- final reports with gaps, blockers, verification needs, and new fixed/unfixed issues

Golden rule: evidence before assertions. Never say "it works" without verification command output and runtime proof.
