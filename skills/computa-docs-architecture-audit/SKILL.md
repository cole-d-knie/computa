---
name: computa-docs-architecture-audit
description: Audit a codebase and existing docs/architecture to produce source-backed architecture documentation findings. Use before creating or updating architecture docs, before Export Control or 4D planning on an existing repo, and whenever Computa phase work may have changed documented architecture.
---

# Computa Docs Architecture Audit

Use this to derive architecture truth from source before docs are written or updated.

Append `docs_architecture_audit_started` to `docs/computa-artifacts/activity-log.csv` when available before the audit, and `docs_architecture_audit_completed` or `docs_architecture_audit_blocked` after, with `artifact_path=docs/architecture/AUDIT-REPORT.md`.

## Audit Inputs

Start with:

- `user-task.md` or the raw request if this is part of a Computa session
- existing `docs/architecture/` docs, especially `README.md`, `ARCHITECTURE.md`, `AUDIT-REPORT.md`, and `_meta/`
- repo tree from `rg --files`
- package manifests and lockfiles
- framework/config files
- routes, API handlers, controllers, services, jobs, queues, workers, scripts, and CLIs
- schemas, migrations, models, database clients, fixtures, and seed data
- frontend pages, components, state, hooks, routing, and assets when present
- auth, security, privacy, consent, analytics, billing, env/config, deployment, observability, and external integrations when relevant
- tests, CI, smoke/runtime scripts, and developer commands

Use web or current docs only when architecture truth depends on version-specific libraries, SaaS behavior, or external APIs. Prefer primary sources and record URLs in `source-ledger.csv`.

## Existing Docs Review

If architecture docs exist, treat each material claim as unverified until checked. Classify claims as:

- `verified`: code/source supports it
- `stale`: once plausible but no longer current
- `wrong`: contradicted by source
- `missing`: important architecture surface is undocumented
- `unknown`: insufficient evidence
- `not_applicable`: claim does not apply to this codebase

Update `docs/architecture/_meta/claim-ledger.csv` with the claim, status, source evidence, and recommended action.

## Codebase Coverage

Produce or update:

- `docs/architecture/AUDIT-REPORT.md`
- `docs/architecture/_meta/source-ledger.csv`
- `docs/architecture/_meta/claim-ledger.csv`
- `docs/architecture/_meta/coverage-map.md`

The audit report must include:

- audit timestamp and scope
- commands run and files inspected
- areas verified
- stale/wrong docs found
- missing docs found
- high-risk unknowns
- recommended creates, updates, removals, and splits
- confidence level and remaining evidence needed

## Architecture Surfaces To Check

Audit enough of these to match the repo:

- app/module boundaries
- API and route surface
- data model and migrations
- request/data/control flows
- frontend composition and state
- auth and authorization
- background jobs and queues
- integrations and external accounts
- env vars and config
- deployment and infrastructure
- logging, metrics, and error handling
- tests and runtime QA paths
- security, privacy, consent, analytics, and billing surfaces when present

Mark unexplored surfaces explicitly. Do not silently omit them.

## Rules

- Prefer source reads over assumptions from filenames.
- Tie every material doc action to a source path, command, or verified external source.
- Separate implemented behavior from desired future behavior.
- Do not write architecture claims from memory.
- If evidence conflicts, preserve both sources and state what must be resolved.
- Recommend small module docs over one giant document when detail would become unreadable.
