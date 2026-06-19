# Swarm Verify Agent Instructions

Use these instructions when the harness does not support native `SKILL.md` discovery.

When the user asks for swarm verification, phased TDD execution, adversarial review, judge/verifier review, runtime QA, or audit-ready implementation:

1. Immediately save the raw user request to an external `user-task.md`.
2. Create an external artifact root with `plan.md`, `master-task-ledger.csv`, issue/blocker Markdown and CSV ledgers, phase directories, task directories, subtask ledgers, evidence logs, and `reports/`.
3. Run Phase 1 investigation before implementation: verify source truth, current behavior, expected behavior, issue origin, edge cases, baseline commands, and failing evidence.
4. Use TDD for behavior changes: failing test first, smallest fix, passing test after.
5. Run unit, integration, smoke, runtime, and browser-visible QA as relevant.
6. Use safe parallelism only for independent review/investigation/test-reading work. Do not parallelize overlapping files, shared runtime state, dashboards, databases, deployments, migrations, or dependent subtasks.
7. After every task, run one adversarial reviewer per subtask and one judge/verifier per subtask. Only implement judge-approved recommendations.
8. After every phase, run one adversarial reviewer per task and one judge/verifier per task. Do not close the phase until each task is approved complete, approved deferred, or blocked with evidence.
9. Keep ledgers current and mark items done only after evidence exists.
10. Create final Markdown reports for summary, verification still needed, blockers/open issues, original-task gap analysis, and new issues found split fixed vs not fixed.
11. Make one commit per completed task only after verification passes and commits are allowed. Do not push unless explicitly asked.

Golden rule: evidence before assertions. Never claim work is complete without verification command output and runtime proof.
