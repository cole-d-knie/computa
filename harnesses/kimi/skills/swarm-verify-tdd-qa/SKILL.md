---
name: swarm-verify-tdd-qa
description: "Apply test-driven development and runtime QA for swarm-verified work: failing tests before implementation, minimal fixes, passing tests after, edge cases, unit/integration/smoke checks, live API or UI verification, and Playwright for browser-visible behavior."
---

# Swarm Verify TDD QA

Use this for every implementation task that changes behavior.

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

## TDD Rule

Use `test-driven-development` when available.

No production code for behavior changes until there is one of:

- a failing test that proves the issue or missing behavior
- a documented reason a failing pre-fix test is impossible, plus alternate baseline evidence

Do not claim a fix is complete unless failing-before and passing-after evidence exists, or the exception is documented.

## Verification Loop

For every meaningful code change:

1. Read relevant files and existing tests.
2. Identify edge cases before coding.
3. Add or update tests first.
4. Confirm the test fails or the bug reproduces.
5. Implement the smallest fix.
6. Re-run the same tests and prove they pass.
7. Run repo verification.
8. Run smoke/runtime QA when relevant.
9. Update ledgers with command output and evidence paths.

Do not over-engineer. Solve the verified behavior and edge cases.

## Default Commands

Try these when appropriate:

```bash
pnpm check
pnpm build
pnpm test
pnpm lint
```

If the repo uses different commands, identify equivalents first, document them, and run those.

If any step fails, read the error, fix the root cause, re-run verification, and do not proceed with a failing suite unless the failure is documented as unrelated and approved by the task evidence.

## Required Test Coverage

Use the level of coverage that matches risk:

- unit tests for changed logic
- integration tests for cross-module behavior
- smoke tests for primary flows
- edge-case tests for boundary conditions, invalid inputs, races, permissions, empty/loading states, retries, duplicate actions, and regression-prone flows
- runtime checks for actual app/service behavior

## Live QA

When relevant:

- If an API changed, hit the endpoint.
- If a UI/dashboard changed, start the service and smoke-test the route.
- If docs, PDFs, generated files, or reports changed, open/render them and verify output.
- If behavior is browser-visible, use `playwright` with real interaction, console/network checks, screenshots, and visible state checks.

Do not parallelize runtime QA against a shared server, browser profile, database, queue, or external console unless isolated environments are created.
