---
name: computa-export-control-codebase-audit
description: Mandatory first-pass Computa Export Control research skill for existing repos/codebases before major planning. Use to map architecture, dependencies, conventions, reusable modules, gaps, giant-file/modularity risks, test/runtime capabilities, and places where packages, tools, skills, or build-from-scratch work may help.
---

# Computa Export Control Codebase Audit

Use this to understand what exists before recommending requirements, technology, prior-art reuse, or execution campaigns. If an existing codebase is present, this skill runs before other export-control research is finalized.

If invoked directly and `docs/computa-artifacts/activity-log.csv` exists or can be initialized, append `research_task_started` before the audit and `research_task_completed`, `research_task_blocked`, or `research_task_deferred` after it, with `scope_name=codebase-audit` and `artifact_path=codebase-audit/`.

## Audit Scope

Inspect:

- existing `docs/architecture/` first when present, then verify its claims against source
- repo layout, package manager, frameworks, build/test/lint commands
- important modules, boundaries, entrypoints, generated files, and reference-only areas
- dependencies, duplicated utilities, dead code, existing abstractions, and extension points
- large files, monolith components, mixed responsibilities, and readability risks
- tests, fixtures, smoke/runtime setup, CI, deployment, observability, and known flaky areas
- security, privacy, auth, data handling, analytics, billing, migrations, and external integrations when relevant

## Outputs

Write under `codebase-audit/`:

- `codebase-intelligence-map.md`: concise architecture and flow map.
- `docs-architecture-readout.md`: existing `docs/architecture/` files read, claims verified, stale/wrong/missing docs, and recommended docs updates.
- `dependency-inventory.md` and `.csv`: current packages/tools, purpose, risk, upgrade/add/keep/remove recommendation.
- `reuse-opportunities.md`: existing local modules/components/helpers that should be reused.
- `modularity-report.md`: giant files, mixed concerns, suggested splits, and files to avoid bloating.
- `test-runtime-map.md`: commands, coverage, smoke/runtime options, gaps, and verification order.
- `integration-surface-map.md`: APIs, data stores, dashboards, SaaS, credentials, queues, deployments, and external systems.
- `codebase-gaps.md`: missing capabilities that may justify new packages, tools, or 4D campaigns.

## Rules

- Prefer reading actual files over inferring from names.
- Existing architecture docs are useful maps, not source truth. Mark unsupported claims as stale, wrong, missing, or unknown.
- Prefer existing local patterns unless evidence supports changing them.
- Recommend small modular readable components over giant files.
- Separate findings from recommendations.
- Tie each recommendation to source paths or command output.
- Mark unknowns instead of guessing.
