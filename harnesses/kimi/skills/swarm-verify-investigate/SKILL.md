---
name: swarm-verify-investigate
description: "Run Phase 1 investigation and baseline for swarm-verified work: independently verify source truth, current behavior, expected behavior, issue origin, edge cases, coverage gaps, baseline commands, and failing evidence before implementation. Use before coding or fixing bugs."
---

# Swarm Verify Investigate

Use this for Phase 1 before implementation.

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

Before moving past Phase 1:

- update phase, task, subtask, issue, and blocker ledgers
- record evidence paths
- list assumptions that changed
- list open questions and whether they block work
- run phase-level adversarial review and judge/verifier review through `swarm-verify-swarms`

Do not implement before baseline evidence exists.
