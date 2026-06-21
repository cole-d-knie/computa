---
name: computa-4d-chess-architect
description: Strategic Computa architect skill for ultra-long autonomous tasks, large edits, major build-from-scratch projects, and broad system changes that need upfront codebase audit for existing repos, system design, technical specification, decision records, risk modeling, dependency analysis, modular component boundaries, and Super-Phase candidates before Computa execution.
---

# Computa 4D Chess Architect

Use this before building Super-Phases. Architect is for understanding, auditing, specifying, deciding, and designing. It does not implement unless the user explicitly asks for a tiny discovery artifact.

## Role

Act as the 4D architect above Computa. Produce the strategic design that later becomes Super-Phases. A Super-Phase should be large enough to justify its own `/computa-make-no-mistakes` run and small enough to have clear ownership, boundaries, inputs, outputs, and verification.

## Required Inputs

Start from `normalized-task.md` when available, then cross-check `user-task.md` for source truth. If neither exists, save the raw request and run `computa-speak` before architecting. If available, inspect:

- repo/path, base branch, working tree state, and relevant remotes
- product requirements, tickets, PRs, designs, docs, and previous reports
- architecture boundaries, services, data stores, APIs, queues, dashboards, deployments, secrets, migrations, and external systems
- tests, commands, CI, runtime entrypoints, observability, logs, and known flaky areas
- security, privacy, legal, billing, analytics, and data-handling surfaces

Use `context7` for current library/API docs when technical decisions depend on version-specific behavior.

If the task targets an existing repo or codebase, the first architecture action is a source-backed codebase audit. Do not propose the architecture, Super-Phases, package choices, or rewrite strategy until current structure, conventions, dependencies, tests, runtime flows, and risky surfaces are mapped.

If `docs/architecture/` exists, read it before the codebase audit:

- `docs/architecture/README.md`
- `docs/architecture/ARCHITECTURE.md`
- `docs/architecture/AUDIT-REPORT.md`
- relevant module docs under `docs/architecture/*/`

Use those docs as a map of likely systems, then verify claims against code. Record stale, wrong, missing, or unknown architecture docs in `strategic-design/system-audit.md`.

## Artifact Root

Run `computa-init` when available. Create or reuse the current 4D session under `docs/computa-artifacts/`. If none exists, create one immediately:

- Standalone path: `docs/computa-artifacts/4d-chess/4D-YYYYMMDD-HHMMSS-slug/`
- Export Control child path: `<export-control-session>/4d-chess/4D-YYYYMMDD-HHMMSS-slug/`

Register the session in `docs/computa-artifacts/session-ledger.csv` and gitignore `docs/computa-artifacts/` when it is inside a repo.

Append `session_started` to `docs/computa-artifacts/activity-log.csv` if the 4D session is newly created. Then append `strategic_design_started` before architecting begins and `strategic_design_completed` or `strategic_design_blocked` after architect reviews, with `artifact_path=strategic-design/` and a concrete `next_action`.

Then save:

- `user-task.md`: raw request, timestamp, invocation, repo/path, explicit constraints, permissions, do-not-touch areas, assumptions, and ambiguities.
- `normalized-task.md`: optimized AI-ready task prompt from `computa-speak`.
- `prompt-normalization-log.md`: raw-to-normalized prompt reconciliation.
- `strategic-design/architecture-brief.md`: concise statement of the problem, goals, non-goals, success criteria, and constraints.
- `strategic-design/system-audit.md`: source-backed audit of codebase/product/platform state.
- `strategic-design/spec.md`: functional and technical specification.
- `strategic-design/decision-records.md`: decisions, alternatives considered, rationale, evidence, and reversibility.
- `strategic-design/risk-register.md` and `strategic-design/risk-register.csv`: risks, severity, likelihood, owner, mitigation, verification.
- `strategic-design/dependency-map.md`: prerequisite graph across systems, teams, credentials, dashboards, data, migrations, tests, and deployment.
- `strategic-design/secrets-needed.md`: required or likely API keys, OAuth apps, webhook secrets, model-provider keys, deployment secrets, dashboard credentials, target env/platform paths, and verification blocked until configured. Link each item to `docs/computa-artifacts/secrets-needed/` entries.
- `strategic-design/unknowns.md` and `strategic-design/unknowns.csv`: unknowns, how to resolve them, and whether they block planning.
- `maps/4d-map-index.md`: index of global 4D maps and which Super-Phase will rely on them.
- `maps/4d-map-change-log.md` and `maps/4d-map-change-ledger.csv`: material map/spec updates.

## Architecting Standard

Before proposing Super-Phases:

- audit the current state enough to avoid guessing from filenames, branch names, or chat history
- read existing architecture docs first when present, then verify them against source before relying on them
- for existing codebases, read the repo structure, existing patterns, dependency graph, tests, entrypoints, and runtime flows before designing changes
- identify ownership boundaries and blast radius
- decide the intended architecture, not merely a task list
- decide modular component boundaries and prevent giant-file designs
- call out alternate designs and why they were rejected
- identify edge cases, rollback paths, migration risks, and observability needs
- separate code work from dashboards, databases, infrastructure, deployment, documentation, and manual validation
- identify private configuration early and invoke `computa-secrets-needed` for every API key, OAuth credential, webhook secret, model-provider token, deployment secret, or dashboard credential. Architecture should continue with named env vars, mocks, fakes, provider adapters, contract tests, fixtures, dry-run modes, and placeholder-safe design, and mark only real live-credential verification as blocked.
- distinguish required work from optional optimization
- define evidence needed for each future Super-Phase
- define what must be true before a Super-Phase can start
- identify security/privacy-sensitive surfaces for each future Super-Phase and define how they will be checkpointed, verified, and handed to Export Control final security closeout when this 4D session is nested under Export Control

## Super-Phase Candidates

Produce `strategic-design/super-phase-candidates.md` and `.csv` with:

- candidate ID and name
- objective
- scope and non-scope
- prerequisite candidates
- expected Computa phases inside the Super-Phase
- required source evidence
- tests and runtime QA expected
- external systems touched
- parallelism safety
- rollback/stop conditions
- output artifacts expected
- completion criteria
- security/privacy checkpoint expectations, including any sensitive surfaces that Export Control final security closeout must re-check after all campaigns land

## Architect Reviews

After drafting the strategic design:

1. Run an adversarial architecture review. Challenge scope, sequencing, hidden dependencies, weak assumptions, missing edge cases, missing systems, unsafe parallelism, and unverifiable success criteria.
2. Run a judge/verifier review of the adversarial findings. Classify each finding as correct, partly correct, wrong, or needs more evidence.
3. Update the strategic design only for judge-approved findings.
4. Record both reviews under `strategic-design/reviews/` and update ledgers/maps.

Do not hand off to `computa-4d-chess-build` until the strategic design is approved, approved with explicit risks, or blocked with evidence.
