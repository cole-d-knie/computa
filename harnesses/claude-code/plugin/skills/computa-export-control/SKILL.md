---
name: computa-export-control
description: Top-level Computa intelligence and quarterback skill for massive projects that need research, product/requirements shaping, codebase audit first for existing repos, technology/package/prior-art discovery, skill/MCP/tool intake, and then sequential computa-4d-chess campaigns. Use when the task is broader than one 4D Chess run, when the user wants a research/thought partner, when avoiding reinventing the wheel matters, or when deciding what to build before execution.
---

# Computa Export Control

Use this as the top layer above `computa-4d-chess`.

Hierarchy:

1. `computa-export-control`: research, decide, and quarterback multiple 4D campaigns.
2. `computa-4d-chess`: architect and execute Super-Phases for ultra-long autonomous tasks.
3. `computa-make-no-mistakes`: one-shot medium tasks, debugging/implementation tasks with small-medium scope, edits, additions, and moderate build-from-scratch work.

Export Control is an intelligence layer. Its job is to prevent reinvention, find useful technologies, discover prior art, identify reusable code or packages, recommend helpful skills/MCPs/tools, audit the target codebase, flesh out requirements, and decide the best execution strategy.

If the task targets an existing repo or codebase, audit that codebase before technology recommendations, product architecture, prior-art adaptation, or 4D campaign design. External research must be interpreted against the actual codebase, not against a blank-slate ideal.

## Required Skills

Load and apply these in order:

1. `computa-init`
2. `computa-speak`
3. `computa-execution-queue`
4. `computa-resume` when recovering prior Export Control work
5. `computa-secrets-needed`
6. `computa-export-control-design`
7. `computa-export-control-execute`

During design, use or trigger focused research subskills as needed:

- `computa-export-control-codebase-audit`
- `computa-export-control-product-requirements`
- `computa-export-control-tech-radar`
- `computa-export-control-prior-art`
- `computa-export-control-skill-mcp-intake`
- `computa-export-control-technical-spec`
- `computa-export-control-implementation-strategy`
- `computa-export-control-audit-suite`
- `security-audit`
- `performance-audit`
- `ui-audit`

During design, run `computa-export-control-implementation-strategy` after codebase/research/spec work and before final 4D campaign design when the work has complex engineering issues, provider integrations, missing keys, migrations, concurrency/state risks, unclear testability, or rollout hazards.

During design, run `computa-export-control-audit-suite` after codebase/research/spec work and before final 4D campaign design when a codebase or app exists. The audit suite runs `security-audit`, `performance-audit`, and `ui-audit` in documentation mode, then produces the remediation backlog that 4D campaigns implement.

During execution, each approved campaign must invoke `computa-4d-chess`. Each 4D campaign may then invoke `computa-make-no-mistakes` and must include final `SP-999-post-run-security-audit` before the campaign is marked complete.

## Research Standard

Use current web research when the question depends on current technologies, packages, docs, APIs, examples, pricing, licenses, security status, or ecosystem practice. Prefer primary sources:

- official docs and changelogs
- package registries and repository metadata
- GitHub source, issues, examples, and licenses
- vendor docs for SaaS/APIs/tools
- credible engineering writeups when primary sources are insufficient

Use `context7` for current library/API docs when available. Use browser, web search, Firecrawl, GitHub, package registries, local skill discovery, and MCP/tool discovery when available. If web access or a tool is unavailable, record the gap and mark findings as local-only or stale-risk.

Do not copy public code blindly. Record license, attribution needs, maintenance risk, and compatibility before recommending reuse.

## Artifact Root

Run `computa-init`. Create `docs/` if missing and create or reuse `<invocation-root>/docs/computa-artifacts/` before summarizing the request. If `docs/computa-artifacts/` is inside a git repo, ensure it is ignored by `.gitignore`.

Immediately after raw request capture, run `computa-speak` to create `normalized-task.md` and `prompt-normalization-log.md`. Use `normalized-task.md` as the working prompt for research and campaign design, while preserving `user-task.md` as source truth.

Immediately after `computa-speak`, invoke `computa-execution-queue` and expand the Export Control invocation into root and session-local queue rows before research or execution. The initial expansion must queue init/speak, architecture-docs audit when relevant, codebase audit, product requirements, tech radar, prior art, skill/MCP intake, technical spec when needed, implementation strategy when needed, audit suite for existing apps/codebases, synthesis reviews, campaign design reviews, `computa-export-control-execute`, final reports, and closeout. Add campaign-specific queue rows after campaign design is concrete.

Actual architecture docs live at `docs/architecture/`, as a sibling of `docs/computa-artifacts/`. Do not create the actual architecture docs inside the Export Control session.

If `docs/architecture/` exists, read it before codebase audit, product decisions, technology research, prior-art recommendations, or campaign design. Treat it as orientation and verify it against code. If it is stale or incomplete, record that in `codebase-audit/` and consider invoking `computa-docs-architecture` before final campaign design.

Create a new Export Control session for every invocation:

- `docs/computa-artifacts/export-control/EC-YYYYMMDD-HHMMSS-slug/`

Register it in `docs/computa-artifacts/session-ledger.csv` with `layer=export-control`.

Maintain `docs/computa-artifacts/activity-log.csv` for resume. Append `session_started` when the Export Control session starts, `campaign_started` and `campaign_completed` or `campaign_blocked` as 4D campaigns execute, and `session_completed` or `session_blocked` during closeout.

Inside the Export Control session, at minimum create:

- `user-task.md`: raw request, constraints, permissions, repo/path, assumptions, ambiguities.
- `research-agenda.md`: research questions, source priorities, parallelism plan, and stop conditions.
- `source-ledger.csv`: source URL/path, type, owner, date checked, claim supported, reliability, license notes.
- `decision-matrix.md` and `.csv`: options, evidence, tradeoffs, recommendation, reversibility.
- `requirements/`: product requirements, user journeys, acceptance criteria, non-goals, open questions.
- `codebase-audit/`: architecture map, dependency map, gaps, reusable components, modularity risks.
- `tech-radar/`: packages, SaaS/tools/APIs, framework choices, adopt/trial/avoid decisions.
- `prior-art/`: similar projects, repos, examples, reusable patterns, license assessment.
- `skills-and-tools/`: local/importable skills, MCPs, plugins, connectors, install notes, harness compatibility.
- `technical-spec/`: execution-grade engineering specs: current/target state, module boundaries, component/API/data/integration design, security/privacy, rollout, test strategy, implementation slices, and acceptance contract.
- `implementation-strategy/`: complex engineering challenges, solution approaches, keyless test strategy, integration risk plan, migration/rollout plan, and campaign-readiness analysis before 4D starts.
- `secrets-needed-readout.md`: private config/API key requirements found during research and specs, with links to root `docs/computa-artifacts/secrets-needed/` entries.
- `standalone-audits/`: security/performance/UI audit findings, evidence, recommendations, consolidated remediation backlog, and 4D implementation campaign map.
- `docs-readout/`: whether `docs/architecture/` existed, what was read, stale/missing docs findings, and whether docs were updated or should be updated before execution. This is only a session readout, not the architecture docs themselves.
- `campaigns/`: sequential `computa-4d-chess` campaign plan, prompts, prerequisites, ledgers.
- `4d-chess/`: child 4D Chess sessions created by this Export Control session.
- `reviews/`: adversarial and judge/verifier reviews.
- `reports/`: final synthesis and handoff.
- `execution-queue.csv` and `execution-queue.md`: session-local dependency-aware queue of required child skills, research tasks, reviews, campaigns, and closeout gates.

Artifacts are the source of truth. Context is disposable.

Multiple Export Control sessions may exist in the same project. Never overwrite prior sessions; create a new `EC-...` directory and update the root session ledger.

The root activity log is not a replacement for campaign ledgers. It is the crash-recovery index. Keep the detailed campaign evidence in `campaigns/`, and write only campaign/session-level rows to `activity-log.csv`.

## Operating Rules

- Be creative, but label speculation clearly and tie recommendations to evidence.
- On existing codebases, run and read the codebase audit before deciding requirements, technologies, reuse strategy, or 4D campaigns.
- On existing codebases with `docs/architecture/`, read those docs before the audit and verify their claims instead of trusting them.
- Separate must-have requirements from optional opportunities.
- Prefer small, modular, readable components over giant files or monolithic plans.
- Prefer existing patterns, packages, proven libraries, and reusable code when evidence supports them.
- Do not add dependencies just because they exist; justify fit, maintenance, license, security, size, and integration cost.
- When recommending or designing around an API, SaaS, model provider, OAuth app, webhook, dashboard, deployment platform, or private config requirement, invoke `computa-secrets-needed`. Still design/build as far as possible with named env vars, placeholders, mocks, fakes, provider adapters, contract tests, fixture payloads, dry-run modes, and missing-secret tests; record what cannot be verified until credentials are configured.
- Missing keys should trigger keyless test design, not stalled execution. Do not block 4D campaign design or execution solely because a credential is absent unless that credential is required to make a safe architecture decision and no mock, fixture, docs, sandbox substitute, or owner decision can resolve it.
- Never store actual secret values in Export Control artifacts. Store only names, target env paths, platform targets, code paths, owner actions, and safe `@Computer` handoff prompt paths.
- Distinguish edit-code work from build-from-scratch work, and choose the lightest effective execution layer.
- Keep code, product, design, data, infrastructure, analytics, security, privacy, docs, and release work separated when that reduces risk.
- Record unknowns and blockers instead of smoothing them over.
- Before 4D campaign design, create or explicitly defer a technical spec when the work needs concrete engineering contracts. Do not let broad 4D campaigns proceed from vague product prose.
- Before 4D campaign design, run `computa-export-control-implementation-strategy` when hard engineering problems could affect architecture, sequencing, keyless testability, integration strategy, data model, migration plan, deployment order, or rollback. Do not make 4D improvise through unresolved engineering uncertainty.
- Before 4D campaign design, run `computa-export-control-audit-suite` for existing codebases/apps unless explicitly N/A. Use its remediation backlog and implementation campaign map as source truth for audit-driven 4D work.
- Do not execute 4D Chess campaigns until the export-control design has passed review or is explicitly accepted with documented risk.
- Do not treat a child skill as complete because it was loaded. It is complete only when its queue item and required outputs are complete, deferred with rationale, or blocked with evidence.

## Review Gates

After research synthesis:

1. Run an adversarial review of the requirements, research completeness, source quality, rejected options, package/tool choices, and campaign sequencing.
2. Run a judge/verifier review of the adversarial findings.
3. Update only judge-approved recommendations.

After campaign design:

1. Review every proposed 4D Chess campaign.
2. Review the overall campaign sequence.
3. Mark each campaign as `approved_for_4d`, `approved_with_risk`, `deferred`, or `blocked`.

Do not execute a campaign with unresolved blocking research questions.

## Closeout

Finish with reports that state:

- what was researched
- what was decided and why
- what technologies/packages/tools/skills were recommended or rejected
- what prior art can be reused and under what license constraints
- what the codebase audit found
- what requirements were added or clarified
- what technical specs were produced, approved, deferred, or blocked
- what implementation challenges were solved before 4D, what keyless test strategy was chosen, and what remains risky
- what secrets/private config are needed, where they must be configured, and which verification remains blocked
- what 4D Chess campaigns were executed or left pending
- what remains unknown, risky, blocked, or owner-decision-dependent
- whether `docs/computa-artifacts/activity-log.csv` is current and where `computa-resume` should restart if follow-up is needed
