---
name: swarm-verify-closeout
description: "Close out swarm-verified work with evidence: reconcile ledgers, verify original request coverage, create final Markdown reports, document verification still needed, blockers, open issues, gaps, new fixed and unfixed issues, commits, and no-push status."
---

# Swarm Verify Closeout

Use this before claiming the task is done.

Use `verification-before-completion` when available.

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

Golden rule: evidence before assertions. Never say "it works" without verification command output and runtime proof.
