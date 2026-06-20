---
name: computa-export-control-technical-spec
description: Focused Computa Export Control technical specification skill for turning researched requirements, codebase audits, technology decisions, and prior-art findings into execution-grade engineering specs before computa-4d-chess campaign design. Use when Export Control needs concrete module boundaries, API contracts, data models, integration flows, state machines, error handling, migration/backcompat plans, observability, test strategy, implementation slices, and acceptance contracts instead of vague architecture or product prose.
---

# Computa Export Control Technical Spec

Use this after Export Control has enough product, codebase, technology, prior-art, and tool evidence to specify how the system should work. This skill creates the technical execution contract that later `computa-4d-chess` campaigns must follow.

This is not product requirements, architecture docs, or an implementation plan:

- Product requirements define what users/business need.
- Architecture docs describe verified current or final system architecture.
- Technical specs define exactly how proposed work should be engineered before execution.
- Implementation plans break the technical spec into coding tasks later.

## Inputs

Read:

- `user-task.md`
- `normalized-task.md`
- `requirements/`
- `codebase-audit/`
- `tech-radar/`
- `prior-art/`
- `skills-and-tools/`
- `decision-matrix.md` and `.csv` when present
- `recommended-design.md` when present
- existing `docs/architecture/` readouts and stale/missing docs notes
- relevant source files, tests, schemas, configs, dashboards, APIs, docs, or external systems needed to verify spec claims

If an existing codebase is involved, do not write target specs until current source truth and local patterns are understood. If required inputs are missing, record a blocker or run the missing Export Control subskill first.

## Activity Log

When `docs/computa-artifacts/activity-log.csv` exists, append:

- `technical_spec_started` before drafting
- `technical_spec_completed`, `technical_spec_blocked`, or `technical_spec_deferred` after review

Use `scope_name=technical-spec`, `artifact_path=technical-spec/spec-index.md`, and set `next_action` to the exact next design or 4D campaign step.

## Output Directory

Write under `technical-spec/` in the current Export Control session:

- `spec-index.md`: reading order, spec status, source inputs, and owner decisions.
- `technical-brief.md`: concise engineering summary, scope, non-scope, success criteria, and target reader.
- `current-state.md`: source-backed current implementation, constraints, patterns, reusable code, and gaps.
- `target-state.md`: proposed behavior and architecture at the engineering level.
- `module-boundaries.md`: modules/components/files to create, modify, preserve, split, or avoid bloating; ownership and responsibilities.
- `component-design.md`: component responsibilities, interfaces, invariants, lifecycle, and internal collaboration.
- `api-contracts.md`: routes, methods, request/response schemas, validation, auth, idempotency, errors, versioning, and compatibility.
- `data-model.md`: entities, schemas, migrations, indexes, retention, privacy, data ownership, and backfill needs.
- `state-and-flow-design.md`: user/runtime/data/control flows, state machines, sequence diagrams or Mermaid diagrams where useful.
- `integration-design.md`: external services, SDKs, events, queues, webhooks, credentials, rate limits, retries, and failure modes.
- `env-and-secrets.md`: required env vars, API keys, OAuth/webhook secrets, model-provider keys, deployment secrets, dashboard/private config, target env/platform paths, fallback/missing-secret behavior, and verification blocked until configured. Link to root `docs/computa-artifacts/secrets-needed/` entries.
- `security-privacy-auth.md`: authz/authn, threat surfaces, PII/secrets, consent, policy constraints, abuse cases, and mitigations.
- `observability-analytics.md`: logs, metrics, traces, events, dashboards, alerts, analytics semantics, and debug hooks.
- `performance-reliability.md`: latency, throughput, caching, concurrency, races, retries, timeouts, degradation, and SLO-like expectations.
- `migration-rollout-backcompat.md`: migrations, flags, rollout phases, rollback, compatibility, data repair, and deploy order.
- `test-strategy.md`: unit/integration/e2e/smoke/runtime/Playwright coverage, fixtures, failing-before expectations, and acceptance evidence.
- `implementation-slices.md`: engineering slices that can become 4D campaigns or Computa phases, with dependencies and non-overlap notes.
- `risks-edge-cases.md`: edge cases, technical risks, unknowns, tradeoffs, and mitigation evidence.
- `acceptance-contract.md`: exact conditions a later implementation must satisfy before it can be called done.
- `open-questions.md` and `.csv`: questions, owner, impact, blocking status, and resolution path.
- `spec-ledger.csv`: spec section, status, source evidence, reviewer, blockers, and next action.

Only create sections that are relevant, but `spec-index.md`, `technical-brief.md`, `current-state.md`, `target-state.md`, `implementation-slices.md`, `test-strategy.md`, `acceptance-contract.md`, and `spec-ledger.csv` are required.

## Spec Standards

- Treat the spec as a contract for future agents. A fresh agent should not need chat history to understand what to build.
- Separate current state from target state.
- Tie every material claim to source evidence or mark it as an assumption, open question, or owner decision.
- Prefer small, modular, readable components over giant files or monolithic subsystems.
- Define boundaries before implementation slices.
- Write concrete contracts: function/module responsibilities, API schemas, event names, data fields, state transitions, validation rules, error cases, and compatibility rules.
- Use `computa-secrets-needed` for every private config requirement. Specs should still describe and slice implementation with named env vars, placeholders, mocks, missing-secret guards, and tests where possible.
- Include rejected approaches and why they were rejected when the choice affects implementation.
- Use diagrams only when they clarify flow or boundaries; label nodes and edges clearly.
- Do not hide uncertainty. Block execution when unresolved questions could materially change architecture, data, security, privacy, or rollout.
- Do not duplicate full architecture docs. Link to `docs/architecture/` for verified existing architecture and write only the technical design needed for this work.

## Review Gate

Before Export Control campaign design:

1. Run adversarial review of spec completeness, source evidence, contracts, boundaries, risk handling, testability, and missing edge cases.
2. Run judge/verifier review of adversarial findings.
3. Update only judge-approved recommendations.
4. Mark the technical spec `approved_for_campaign_design`, `approved_with_risks`, `deferred`, or `blocked` in `spec-index.md` and `spec-ledger.csv`.

Do not let 4D campaign design proceed from vague requirements when a technical spec is needed and missing.
