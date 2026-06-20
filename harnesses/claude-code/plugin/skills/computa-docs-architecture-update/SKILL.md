---
name: computa-docs-architecture-update
description: Create, revise, split, remove, or mark stale docs/architecture content from a source-backed architecture audit. Use after computa-docs-architecture-audit or after Computa phase work to keep architecture docs accurate and detailed without guessing.
---

# Computa Docs Architecture Update

Use this to apply architecture documentation changes after an audit. It updates docs from source truth, not from intent or chat memory.

Append `docs_architecture_update_started` to `docs/computa-artifacts/activity-log.csv` when available before editing docs, and `docs_architecture_update_completed` or `docs_architecture_update_blocked` after, with `artifact_path=docs/architecture/` and `evidence_path=docs/architecture/AUDIT-REPORT.md`.

## Required Inputs

Read:

- `docs/architecture/AUDIT-REPORT.md`
- `docs/architecture/_meta/source-ledger.csv`
- `docs/architecture/_meta/claim-ledger.csv`
- `docs/architecture/_meta/coverage-map.md`
- relevant repo source files and command outputs cited by the audit
- current Computa phase/task ledgers when invoked from a Computa session

If the audit is missing or too weak, run `computa-docs-architecture-audit` before updating.

## Update Targets

Maintain the following where applicable:

- `README.md`: quick navigation, system-at-a-glance, module index, key numbers, and where-to-find table.
- `ARCHITECTURE.md`: concise but complete system architecture.
- `AUDIT-REPORT.md`: updated audit status and change log.
- module docs under directories such as `api/`, `frontend/`, `data-model/`, `auth/`, `infrastructure/`, `agents/`, `orchestrator/`, `services/`, `domain/`, or project-specific names.
- `_meta/source-ledger.csv`, `_meta/claim-ledger.csv`, `_meta/coverage-map.md`, and `_meta/docs-update-log.md`.

## Editing Rules

- Add missing docs for important architecture surfaces.
- Update stale docs with current code-derived behavior.
- Remove, archive, or mark obsolete generated architecture docs when they mislead. Be conservative with clearly user-authored narrative notes; preserve them with an `unknown` or `needs owner decision` label if intent is unclear.
- Split oversized docs when module-level docs would be clearer.
- Use tables for route inventories, env vars, jobs, schemas, events, integrations, and commands.
- Cite source paths and commands for material claims.
- Preserve unknowns instead of guessing.
- Keep docs readable and modular. Do not create one massive catch-all file.

## Audit Report Requirements

After updates, `AUDIT-REPORT.md` must state:

- what changed in the docs
- what code/source evidence supports it
- what was verified
- what remains stale, missing, unknown, or owner-dependent
- what docs were added, removed, split, or left intentionally unchanged
- whether docs are current enough for planning or handoff

## Completion Bar

Do not claim docs are updated until:

- all audit-approved doc changes are applied or explicitly deferred
- claim/source ledgers match the docs
- coverage map reflects remaining gaps
- docs-update-log records the update
- a fresh reader can find system overview, module docs, known gaps, and source evidence without chat context
