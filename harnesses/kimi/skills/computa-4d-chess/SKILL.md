---
name: computa-4d-chess
description: One-shot Computa super-phase entrypoint for ultra-long autonomous tasks, large edits, major system additions, full-stack builds from scratch, or very broad ambiguous work. Use when the task is too broad for one normal computa-make-no-mistakes run and needs codebase audit first for existing repos, then architecture, system design, audited decisions, Super-Phase planning, and execution of each Super-Phase through computa-make-no-mistakes.
---

# Computa 4D Chess

Use this as the one-shot entrypoint for work that needs one level above Computa phases: ultra-long autonomous tasks, large system changes, large code edits, or major build-from-scratch projects.

Before architecture, execution, and closeout, follow the hook-enforced Computa execution contract when available: `templates/computa-execution-contract.md`. If hook validation reports missing child rows, active rows, or broken artifact shape, correct the queue/artifacts before claiming progress.

For massive research/strategy work that should decide what technologies, packages, prior art, tools, or requirements to use before 4D execution, use `computa-export-control`.

Computa creates and executes phases. 4D Chess creates and executes Super-Phases. A Super-Phase is a complete multi-phase Computa plan with its own inputs, acceptance criteria, artifact root, ledgers, maps, evidence, reviews, and closeout.

Treat the user's text after the skill name as the task. If the task is too vague to safely plan, ask only for the blocking objective, repo/path, expected outcome, and constraints. Otherwise start.

## Required Skills

Load and apply these skills in order:

1. `computa-init`
2. `computa-speak`
3. `computa-execution-queue`
4. `computa-resume` when recovering prior 4D work
5. `computa-secrets-needed`
6. `computa-4d-chess-architect`
7. `computa-4d-chess-build`
8. `computa-4d-chess-execute`

During execution, each Super-Phase must invoke `computa-make-no-mistakes`.

Also use or emulate the Computa dependency set when available: `caveman`, `using-superpowers`, `writing-plans`, `executing-plans`, `test-driven-development`, `systematic-debugging` or `investigate`, `dispatching-parallel-agents`, `subagent-driven-development`, `requesting-code-review`, `verification-before-completion`, `playwright`, and `context7`.

If a dependency is missing, continue with equivalent behavior and record it in the Super-Phase artifact ledger.

## One-Shot Workflow

1. Run `computa-init` so `docs/` and `docs/computa-artifacts/` exist.
2. Save the raw request, then run `computa-speak` to create `normalized-task.md` and use that as the downstream working prompt.
3. Invoke `computa-execution-queue` and expand the 4D invocation into root and session-local queue rows before architecture or build work.
4. If `docs/architecture/` exists, read it first for orientation before architecture decisions, then verify claims against code during the codebase audit.
5. If a repo/codebase exists, run a codebase audit before architecture decisions. Do not design Super-Phases from chat context or desired architecture alone.
6. Run `computa-4d-chess-architect` to audit, map, spec, decide, and produce the strategic architecture.
7. Run `computa-4d-chess-build` to create the Super-Phase architecture and artifact tree, then replace generic Super-Phase queue placeholders with explicit rows for every Super-Phase.
8. Review each created Super-Phase with an adversarial reviewer, then a judge/verifier.
9. Review the full Super-Phase plan with an adversarial reviewer, then a judge/verifier.
10. Run `computa-4d-chess-execute` to execute each approved Super-Phase by consuming the queue and invoking `/computa-make-no-mistakes`.
11. After every Super-Phase execution, run Super-Phase-level adversarial review, then judge/verifier review.
12. Finish with a 4D security/privacy checkpoint that records touched sensitive surfaces, unresolved risks, and whether anything must be handed to the parent Export Control final security closeout. Do not run the full `/security-audit` from normal 4D closeout unless the user explicitly asked for that standalone audit.
13. Finish with 4D closeout reports that synthesize all Super-Phase Computa closeouts, checkpoints, and handoff items into one low-context handoff.

## 4D Operating Principles

- Context is disposable; artifacts are the source of truth.
- Save the raw user request before summarizing or planning.
- Run `computa-speak` after raw request capture and before architecture analysis. Use `normalized-task.md` for downstream planning while preserving `user-task.md` as source truth.
- Create `docs/` if missing, then create or reuse `<invocation-root>/docs/computa-artifacts/`.
- Keep actual architecture docs at `docs/architecture/`, not under `docs/computa-artifacts/`.
- If this is a standalone 4D run, create `docs/computa-artifacts/4d-chess/4D-YYYYMMDD-HHMMSS-slug/`.
- If invoked by Export Control, create the 4D session under the parent Export Control session at `.../4d-chess/4D-.../`.
- Register the 4D session in `docs/computa-artifacts/session-ledger.csv` with its parent session ID when applicable.
- Maintain `docs/computa-artifacts/activity-log.csv`. Append `session_started` when the 4D session starts, `super_phase_created` when a Super-Phase is created, `super_phase_started` and `super_phase_completed` during execution, and `session_completed` or `session_blocked` at closeout.
- Maintain root and session-local `execution-queue.csv` through `computa-execution-queue`. Queue rows must make child skill invocation, Super-Phase execution, review gates, docs hooks, security/privacy checkpoints, and closeout visible. Execute the highest-priority unblocked queue item, not the most recent chat impulse.
- Before `session_completed`, verify the 4D security/privacy checkpoint is current. If this 4D session is a child of Export Control, hand off security-sensitive findings to the Export Control final security closeout instead of launching a full 4D-local `/security-audit`.
- If `docs/computa-artifacts/` is inside a git repo, ensure it is ignored by `.gitignore`.
- Use maps, ledgers, issue logs, blocker logs, decision records, and evidence directories.
- Prefer low-context handoffs: every Super-Phase must be executable by a fresh agent with only its directory.
- Do not assume. Verify from source files, docs, PRs, tests, logs, dashboards, runtime behavior, and user constraints.
- If `docs/architecture/` exists, read it before Super-Phase architecture work and record whether it was verified, stale, missing coverage, or useful for planning.
- On existing codebases, audit current structure, patterns, dependencies, tests, and runtime flows before deciding the target architecture.
- Plan dependencies explicitly. Do not execute dependent Super-Phases before prerequisites are complete.
- Use safe parallelism only for independent Super-Phases with non-overlapping files, systems, data, dashboards, databases, browsers, queues, environments, and deployment state.
- Preserve superseded plans and decisions; never erase audit history.
- Prefer small, modular, readable components over gigantic files. Super-Phases should preserve clear component boundaries and should not encourage monolithic implementation.
- Build and execute Super-Phases as far as possible even when API keys, OAuth credentials, webhook secrets, model-provider tokens, deployment secrets, or dashboard/private config are missing. A missing key is not a valid reason to skip a Super-Phase unless the key is required to choose the architecture safely and no mock, fixture, docs, sandbox substitute, or owner decision can resolve the choice. Use `computa-secrets-needed` to record the required secrets, target env/platform paths, code paths, blocked verification, and safe `@Computer` handoff prompts. Do not store actual secret values.
- Every secret-dependent Super-Phase must define keyless tests before execution: mocks/fakes, provider adapters, contract tests, fixture payloads, synthetic webhooks/events, dry-run paths, env-validation tests, and negative-path behavior for missing/invalid credentials. Only live provider calls and dashboard-side checks may remain blocked by the missing key.
- Do not push unless explicitly asked.
- Do not use broad staging commands such as `git add .`, `git add -A`, `git add --all`, `git add -u`, or `git add :/`. Stage intentional files explicitly.
- Do not mark a skill, Super-Phase, or session complete while its required queue rows are still queued, ready, running, or review_needed.

## Closeout Bar

Do not claim the 4D task is complete until:

- every Super-Phase is complete, approved deferred, or blocked with evidence
- each Super-Phase has its own Computa closeout
- the 4D master ledgers are current
- all Super-Phase reviews and full-plan reviews are recorded
- maps and map-change ledgers are current
- root `activity-log.csv` records Super-Phase creation/start/finish/block events and the final 4D session status
- `reports/security-and-privacy-checkpoint.md` or equivalent security checkpoint artifacts identify touched security/privacy surfaces, unresolved risks, and Export Control handoff items
- root and session-local execution queues agree that no required child skill, Super-Phase, review gate, docs hook, or closeout item remains active
- existing architecture docs were read first when present and were verified, updated through nested Computa docs hooks, or documented as stale/blocked
- `docs/computa-artifacts/secrets-needed/` is current for all Super-Phases, including any runtime/deploy verification blocked by missing private config
- final reports explain what was done, what needs verification, current blockers, open issues, gaps versus the original request, new issues found and fixed, and new issues found but not fixed
- `computa_hooks.py validate --strict` and `validate --closeout --strict` pass, or the final report lists the exact queue/artifact blockers

Golden rule: evidence before assertions. Never say "it works" without verification and runtime proof.
