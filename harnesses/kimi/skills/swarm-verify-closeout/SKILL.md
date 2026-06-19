---
name: swarm-verify-closeout
description: "Close out swarm-verified work with evidence: reconcile ledgers, verify original request coverage, create final Markdown reports, document verification still needed, blockers, open issues, gaps, new fixed and unfixed issues, commits, and no-push status."
---

# Swarm Verify Closeout

Use this before claiming the task is done.

Use `verification-before-completion` when available.

## Required Dependency Skills

When this subskill is invoked directly, use or trigger all Kimi-compatible swarm-verify dependencies when available:

- `caveman`: terse, concrete communication.
- `using-superpowers`: start-of-task planning discipline.
- `writing-plans` and `executing-plans`: plan creation and execution.
- `test-driven-development`: fail-first implementation.
- `systematic-debugging` or `investigate`: root-cause investigation.
- `dispatching-parallel-agents` or Kimi agent swarm/delegation: safe swarm parallelism.
- `requesting-code-review`: adversarial review.
- `verification-before-completion`: completion proof.
- `playwright`: browser-visible runtime QA.
- `context7`: current, version-specific docs for libraries, frameworks, APIs, CLIs, and harness behavior.

If any dependency is missing, continue with equivalent behavior and record the missing dependency in the artifact ledger.

## Reconcile Scope

Before writing the final answer:

- re-read `user-task.md`
- re-read all plan, phase, task, subtask, issue, blocker, and evidence ledgers
- confirm every phase/task/subtask is done or explicitly deferred with rationale
- compare completed work to the original user request
- identify satisfied, partially satisfied, missing, deferred, and out-of-scope items

## Final Reports

Create concise but substantive Markdown reports under the external artifact root, preferably in `reports/`.

Required report substance:

- `final-summary.md`: what was done, why it was done, important changes, important evidence paths, and final status.
- `verification-needed.md`: what still needs verification, who/what can verify it, and whether it blocks completion or merge.
- `blockers-and-open-issues.md`: current blockers, unresolved open issues, risks, and next actions.
- `task-gap-analysis.md`: compare `user-task.md` against completed work; list satisfied, partially satisfied, missing, deferred, and out-of-scope items.
- `map-artifacts.md`: map files created, map change ledger/log coverage, important updates, unresolved unknowns, map gaps, and which maps should be read first for follow-up work.
- `new-issues-found.md`: all new issues discovered during the work, split into fixed and not fixed, with evidence and rationale.

Reports may be combined only when that makes them clearer, but every category above must remain present as explicit headings.

## Verification Evidence

Do not claim done unless you can provide:

- exact verification commands and passing output
- failing pre-fix evidence or documented reason it was impossible
- passing post-fix evidence
- smoke/runtime QA performed
- Playwright verification if browser-visible behavior was involved
- edge cases covered
- paths to plan, phase, task, subtask, issue, blocker, evidence, and report artifacts
- paths to map artifacts and any map gaps or stale-map risks
- paths to `maps/map-change-log.md` and `maps/map-change-ledger.csv`

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

Golden rule: evidence before assertions. Never say "it works" without verification command output and runtime proof.
