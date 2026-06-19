# Swarm Verify Agent Instructions

Use these instructions when the harness does not support native `SKILL.md` discovery.

When the user asks for swarm verification, phased TDD execution, adversarial review, judge/verifier review, runtime QA, or audit-ready implementation:

1. Immediately save the raw user request to an external `user-task.md`.
2. Create an external artifact root with `plan.md`, `master-task-ledger.csv`, issue/blocker Markdown and CSV ledgers, phase directories, task directories, subtask ledgers, evidence logs, `maps/`, and `reports/`.
3. When any swarm-verify phase or subworkflow is run independently, use the same available dependency capabilities: terse communication, planning, TDD, investigation, parallel agents, adversarial review, completion verification, Playwright/browser QA, and Context7/current docs.
4. Run Phase 1 orientation audit before implementation: create `maps/map-index.md`, `task-scope-map.md`, `codebase-map.md`, `flow-map.md`, `test-and-command-map.md`, `risk-map.md`, `map-change-log.md`, and `map-change-ledger.csv`.
5. Run Phase 2 investigation before implementation: reference and update the maps, verify source truth, current behavior, expected behavior, issue origin, edge cases, baseline commands, and failing evidence.
6. Use TDD for behavior changes: failing test first, smallest fix, passing test after.
7. Run unit, integration, smoke, runtime, and browser-visible QA as relevant.
8. Use safe parallelism only for independent review/investigation/test-reading work. Do not parallelize overlapping files, shared runtime state, dashboards, databases, deployments, migrations, or dependent subtasks.
9. After every task, run one adversarial reviewer per subtask and one judge/verifier per subtask. Only implement judge-approved recommendations.
10. After every phase, run one adversarial reviewer per task and one judge/verifier per task. Do not close the phase until each task is approved complete, approved deferred, or blocked with evidence.
11. Keep ledgers and maps current. Maps may change at any time as work reveals new information; track every material map update in both `maps/map-change-log.md` and `maps/map-change-ledger.csv`. Mark items done only after evidence exists.
12. Create final Markdown reports for summary, verification still needed, blockers/open issues, original-task gap analysis, map artifacts and map-change coverage, and new issues found split fixed vs not fixed.
13. Make one commit per completed task only after verification passes and commits are allowed. Do not push unless explicitly asked.

Golden rule: evidence before assertions. Never claim work is complete without verification command output and runtime proof.
