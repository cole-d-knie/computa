---
name: computa-export-control-implementation-strategy
description: Focused Computa Export Control implementation-strategy skill for solving complex engineering challenges before launching computa-4d-chess campaigns. Use after codebase audit, research, technical specs, and audit-suite findings but before campaign design/execution, especially when the work has difficult integration choices, missing API keys/secrets, risky migrations, concurrency/state problems, unclear testability, provider mocks, deployment sequencing, or architecture tradeoffs that must be reasoned through before 4D execution.
---

# Computa Export Control Implementation Strategy

Use this before Export Control launches `computa-4d-chess` campaigns. Its job is to turn hard engineering uncertainty into a concrete implementation strategy that 4D can execute without guessing.

This skill does not implement product code unless the user explicitly asks for a tiny spike/proof artifact. It designs the approach, proves what can be proven safely, and marks only true blockers.

## Inputs

Read:

- `user-task.md`
- `normalized-task.md`
- `requirements/`
- `codebase-audit/`
- `tech-radar/`
- `prior-art/`
- `skills-and-tools/`
- `technical-spec/`
- `standalone-audits/`
- `decision-matrix.md` and `.csv`
- `recommended-design.md`
- `secrets-needed-readout.md`
- root `docs/computa-artifacts/secrets-needed/secrets-needed.csv` when present
- relevant source files, tests, configs, env examples, deployment files, provider docs, architecture docs, and logs

If required inputs are missing, create a precise blocker or run the missing Export Control subskill first. Do not invent an implementation strategy from chat memory.

## Activity Log

When `docs/computa-artifacts/activity-log.csv` exists, append:

- `implementation_strategy_started` before analysis
- `implementation_strategy_completed`, `implementation_strategy_blocked`, or `implementation_strategy_deferred` after review

Use `scope_name=implementation-strategy`, `artifact_path=implementation-strategy/strategy-index.md`, and set `next_action` to the exact campaign-design or blocker step.

## Output Directory

Write under `implementation-strategy/` in the current Export Control session:

- `strategy-index.md`: reading order, status, source inputs, and owner decisions.
- `engineering-challenges.md`: hard implementation problems, why they are hard, affected systems, and evidence.
- `challenge-ledger.csv`: challenge ID, scope, severity, dependency, decision needed, strategy, evidence path, status.
- `solution-approaches.md`: candidate implementation approaches, tradeoffs, rejected approaches, fallback paths, and reversibility.
- `spike-plan.md`: tiny safe spikes or proofs that can reduce risk before 4D, including what can be proven without production credentials.
- `keyless-test-strategy.md`: how to test without API keys or private config using mocks, fakes, contract tests, fixtures, provider SDK stubs, recorded schemas, dry-run modes, local emulators, synthetic webhooks, env-validation tests, and negative-path tests.
- `integration-risk-plan.md`: external services, auth, webhooks, rate limits, idempotency, retries, error handling, observability, and degradation.
- `migration-and-rollout-plan.md`: deploy order, flags, backcompat, rollback, data repair, and production safety.
- `campaign-readiness.md`: what each 4D campaign must know before starting, what remains unknown, and what must be verified inside 4D.
- `implementation-strategy-ledger.csv`: section, status, source evidence, reviewer, blockers, and next action.

Only create sections that are relevant, but `strategy-index.md`, `engineering-challenges.md`, `solution-approaches.md`, `keyless-test-strategy.md`, `campaign-readiness.md`, and `implementation-strategy-ledger.csv` are required.

## Strategy Standard

- Treat missing API keys or private config as a test-design problem, not a reason to stop design or implementation planning.
- Do not let a missing key block 4D campaign design unless the key is required to choose the architecture safely and no mock, contract, fixture, docs, local emulator, sandbox substitute, or owner decision can resolve the choice.
- For every secret-dependent feature, define what can be tested before credentials exist and what must be verified after credentials are configured.
- Prefer small adapters around external providers so mocks, fakes, and contract tests can exercise the rest of the system without live credentials.
- Define failure-mode behavior for missing, invalid, revoked, expired, rate-limited, or permission-limited credentials.
- Identify complex engineering issues before 4D starts: data modeling, state machines, migrations, concurrency, auth boundaries, caching, queues, background jobs, idempotency, provider semantics, deployment ordering, observability, and rollback.
- Convert uncertainty into explicit 4D instructions, prerequisite evidence, test requirements, and stop conditions.
- Do not over-plan trivial work. Use this skill when complexity or uncertainty would otherwise make 4D campaigns improvise.

## Review Gate

Before Export Control creates or launches 4D campaigns:

1. Run adversarial review of engineering challenges, solution approaches, keyless test strategy, integration risks, migration/rollout plan, and campaign readiness.
2. Run judge/verifier review of the adversarial findings.
3. Update only judge-approved recommendations.
4. Mark implementation strategy `approved_for_campaign_design`, `approved_with_risks`, `deferred`, or `blocked` in `strategy-index.md` and `implementation-strategy-ledger.csv`.

Do not launch 4D campaigns when a complex engineering challenge remains unresolved and could materially change the campaign sequence, architecture, data model, provider integration, or test strategy.
