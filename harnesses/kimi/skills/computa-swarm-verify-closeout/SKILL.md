---
name: computa-swarm-verify-closeout
description: "Close out computa-swarm-verified work with evidence: reconcile ledgers, verify original request coverage, create final Markdown reports, document verification still needed, blockers, open issues, gaps, modularity/readability status, new fixed and unfixed issues, commits, and no-push status."
---

# Computa Swarm Verify Closeout

Use this before claiming the task is done.

Use `verification-before-completion` when available.

## Required Dependency Skills

When this subskill is invoked directly, use or trigger all computa-swarm-verify dependencies when available:

- `caveman`: terse, concrete communication.
- `computa-secrets-needed`: safe ledger and handoff prompts for missing API keys, OAuth credentials, webhook secrets, model-provider keys, and deployment secrets.
- `using-superpowers`: start-of-task planning discipline.
- `writing-plans` and `executing-plans`: plan creation and execution.
- `test-driven-development`: fail-first implementation.
- `systematic-debugging` or `investigate`: root-cause investigation.
- native agent swarm/delegation: safe swarm parallelism.
- `requesting-code-review`: adversarial review.
- `verification-before-completion`: completion proof.
- `playwright`: browser-visible runtime QA.
- `context7`: current, version-specific docs for libraries, frameworks, APIs, CLIs, and harness behavior.

If any dependency is missing, continue with equivalent behavior and record the missing dependency in the artifact ledger.

## Reconcile Scope

Before writing the final answer:

- re-read `user-task.md`
- re-read `normalized-task.md` and `prompt-normalization-log.md` when present
- re-read all plan, phase, task, subtask, issue, blocker, and evidence ledgers
- re-read root `docs/computa-artifacts/activity-log.csv`
- re-read `docs/computa-artifacts/secrets-needed/secrets-needed.csv` and related per-secret Markdown files when they exist
- confirm every phase/task/subtask is done or explicitly deferred with rationale
- compare completed work to the original user request
- identify satisfied, partially satisfied, missing, deferred, and out-of-scope items
- append `session_completed` or `session_blocked` to `activity-log.csv` before the final response, with the final report path and exact next action

## Final Reports

Create concise but substantive Markdown reports under the current `docs/computa-artifacts/` session, preferably in `reports/`.

Required report substance:

- `final-summary.md`: what was done, why it was done, important changes, important evidence paths, and final status.
- `verification-needed.md`: what still needs verification, who/what can verify it, and whether it blocks completion or merge.
- `blockers-and-open-issues.md`: current blockers, unresolved open issues, risks, and next actions.
- `task-gap-analysis.md`: compare `user-task.md` against completed work; list satisfied, partially satisfied, missing, deferred, and out-of-scope items.
- `map-artifacts.md`: map files created, map change ledger/log coverage, important updates, unresolved unknowns, map gaps, and which maps should be read first for follow-up work.
- `architecture-docs-status.md`: whether `docs/architecture/` was created, updated, no-op, or blocked; exact docs paths changed; stale or missing architecture docs; and whether docs are current enough for follow-up planning.
- `secrets-needed.md`: all required API keys/private config, target env files, platform secret targets, related code paths, safe `@Computer` prompt paths, status, and verification blocked until configuration. State clearly when no secrets are needed.
- `new-issues-found.md`: all new issues discovered during the work, split into fixed and not fixed, with evidence and rationale.
- `modularity-readability.md`: component/file structure, large-file risks, responsibility boundaries, and any follow-up splits recommended.

Reports may be combined only when that makes them clearer, but every category above must remain present as explicit headings.

## Verification Evidence

Do not claim done unless you can provide:

- exact verification commands and passing output
- failing pre-fix evidence or documented reason it was impossible
- passing post-fix evidence
- smoke/runtime QA performed
- Playwright verification if browser-visible behavior was involved
- edge cases covered
- whether implementation stayed small, modular, readable, and consistent with project boundaries
- paths to plan, phase, task, subtask, issue, blocker, evidence, and report artifacts
- path to `docs/computa-artifacts/activity-log.csv` and whether it is current enough for `computa-resume`
- paths to map artifacts and any map gaps or stale-map risks
- paths to `maps/map-change-log.md` and `maps/map-change-ledger.csv`
- paths to architecture docs, docs audit report, docs update ledger, and any remaining docs gaps
- paths to `docs/computa-artifacts/secrets-needed/`, the secrets ledger, per-secret Markdown files, and remaining private-config verification blockers

If verification could not be run, document why, what risk remains, and what command or manual check should be run next.

## Commits And Pushes

- Make one commit per completed task when commits are allowed.
- Commit only after task verification passes.
- Use concise Conventional Commits: `type(scope): subject`.
- Keep subject <= 50 chars.
- Use a body only when the why is not obvious.
- Do not push unless explicitly asked.

## Final Response

Keep the final response concise and evidence-backed.

Include:

- what changed
- what was tested
- final status
- remaining risks, blockers, gaps, or deferred items
- new issues found and fixed
- new issues found but not fixed
- whether anything needs manual verification
- artifact/report paths
- map artifact paths and whether the map is current
- map change log/ledger paths and whether all material map changes were tracked
- architecture docs status and whether `docs/architecture/AUDIT-REPORT.md` is current enough for handoff
- secrets-needed status, including whether missing private config blocks runtime/deploy verification
- activity-log status and the latest resume point, especially if anything remains blocked or deferred

Golden rule: evidence before assertions. Never say "it works" without verification command output and runtime proof.
