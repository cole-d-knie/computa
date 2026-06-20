---
name: computa-docs-architecture
description: Build, audit, or update code-derived architecture documentation for a codebase. Use when a project needs docs/architecture created, when existing architecture docs may be stale, when Computa phase work changes architecture-relevant behavior, or when computa-make-no-mistakes, computa-4d-chess, or computa-export-control need source-backed docs before planning.
---

# Computa Docs Architecture

Use this as the architecture-documentation orchestrator. It produces a source-backed docs set shaped like the Securities Pulse architecture docs: a fast index, a full architecture narrative, module-level docs, and an audit report proving what was verified, changed, stale, missing, or unknown.

Architecture docs must live at `docs/architecture/`, as a sibling of `docs/computa-artifacts/`. Never create the actual architecture docs inside a Computa artifact session.

## Required Skills

Use or emulate these in order:

1. `computa-init`
2. `computa-docs-architecture-init`
3. `computa-docs-architecture-audit`
4. `computa-docs-architecture-update`

## Decision Flow

1. Run `computa-init` so `docs/` and `docs/computa-artifacts/` exist.
2. Append `docs_architecture_started` to `docs/computa-artifacts/activity-log.csv` when available, with `artifact_path=docs/architecture/`.
3. If `docs/architecture/` is missing or effectively empty, run `computa-docs-architecture-init`, then `computa-docs-architecture-audit`, then `computa-docs-architecture-update`.
4. If `docs/architecture/` exists, read it first for orientation:
   - `docs/architecture/README.md`
   - `docs/architecture/ARCHITECTURE.md`
   - `docs/architecture/AUDIT-REPORT.md`
   - relevant module docs under `docs/architecture/*/`
5. Verify the docs against code. Existing docs are leads, not authority.
6. Update, add, split, merge, or mark stale architecture docs according to the audit evidence.
7. Append `docs_architecture_completed` or `docs_architecture_blocked` to `activity-log.csv` with the audit report path and exact next action.

## Target Docs Shape

Create or maintain:

- `docs/architecture/README.md`: quick start, system-at-a-glance, diagrams when helpful, docs index, key numbers, and where-to-find table.
- `docs/architecture/ARCHITECTURE.md`: end-to-end system overview, module map, pipelines/flows, API surface, data model, frontend/client architecture, auth/security, infrastructure, observability, and known issues.
- `docs/architecture/AUDIT-REPORT.md`: what was audited, exact code/doc sources checked, verified claims, stale/wrong claims, missing docs, changes made, remaining gaps, and confidence.
- Module directories that fit the codebase, such as `api/`, `frontend/`, `data-model/`, `auth/`, `infrastructure/`, `agents/`, `orchestrator/`, `services/`, `domain/`, `analytics/`, or project-specific names.
- `docs/architecture/_meta/source-ledger.csv`: source path/URL, type, date checked, claim supported, reliability, and notes.
- `docs/architecture/_meta/claim-ledger.csv`: claim ID, doc path, claim, source evidence, status, action, and reviewer notes.
- `docs/architecture/_meta/coverage-map.md`: what the docs cover, what remains undocumented, and why.
- `docs/architecture/_meta/docs-update-log.md`: narrative log of doc updates and why they were made.

Only create module directories that match the actual codebase. Do not force irrelevant categories.

## Source Standard

Derive truth from code, config, tests, migrations, schemas, routes, package manifests, deployment files, runtime commands, and verified external docs. Do not guess.

For every material claim:

- cite source paths or commands in the relevant doc or ledger
- mark stale or unknown claims explicitly
- separate current implementation from intended design
- avoid copying large code blocks
- prefer compact tables for APIs, routes, data stores, jobs, and modules

## Update Policy

When docs already exist, update them heavily if the code demands it. Add missing files, remove or archive obsolete generated architecture docs, split overgrown docs, and correct stale claims. Preserve user-authored notes when intent is unclear, but label unsupported claims until verified.

When Computa phase work changed code, update architecture docs after the phase using `computa-make-no-mistakes-docs-update` so the docs reflect the ledger and the actual code.

## Completion Bar

Do not claim architecture docs are current until:

- the audit read the relevant codebase surfaces
- `AUDIT-REPORT.md` states verified, stale, missing, and unknown areas
- source and claim ledgers exist or are updated
- docs changes are tied to source evidence
- remaining gaps are explicit
