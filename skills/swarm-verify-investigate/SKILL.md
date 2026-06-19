---
name: swarm-verify-investigate
description: "Run Phase 1 orientation audit and Phase 2 investigation/baseline for swarm-verified work: map the codebase/task, independently verify source truth, current behavior, expected behavior, issue origin, edge cases, coverage gaps, baseline commands, and failing evidence before implementation. Use before coding or fixing bugs."
---

# Swarm Verify Investigate

Use this for Phase 1 orientation audit and Phase 2 investigation before implementation.

## Required Discipline

Use `investigate` or `systematic-debugging` when available. If not available, follow the same root-cause standard manually.

Before each investigation action, state:

- why this action is useful
- what assumption it could falsify

## Source Truth

Inspect the relevant source materials before changing code:

- user-task.md
- repo files and tests
- PRs, branches, tickets, docs, specs, prompts, logs, dashboards, or console state
- prior reports and ledgers
- runtime behavior where applicable

Do not infer scope from branch names alone. Use the original request and source-of-truth artifacts.

## Orientation Audit And Map

Before targeted fixes or implementation, audit the working context broadly enough to avoid editing blind.

Create or update the artifact root `maps/` directory with:

- `map-index.md`: map inventory, timestamps, evidence paths, and where later phases should look first.
- `task-scope-map.md`: raw request summary, acceptance criteria, constraints, explicit exclusions, likely stakeholders, and unresolved questions.
- `codebase-map.md`: repo roots, package/app boundaries, key modules, entrypoints, route/API surfaces, config files, generated/reference-only files, and relevant ownership boundaries.
- `flow-map.md`: user, runtime, data, analytics, queue, network, database, deployment, or dashboard flows relevant to the task.
- `test-and-command-map.md`: package manager, install/build/lint/test commands, existing test locations, missing test coverage, smoke/runtime commands, and Playwright/browser routes if relevant.
- `risk-map.md`: high-risk files/systems, edge cases, migrations, external consoles, credentials/secrets boundaries, production-touching surfaces, race conditions, and assumptions to challenge.

Use fast structural reads first: `git status`, branch/remotes, `rg --files`, package manifests, config files, routes, tests, docs, PR/ticket references, and runtime entrypoints. Then inspect only the files needed to make the map accurate.

If the codebase is huge, make the audit task-focused but still map adjacent systems that could regress. Mark unexplored areas explicitly with why they appear irrelevant or why they remain unknown.

Keep maps living. Whenever later work disproves a map entry or discovers a new flow/file/risk, update the relevant map and ledger before continuing.

## Baseline Work

Identify and log:

- existing behavior
- expected behavior
- suspected issue origin
- likely edge cases
- current tests and coverage gaps
- systems/files that may be touched
- safe verification commands for the repo
- runtime QA route or endpoint, if relevant
- map artifacts used and any map updates made

Run baseline verification before changing code. Capture command output and evidence paths.

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
- record evidence paths
- list assumptions that changed
- list open questions and whether they block work
- run phase-level adversarial review and judge/verifier review through `swarm-verify-swarms`

Do not implement before baseline evidence exists.
