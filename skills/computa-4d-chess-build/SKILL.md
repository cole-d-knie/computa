---
name: computa-4d-chess-build
description: Build the Computa 4D Super-Phase plan from an audited strategic design/spec for large edits, major system additions, or build-from-scratch projects. Use to create Super-Phase directories, ledgers, maps, modular boundaries, dependencies, handoff prompts, reviews, and execution order before invoking computa-make-no-mistakes.
---

# Computa 4D Chess Build

Use this after `computa-4d-chess-architect`. Build turns the strategic design/spec into an executable Super-Phase system. It creates structure; it does not execute implementation.

## Source Material

Read the 4D artifact root, especially:

- `user-task.md`
- `normalized-task.md`
- existing `docs/architecture/` orientation docs and their current audit status when present
- `strategic-design/architecture-brief.md`
- `strategic-design/system-audit.md`
- `strategic-design/spec.md`
- `strategic-design/decision-records.md`
- `strategic-design/risk-register.md`
- `strategic-design/dependency-map.md`
- `strategic-design/secrets-needed.md` and root `docs/computa-artifacts/secrets-needed/` entries when present
- `strategic-design/super-phase-candidates.md`
- strategic design review outputs

If those do not exist, run `computa-4d-chess-architect` first or create a blocking issue explaining what is missing.

## Build The Super-Phase Tree

Create:

- `super-phases/super-phase-ledger.csv`: every Super-Phase in dependency order with status, prerequisites, artifact path, owner/agent, expected Computa invocation, evidence path, and next action.
- `super-phases/super-phase-plan.md`: narrative plan, sequencing, dependency graph, safe parallelism, stop conditions, rollback strategy, and verification strategy.
- `super-phases/issues-and-blockers.md` and `.csv`: global Super-Phase issues and blockers.
- `super-phases/reviews/`: per-Super-Phase and whole-plan adversarial plus judge/verifier reviews.
- `super-phases/handoff-index.md`: low-context index of every Super-Phase and its invocation prompt.
- `security-audit/`: reserved post-run `/security-audit` gate artifacts, including `invocation.md`, `summary.md`, `issues-and-blockers.md`, `issues-and-blockers.csv`, and `security-audit-ledger.csv`.

For each Super-Phase directory `super-phases/SP-###-slug/`, create:

- `super-phase.md`: objective, scope, non-scope, prerequisites, expected outputs, acceptance criteria, edge cases, risks, rollback, and stop conditions.
- `computa-invocation.md`: exact `/computa-make-no-mistakes ...` prompt for that Super-Phase.
- `input-context.md`: minimum source-truth context a fresh agent needs; reference artifacts by path instead of copying large context.
- `expected-artifacts.md`: required Computa artifact root contents, phase expectations, reports, evidence, and closeout outputs.
- `super-phase-ledger.csv`: local Super-Phase tasks/checkpoints and status.
- `issues-and-blockers.md` and `.csv`: local issues and blockers.
- `evidence-index.md`: expected evidence, commands, screenshots, logs, dashboards, runtime QA, and test outputs.
- `secrets-needed.md`: secrets/private config this Super-Phase needs, target env/platform paths, code paths, safe `@Computer` prompt links, and blocked verification. State `none known` when none are needed.
- `handoff.md`: low-context handoff template for execute/resume.

For every created Super-Phase, append `super_phase_created` to the root `docs/computa-artifacts/activity-log.csv` with `artifact_path` pointing at the Super-Phase directory and `next_action` naming the first prerequisite or review step.

Also create mandatory final Super-Phase `super-phases/SP-999-post-run-security-audit/` and include it in `super-phases/super-phase-ledger.csv`.

`SP-999-post-run-security-audit` requirements:

- depends on every implementation Super-Phase
- uses the same Super-Phase artifact files as other Super-Phases
- `computa-invocation.md` must invoke `/computa-make-no-mistakes` and instruct it to run `/security-audit` in 4D final Super-Phase implementation mode
- creates or updates `<4D-session>/security-audit/` and `reports/security-audit.md`
- records branch/progress file/commit range for the security audit
- updates maps, ledgers, architecture docs, and final reports after any security changes
- runs Super-Phase adversarial review followed by judge/verifier review
- must be complete, explicitly N/A, or blocked/deferred with evidence and owner acceptance before 4D `session_completed`

## Super-Phase Design Rules

- A Super-Phase is a complete multi-phase Computa plan, not a normal task.
- Each Super-Phase must be independently runnable through `/computa-make-no-mistakes`.
- Each Super-Phase must produce its own Phase 0, maps, investigation, TDD/QA, swarms, closeout, and reports inside its Computa artifact root.
- The overall 4D plan must include `SP-999-post-run-security-audit` as the final Super-Phase after all implementation Super-Phases and before 4D `session_completed`. This is not a replacement for Super-Phase security reviews; it is the final whole-codebase hardening pass orchestrated through `/computa-make-no-mistakes`.
- Keep Super-Phase prompts concise but complete enough for a fresh agent to execute without chat history.
- When architecture docs exist, include references to the relevant docs and audit status in Super-Phase `input-context.md`, but require the nested Computa run to verify source truth.
- Do not create overlapping Super-Phases unless the dependency order prevents simultaneous execution.
- Separate dashboards, database/migrations, infrastructure, code, docs, QA, and release work when overlap would create risk.
- Keep implementation boundaries modular. Super-Phase prompts should discourage giant files and call out expected component/module splits.
- Include `computa-secrets-needed` in Super-Phase prompts whenever the Super-Phase touches API keys, provider tokens, OAuth/webhook credentials, deployment secrets, dashboard accounts, or private config. Do not block planning just because credentials are missing; require placeholder-safe implementation and explicit blocked-verification records.
- Encode dependencies explicitly. No dependent Super-Phase may start before prerequisite evidence exists.
- Preserve rejected, merged, split, and superseded Super-Phase candidates in a history section or ledger.

## Review Gates

After each Super-Phase is created:

1. Run one adversarial reviewer for that Super-Phase.
2. Run one judge/verifier for that adversarial review.
3. Implement only judge-approved revisions.
4. Record review outputs in the Super-Phase directory and in `super-phases/reviews/`.

After all Super-Phases are created:

1. Run an adversarial review of the overall Super-Phase plan.
2. Run a judge/verifier review of that adversarial review.
3. Update the plan only for judge-approved recommendations.
4. Mark the full plan as `approved_for_execution`, `approved_with_risks`, or `blocked`.

Do not hand off to `computa-4d-chess-execute` until the overall Super-Phase plan has passed this review gate or is explicitly accepted with documented risk.

After the full plan is approved, append an activity-log row with `event_type=super_phase_plan_approved`, `scope_type=super_phase_plan`, `artifact_path=super-phases/super-phase-plan.md`, and a `next_action` that tells `computa-resume` whether execution can start or remains blocked.
