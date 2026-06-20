---
name: computa-make-no-mistakes
description: One-command entrypoint that invokes the complete swarm-verify suite for a medium-scope task, including Jira/task fixes, editing existing code, adding features to a system, or building a moderate project from scratch with setup, investigation, TDD/runtime QA, swarms, and closeout. Use when the user wants the full swarm-verify workflow from one skill invocation.
---

# Computa Make No Mistakes

Use this as the single-command entrypoint for a Jira task, bugfix, system addition, code edit, or medium-scope build-from-scratch project. Treat the user's text after the skill name as the task.

For ultra-long autonomous work, use `computa-4d-chess`. For massive research/strategy work that should decide what to build and what tools to use before 4D execution, use `computa-export-control`.

If the task is missing or too vague to test, ask only for the blocking objective, expected behavior, and repo/path. Otherwise start.

## Required Dependency Skills

Use or trigger these when available:

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

## Invoke The Full Suite

Load and apply every swarm-verify skill in this order:

1. `swarm-verify`
2. `swarm-verify-setup`
3. `computa-speak`
4. `swarm-verify-investigate`
5. `swarm-verify-tdd-qa`
6. `swarm-verify-swarms`
7. `swarm-verify-closeout`

Also load and apply `computa-make-no-mistakes-docs-update` at the end of every phase and during final closeout.

Do not skip a listed skill because this entrypoint is "one-shot". One-shot means the user invokes one skill; internally, the full suite still runs.

Also read `swarm-verify/references/master-swarm-verification-prompt.md` when present. It is the parity source. If a detail is present there and absent here, follow the reference unless the user explicitly overrides it.

## Execution Contract

Execute the task end to end under the complete swarm-verify rules:

- Before each meaningful action, briefly justify it and challenge why it might be wrong.
- Save the raw user request to `user-task.md` before rewriting, summarizing, or planning from memory.
- Run `computa-init`, create `docs/` if missing, create or reuse `<invocation-root>/docs/computa-artifacts/`, and create a new `CMN-YYYYMMDD-HHMMSS-slug` session for this invocation.
- Immediately after raw request capture, run `computa-speak` to create `normalized-task.md` and `prompt-normalization-log.md`. Downstream phases analyze `normalized-task.md` first and cross-check `user-task.md` when scope or permissions matter.
- If this is a standalone Computa run, place it under `docs/computa-artifacts/computa/CMN-.../`. If invoked by 4D Chess, place it under the parent 4D session at `.../computa/CMN-.../`.
- Register the session in `docs/computa-artifacts/session-ledger.csv` with `layer=computa` and the parent session ID when applicable.
- Maintain `docs/computa-artifacts/activity-log.csv` with the standard header. Append `session_started` as soon as the CMN session exists.
- If `docs/computa-artifacts/` is inside a git repo, ensure it is ignored by `.gitignore`.
- If `docs/architecture/` exists, read its `README.md`, `ARCHITECTURE.md`, `AUDIT-REPORT.md`, and relevant module docs before the Phase 1 codebase audit. Treat those docs as orientation, then verify them against source files and update stale claims.
- Phase 0: create the artifact root, plan directory, `plan.md`, master task CSV, issue/blocker Markdown and CSV ledgers, phase directories, task directories, subtask ledgers, and reports directory.
- Phase 1: run a codebase/task orientation audit before implementation. Create reusable living maps for scope, codebase, flows, commands/tests, risks, unknowns, and out-of-scope areas.
- Keep maps current. Maps may change at any time when evidence changes; track each material update in both Markdown and CSV under `maps/`.
- Phase 2: investigate source truth, current behavior, expected behavior, issue origin, edge cases, baseline commands, and failing evidence before implementation.
- Split work into phases, tasks, and subtasks with explicit order and dependencies. Do not run dependent work before prerequisites are done.
- Append to the root `activity-log.csv` every time a phase or task starts, completes, blocks, or is deferred. Example events: `phase_started`, `task_started`, `task_completed`, `phase_completed`, `phase_blocked`. Subtasks stay in task-level subtask ledgers and are not duplicated in the root activity log.
- Prefer small, modular, readable components over gigantic files. Split by responsibility, keep APIs narrow, follow existing project boundaries, and avoid dumping unrelated behavior into one file.
- If any phase, task, or subtask needs an API key, private config, OAuth app, webhook secret, provider token, deployment secret, or dashboard credential, run `computa-secrets-needed` immediately. Build as far as possible with named env vars, placeholders, mocks, feature guards, and missing-secret tests where reasonable; record what runtime/deploy verification remains blocked until the secret is configured.
- Never put actual secret values in code, artifacts, logs, reports, screenshots, terminal output, or git. The secrets-needed artifact must include target env paths, platform secret targets, related code paths, blocked verification, and a safe `@Computer` prompt for a future explicitly-authorized credential handoff.
- Use safe swarms for parallelism only. Do not parallelize overlapping files, systems, data, dashboards, databases, browsers, servers, deployments, migrations, queues, or dependent subtasks.
- For behavior changes, use TDD: failing test first, smallest fix, passing test after.
- Run relevant unit, integration, smoke, runtime, and Playwright/browser-visible QA. Solve discovered edge cases.
- After every task, run one adversarial reviewer per subtask, then one judge/verifier per subtask. Only implement judge-approved recommendations.
- After every phase, run `computa-make-no-mistakes-docs-update` so `docs/architecture/` is created, updated, no-op recorded, or blocked with evidence based on the phase ledgers and code truth.
- After every phase docs update, run one adversarial reviewer per task, then one judge/verifier per task. Do not close a phase until each task is approved complete, approved deferred, or blocked with evidence.
- Keep ledgers, logs, and evidence current as work happens.
- Make one descriptive commit per completed task only after verification passes and commits are allowed.
- Do not push unless explicitly asked.
- At closeout, append `session_completed` when the task is complete, or `session_blocked` when it cannot safely proceed. The final row must include the report path and exact `next_action` for resume.

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
- architecture docs created/updated/no-op/blocked status, changed docs paths, and remaining docs gaps
- `docs/computa-artifacts/secrets-needed/` status, required secrets, target env/platform paths, and any verification blocked by missing private config
- new issues found and fixed
- new issues found and not fixed
- exact verification commands and runtime QA evidence

Golden rule: evidence before assertions. Never say "it works" without verification command output and runtime proof.
