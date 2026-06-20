---
name: computa-export-control-design
description: Design-phase controller for Computa Export Control. Use to turn a massive or vague task into research questions, mandatory codebase audit for existing repos, product requirements, technology/package/prior-art searches, skill/MCP/tool intake, technical specs, decision matrices, and a reviewed sequence of computa-4d-chess campaigns before execution.
---

# Computa Export Control Design

Use this before `computa-export-control-execute`. Design researches and decides. It does not implement product code unless the user explicitly asks for a tiny discovery artifact.

## Inputs

Start from `normalized-task.md` when available, then cross-check `user-task.md` for source truth. If neither exists, save the raw request and run `computa-speak` before design. Inspect:

- repo/path and current codebase state
- `docs/architecture/` first when it exists, especially `README.md`, `ARCHITECTURE.md`, `AUDIT-REPORT.md`, and relevant module docs
- user goals, implied users, constraints, non-goals, deadlines, and risk tolerance
- existing reports, tickets, PRs, designs, docs, dashboards, APIs, deployments, and prior artifacts
- available skills, MCPs, plugins, connectors, browser/web access, GitHub access, and package/doc tooling

## Research Plan

Create `research-agenda.md` with:

- research questions grouped by product, codebase, technology, prior art, tools/skills, risks, and execution strategy
- source priorities and search queries
- what must be verified through web research
- what can be answered from the local codebase
- what can run in parallel safely
- stop conditions for research

Before each focused research task starts, append `research_task_started` to the root `docs/computa-artifacts/activity-log.csv` when an artifact root exists. After each focused task finishes, blocks, or is deferred, append `research_task_completed`, `research_task_blocked`, or `research_task_deferred` with the output path and next action. These rows are task-level resume points for Export Control design, not replacements for the detailed research ledgers.

Then invoke focused subskills as needed:

1. `computa-export-control-codebase-audit` when a repo/codebase exists
2. `computa-export-control-product-requirements`
3. `computa-export-control-tech-radar`
4. `computa-export-control-prior-art`
5. `computa-export-control-skill-mcp-intake`
6. `computa-export-control-technical-spec` after enough research exists and before audit-suite/campaign design
7. `computa-export-control-audit-suite` after enough source truth exists and before final campaign design

For existing codebases, complete and read the codebase audit before finalizing requirements, technology choices, prior-art reuse, or 4D campaign sequence.

If architecture docs exist, read them before the codebase audit and require the audit to verify, correct, or mark stale the relevant claims. If architecture docs are missing and the project is large enough that future agents would need them, add `computa-docs-architecture` to the design plan before execution or record why it is deferred.

For work that needs concrete engineering direction, run `computa-export-control-technical-spec` before creating 4D campaigns. Technical specs should convert the research into current/target state, module boundaries, component/API/data/integration design, rollout/backcompat, observability, test strategy, implementation slices, and an acceptance contract. If a technical spec is not needed, record why in `decision-matrix.md` and `campaigns/campaign-sequence.md`.

For existing codebases or apps, run `computa-export-control-audit-suite` after codebase/research/spec work and before final 4D campaign design. The audit suite runs `security-audit`, `performance-audit`, and `ui-audit` in documentation mode. If any category is not applicable, require a category no-op report with evidence. Do not create final 4D implementation campaigns until the audit suite has produced and reviewed `standalone-audits/remediation-backlog.csv`.

## Synthesis

Produce:

- `decision-matrix.md` and `.csv`: option, evidence, pros, cons, risk, cost, reversibility, recommendation.
- `recommended-design.md`: product and technical direction, including what should be edited versus built from scratch.
- `secrets-needed-readout.md`: private config/API key requirements discovered during research/design, with links to root `docs/computa-artifacts/secrets-needed/` entries and blocked verification.
- `docs-architecture-readout.md`: architecture docs read from `docs/architecture/`, verified useful claims, stale/missing claims, and docs work needed before or during execution.
- `reuse-plan.md`: packages, code examples, patterns, assets, skills, and tools worth using.
- `do-not-use.md`: rejected technologies, risky dependencies, stale examples, incompatible licenses, and why.
- `technical-spec/`: execution-grade specs produced by `computa-export-control-technical-spec`, or a documented deferral/no-op rationale.
- `standalone-audits/`: security/performance/UI audit documentation, category findings, consolidated remediation backlog, implementation campaign map, and audit-suite reviews.
- `campaigns/campaign-sequence.md`: sequential `computa-4d-chess` campaigns with objectives, prerequisites, outputs, risks, and expected prompts.
- `campaigns/campaign-ledger.csv`: campaign ID, name, status, dependencies, evidence paths, 4D prompt path, owner, next action.

## Design Rules

- Be a creative product manager and requirements analyst, but keep evidence separate from speculation.
- Existing-codebase work starts with the codebase audit. Do not design as if starting from scratch unless the audit supports replacement or greenfield work.
- Prefer using proven technology and reusable packages over custom implementation when it reduces risk.
- Prefer small, modular, readable components over large files or monolithic subsystems.
- When research, specs, recommended technologies, SaaS APIs, model providers, dashboards, OAuth apps, webhooks, or deployment targets require secrets/private config, invoke `computa-secrets-needed`. Keep design and build planning moving with named env vars and placeholders; mark only real credential-dependent verification as blocked.
- Do not turn vague requirements directly into 4D campaigns when technical contracts are needed. Specify boundaries, contracts, data, flows, rollout, and tests first.
- Do not turn audit prompts directly into 4D implementation tasks. First convert the 300 standalone prompts into evidence-backed findings, deduplicated backlog items, dependencies, and campaign groups through `computa-export-control-audit-suite`.
- Identify where existing code should be preserved, extended, replaced, or avoided.
- Record edge cases, missing requirements, future-proofing opportunities, and owner decisions.
- Do not recommend a package without checking fit, license, maintenance, ecosystem health, security posture, and integration cost.
- Do not recommend public code reuse without license and attribution notes.
- Keep 4D campaigns sequential by default. Only mark campaigns parallel-safe when there is no file, data, infra, dashboard, deployment, or conceptual dependency overlap.

## Review

Before execution:

1. Run adversarial review of research completeness, decision quality, package/tool choices, codebase assumptions, technical spec quality, audit-suite coverage, remediation-backlog quality, and campaign sequencing.
2. Run judge/verifier review of the adversarial findings.
3. Update artifacts only for judge-approved findings.
4. Mark the design `approved_for_execution`, `approved_with_risks`, or `blocked`.

If blocked, stop and report exactly what evidence or decision is missing.

Append the design review result to `activity-log.csv` as `export_control_design_approved` or `export_control_design_blocked`, with `campaigns/campaign-sequence.md` or the blocker report as `artifact_path`.
