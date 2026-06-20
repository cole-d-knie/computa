---
name: computa-make-no-mistakes-docs-update
description: End-of-phase architecture documentation hook for computa-make-no-mistakes. Use after every Computa phase and final closeout to build or update docs/architecture from phase ledgers, code changes, maps, tests, and source-backed evidence.
---

# Computa Make No Mistakes Docs Update

Use this at the end of every Computa phase and again during final closeout. Its job is to keep architecture docs current with the actual work and evidence produced by the phase.

## Required Inputs

Read the current Computa session:

- `user-task.md`
- plan and master ledgers
- current phase directory
- task/subtask ledgers
- issue and blocker logs
- evidence index and command outputs
- maps and map-change ledgers
- git status/diff when working in a repo
- test, build, lint, smoke, runtime, and Playwright evidence

Also read `docs/architecture/` first if it exists:

- `README.md`
- `ARCHITECTURE.md`
- `AUDIT-REPORT.md`
- relevant module docs
- `_meta/source-ledger.csv`
- `_meta/claim-ledger.csv`
- `_meta/coverage-map.md`

## Phase Hook Flow

1. Decide whether the completed phase changed architecture-relevant truth: modules, APIs, flows, data model, auth, security, privacy, analytics, integrations, config, deployment, tests, or runtime behavior.
2. Append `docs_update_started` to the root `docs/computa-artifacts/activity-log.csv` with the current phase as `scope_id`.
3. If `docs/architecture/` is missing or empty, invoke `computa-docs-architecture` to initialize, audit, and create docs.
4. If docs exist, invoke `computa-docs-architecture-audit` focused on changed and adjacent surfaces, then `computa-docs-architecture-update`.
5. If the phase made no docs-relevant changes, record a no-op in the session and docs update logs with evidence.
6. Update Computa phase/task ledgers with the docs action, docs paths, and remaining gaps.
7. Append `docs_update_completed`, `docs_update_noop`, or `docs_update_blocked` to `activity-log.csv` with the docs update evidence and next action.

## Logging

Record every phase docs update under the current Computa session, preferably:

- `docs-updates/phase-docs-update-log.md`
- `docs-updates/phase-docs-update-ledger.csv`

Use this CSV header:

`update_id,timestamp,phase,task_scope,docs_action,architecture_docs_path,audit_report_path,evidence_path,status,remaining_gap`

Also append to `docs/architecture/_meta/docs-update-log.md` when architecture docs exist.

Also keep the root `docs/computa-artifacts/activity-log.csv` current so `computa-resume` can tell whether the phase is blocked on architecture-doc updates.

## Rules

- Architecture docs are source-backed handoff material, not a diary.
- Do not update docs from chat memory alone.
- Tie doc changes to code/source paths and phase evidence.
- Preserve unknowns and blockers.
- Keep docs modular and readable; split by architecture surface when needed.
- Do not close a Computa phase until this docs hook is complete, no-op with evidence, or blocked with a recorded reason.

## Closeout Requirement

Final Computa closeout must report:

- whether architecture docs were created, updated, no-op, or blocked
- exact docs paths changed
- remaining architecture-doc gaps
- whether `docs/architecture/AUDIT-REPORT.md` says the docs are current enough for follow-up planning
