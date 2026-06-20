---
name: computa-swarm-verify-investigate
description: "Run Phase 1 orientation audit and Phase 2 investigation/baseline for computa-swarm-verified work: map the codebase/task, independently verify source truth, current behavior, expected behavior, issue origin, edge cases, modular component boundaries, coverage gaps, baseline commands, and failing evidence before implementation. Use before code edits, bug fixes, additions, or moderate build-from-scratch work."
---

# Computa Swarm Verify Investigate

Use this for Phase 1 orientation audit and Phase 2 investigation before implementation.

## Required Dependency Skills

When this subskill is invoked directly, use or trigger all computa-swarm-verify dependencies when available:

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

## Required Discipline

Use `investigate` or `systematic-debugging` when available. If not available, follow the same root-cause standard manually.

Before each investigation action, state:

- why this action is useful
- what assumption it could falsify

## Source Truth

Inspect the relevant source materials before changing code:

- user-task.md
- normalized-task.md when present, cross-checked against user-task.md
- `docs/architecture/` first when it exists, especially `README.md`, `ARCHITECTURE.md`, `AUDIT-REPORT.md`, and relevant module docs
- repo files and tests
- PRs, branches, tickets, docs, specs, prompts, logs, dashboards, or console state
- prior reports and ledgers
- runtime behavior where applicable

Do not infer scope from branch names alone. Use the original request and source-of-truth artifacts. Treat existing architecture docs as orientation, not proof; verify their claims against code and record stale, wrong, missing, or unknown docs in the maps and issue ledgers.

## Orientation Audit And Map

Before targeted fixes or implementation, audit the working context broadly enough to avoid editing blind.

Append `phase_started` to `docs/computa-artifacts/activity-log.csv` before Phase 1 orientation begins, with `scope_name=orientation-audit` and `artifact_path` pointing at the Phase 1 directory or `maps/`.

Create or update the artifact root `maps/` directory with:

- `architecture-docs-map.md`: existing `docs/architecture/` files read, claims trusted only after verification, stale or missing docs, and docs surfaces that should be updated after phases.
- `map-index.md`: map inventory, timestamps, evidence paths, and where later phases should look first.
- `task-scope-map.md`: raw request summary, acceptance criteria, constraints, explicit exclusions, likely stakeholders, and unresolved questions.
- `codebase-map.md`: repo roots, package/app boundaries, key modules, entrypoints, route/API surfaces, config files, generated/reference-only files, and relevant ownership boundaries.
- `flow-map.md`: user, runtime, data, analytics, queue, network, database, deployment, or dashboard flows relevant to the task.
- `test-and-command-map.md`: package manager, install/build/lint/test commands, existing test locations, missing test coverage, smoke/runtime commands, and Playwright/browser routes if relevant.
- `risk-map.md`: high-risk files/systems, edge cases, migrations, external consoles, credentials/secrets boundaries, production-touching surfaces, race conditions, and assumptions to challenge.
- `modularity-map.md`: existing component/module boundaries, reusable helpers, files at risk of becoming too large, and recommended split points for readable implementation.
- `map-change-log.md`: narrative change log for map updates.
- `map-change-ledger.csv`: structured change ledger for map updates.

Use fast structural reads first: `git status`, branch/remotes, `rg --files`, package manifests, config files, routes, tests, docs, PR/ticket references, and runtime entrypoints. Then inspect only the files needed to make the map accurate.

If the codebase is huge, make the audit task-focused but still map adjacent systems that could regress. Mark unexplored areas explicitly with why they appear irrelevant or why they remain unknown.

Keep maps living. Maps may change at any time when later work disproves a map entry or discovers a new file, flow, command, risk, edge case, dependency, or external system. Update the relevant map before continuing, and record the change in both `map-change-log.md` and `map-change-ledger.csv`.

## Baseline Work

Identify and log:

- existing behavior
- expected behavior
- suspected issue origin
- likely edge cases
- current tests and coverage gaps
- systems/files that may be touched
- modular component boundaries and files that should not become catch-alls
- safe verification commands for the repo
- runtime QA route or endpoint, if relevant
- map artifacts used and any map updates made
- map change ledger rows added during this investigation

Run baseline verification before changing code. Capture command output and evidence paths.

Append `phase_started` to `activity-log.csv` before Phase 2 investigation/baseline begins, with `scope_name=investigation-baseline` and `artifact_path` pointing at the Phase 2 directory or baseline evidence directory. Append completion or blocked status through `computa-swarm-verify-swarms` before moving to implementation.

## Reproduction Or Gap Proof

Reproduce the issue or prove the current gap.

If behavior can be tested:

- write or identify the first failing test before implementation
- confirm it fails for the right reason
- save the failing output

If a failing pre-fix test is impossible:

- document why
- capture the strongest available baseline evidence
- add post-fix regression or smoke verification where possible

## Investigation Close

Before moving past orientation or baseline investigation:

- update phase, task, subtask, issue, and blocker ledgers
- update `maps/map-index.md` and any stale map files
- update `maps/map-change-log.md` and `maps/map-change-ledger.csv` for every map change
- record evidence paths
- list assumptions that changed
- list open questions and whether they block work
- run phase-level adversarial review and judge/verifier review through `computa-swarm-verify-swarms`

Do not implement before baseline evidence exists.
