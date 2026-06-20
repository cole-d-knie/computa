---
name: computa-docs-architecture-init
description: Initialize docs/architecture structure for Computa architecture documentation. Use when architecture docs are missing, empty, or need a verified source-ledger scaffold before a codebase audit and docs build/update.
---

# Computa Docs Architecture Init

Use this to create the architecture docs skeleton. It prepares structure only; it does not invent architecture content.

## Preconditions

Run `computa-init` first so `docs/` and `docs/computa-artifacts/` exist.

Create `docs/architecture/` if missing. Do not overwrite existing docs.

Append `docs_architecture_init_started` to `docs/computa-artifacts/activity-log.csv` when available before creating files, and `docs_architecture_init_completed` or `docs_architecture_init_blocked` after, with `artifact_path=docs/architecture/`.

## Required Structure

Create or reuse:

- `docs/architecture/README.md`
- `docs/architecture/ARCHITECTURE.md`
- `docs/architecture/AUDIT-REPORT.md`
- `docs/architecture/_meta/`
- `docs/architecture/_meta/source-ledger.csv`
- `docs/architecture/_meta/claim-ledger.csv`
- `docs/architecture/_meta/coverage-map.md`
- `docs/architecture/_meta/docs-update-log.md`

Seed empty or placeholder files only when absent. Placeholder text must say the file is pending source-backed audit and must not present guesses as fact.

## Module Directories

Create module directories only when the codebase indicates they exist or the user explicitly requests them. Common examples:

- `api/`
- `frontend/`
- `data-model/`
- `auth/`
- `infrastructure/`
- `agents/`
- `orchestrator/`
- `services/`
- `domain/`
- `analytics/`

Prefer project-specific names when the codebase has stronger local language.

## Ledger Headers

Use this header for `source-ledger.csv`:

`source_id,path_or_url,type,date_checked,owner_or_area,claim_supported,reliability,license_or_policy_notes,notes`

Use this header for `claim-ledger.csv`:

`claim_id,doc_path,claim,source_id,status,action,checked_at,notes`

Statuses should be one of:

- `verified`
- `stale`
- `wrong`
- `missing`
- `unknown`
- `not_applicable`

## Logging

Append every initialization action to `_meta/docs-update-log.md` with timestamp, files created, files reused, and any unknowns that the audit must resolve.
