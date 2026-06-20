---
name: computa-4d-chess-execute
description: Execute an approved Computa 4D Super-Phase plan for large edits, major system additions, or build-from-scratch projects by invoking computa-make-no-mistakes for each Super-Phase, enforcing dependencies, modular implementation checks, evidence collection, reviews, ledgers, map updates, and final 4D closeout.
---

# Computa 4D Chess Execute

Use this after `computa-4d-chess-build` has produced an approved Super-Phase plan. Execute does not redesign the architecture unless new evidence proves the plan is wrong.

## Preflight

Before execution, verify:

- `user-task.md` exists
- strategic design artifacts exist and were reviewed
- existing `docs/architecture/` has been read when present, and stale/missing docs risks are recorded
- `super-phases/super-phase-ledger.csv` exists
- `docs/computa-artifacts/secrets-needed/secrets-needed.csv` exists or can be initialized
- each Super-Phase has `super-phase.md`, `computa-invocation.md`, `expected-artifacts.md`, and `handoff.md`
- mandatory final `super-phases/SP-999-post-run-security-audit/` exists unless there is an explicit no-codebase/N/A blocker
- overall Super-Phase plan is `approved_for_execution` or `approved_with_risks`
- repo/path/base branch and permissions are known
- no explicit do-not-touch constraint is violated

If preflight fails, stop and record a blocker. Do not improvise execution from chat memory.

## Execution Loop

For each Super-Phase in dependency order, including mandatory final `SP-999-post-run-security-audit`:

1. Confirm prerequisites are complete with evidence.
2. Re-read the Super-Phase directory and global maps.
3. Briefly justify starting it and challenge why it might be unsafe or premature.
4. Append `super_phase_started` to `docs/computa-artifacts/activity-log.csv` with the Super-Phase directory as `artifact_path`.
5. Invoke `/computa-make-no-mistakes` using the exact prompt in `computa-invocation.md`. For `SP-999-post-run-security-audit`, that prompt must instruct Computa to run `/security-audit` in 4D final Super-Phase implementation mode.
6. Require the nested Computa run to create its own child session under this 4D session at `computa/CMN-YYYYMMDD-HHMMSS-slug/`, save its own `user-task.md`, register in `docs/computa-artifacts/session-ledger.csv`, append its own phase/task activity rows to the root `activity-log.csv`, build phases/tasks/subtasks, run investigation, TDD/QA, swarms, and closeout.
7. Import or link the nested Computa artifact root in the Super-Phase ledger.
8. Verify the nested closeout against the Super-Phase acceptance criteria.
9. Verify any secrets needed by the Super-Phase are recorded through `computa-secrets-needed`, with target env/platform paths and safe `@Computer` prompts. Missing credentials may block runtime/deploy verification, but they must not be hidden.
10. Verify the nested Computa docs hook created/updated architecture docs, recorded a no-op, or documented a blocker with evidence.
11. Run Super-Phase-level adversarial review.
12. Run Super-Phase-level judge/verifier review.
13. Verify the nested implementation stayed small, modular, readable, and consistent with the architecture.
14. Implement or schedule only judge-approved follow-up.
15. Update ledgers, issue logs, maps, handoffs, docs status, secrets-needed status, and evidence indexes.
16. Append `super_phase_completed`, `super_phase_blocked`, or `super_phase_deferred` to `activity-log.csv` with the review/evidence path and exact next action.

## Parallelism

Parallelize Super-Phases only when all are true:

- no dependency relation exists between them
- they do not touch overlapping files, modules, migrations, dashboards, databases, queues, browser sessions, test servers, deploys, credentials, data, or external accounts
- they have separate artifact roots and evidence paths
- a coordinator can reconcile outputs before any dependent Super-Phase begins

When unsure, execute serially.

## Plan Changes During Execution

If execution reveals the architecture or Super-Phase plan is wrong:

- stop affected work
- preserve the old evidence and plan
- write a plan-change proposal
- run adversarial review on the proposal
- run judge/verifier review
- update architecture maps, Super-Phase ledgers, dependencies, and handoffs only for approved changes
- resume from the corrected dependency point

Never silently skip, merge, or reorder Super-Phases.

## Super-Phase Closeout

After each Super-Phase, record:

- nested Computa artifact root
- nested phases completed/deferred/blocked
- verification commands and runtime QA evidence
- review verdicts
- issues found and fixed
- issues found and not fixed
- map updates caused by the Super-Phase
- architecture docs updates, no-op reason, or blockers caused by the Super-Phase
- secrets-needed entries added/updated and any verification blocked by missing private config
- whether dependent Super-Phases may start
- matching `activity-log.csv` row and latest resume point

## Final Security Super-Phase

`SP-999-post-run-security-audit` is the mandatory final Super-Phase. It is part of `super-phases/super-phase-ledger.csv`, not a hidden closeout hook.

The nested Computa run for SP-999 must create `security-audit/` inside the 4D session with:

- `invocation.md`: exact `/computa-make-no-mistakes` invocation, nested `/security-audit` invocation, repo path, starting branch, starting commit SHA, 4D session ID, and scoped audit branch/progress file names.
- `summary.md`: final security audit outcome, applied count, N/A count, blocked/skipped prompts, most important fixes, and remaining risks.
- `issues-and-blockers.md` and `.csv`: audit blockers, unsafe recommendations, owner decisions, and follow-up items.
- `security-audit-ledger.csv`: audit start/end timestamps, branch, progress file, commit range, verification command summary, and final status.

SP-999 execution rules:

1. Append normal `super_phase_started` and `super_phase_completed` or blocked/deferred rows for SP-999.
2. Also append `security_audit_started` to `docs/computa-artifacts/activity-log.csv` with `artifact_path` pointing to `security-audit/invocation.md` when `/security-audit` starts.
3. Invoke `/security-audit` through `/computa-make-no-mistakes`, using branch `vibecoder/security-<4d-session-id-or-slug>` and progress file `.claude/vibecoder/security-<4d-session-id-or-slug>-progress.md`.
4. Let `/security-audit` complete all 100 prompts or record precise blockers. Do not weaken security controls to satisfy a prompt.
5. Import or link the security audit progress file and git commit range into `security-audit/summary.md`.
6. Run architecture-docs update after audit changes.
7. Run SP-999 adversarial review, then judge/verifier review. Implement only judge-approved follow-up that is safe in this closeout context; otherwise log it as follow-up.
8. Append `security_audit_completed`, `security_audit_blocked`, or `security_audit_deferred` to `activity-log.csv`.

If there is no codebase/repo to audit, SP-999 can be `deferred` with a concrete N/A reason. If the 4D run is read-only or the user forbids security hardening commits, SP-999 must be `blocked` or `deferred` and 4D cannot be marked complete unless the blocker is explicitly accepted.

## 4D Closeout

After all Super-Phases:

- reconcile the master ledger and every Super-Phase ledger
- verify `SP-999-post-run-security-audit` is completed, explicitly N/A, or blocked/deferred with evidence and owner acceptance
- append `session_completed` or `session_blocked` for the 4D session to `docs/computa-artifacts/activity-log.csv`
- produce `reports/4d-summary.md`
- produce `reports/security-audit.md`
- produce `reports/verification-needed.md`
- produce `reports/blockers-and-open-issues.md`
- produce `reports/gaps-vs-user-task.md`
- produce `reports/new-issues-found.md`
- produce `reports/map-and-ledger-coverage.md`
- produce `reports/secrets-needed.md` summarizing required private config, target env/platform paths, safe `@Computer` prompt paths, configured/verified status, and remaining blocked verification
- state whether the original task is complete, partially complete, blocked, or requires owner decision

Do not claim completion while a nested Computa run is still active, while any Super-Phase is unreviewed, or while SP-999 is missing from the ledger.
