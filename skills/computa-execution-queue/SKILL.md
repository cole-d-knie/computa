---
name: computa-execution-queue
description: Create and maintain Computa dependency-aware execution queues for Export Control, 4D Chess, Computa Make No Mistakes, and nested skill invocations. Use whenever a Computa skill starts, expands child skills, resumes work, or decides the next safe item to execute.
---

# Computa Execution Queue

Use this as the shared queue manager for every Computa layer.

Also follow `templates/computa-execution-contract.md` from the Computa repo when available. That contract is the hook-enforced source for recursive routing, terminal child completion, artifact shape, and safe git staging.

The queue turns skill prose into an explicit execution graph. A skill invocation is not complete just because the skill was loaded. When a top-level or orchestration skill starts, it must expand its expected child skills, phases, review gates, docs hooks, and closeout gates into the queue before executing them.

## Queue Files

Create or reuse these root files under the invocation root:

- `docs/computa-artifacts/execution-queue.csv`
- `docs/computa-artifacts/execution-queue.md`

When a session has its own detailed plan, also create a session-local queue:

- `<session>/execution-queue.csv`
- `<session>/execution-queue.md`

The root queue is the cross-session resume index. Session-local queues are the detailed source truth for that session. Keep both aligned when queue items start, finish, block, defer, or materially change.

## CSV Header

Use this exact header:

`queue_id,parent_queue_id,session_id,layer,scope_type,scope_id,scope_name,skill,action,priority,status,dependencies,non_overlap_key,allowed_parallelism,required_outputs,review_gate,artifact_path,evidence_path,next_action,created_at,started_at,completed_at,notes`

## Status Values

Use only:

- `queued`
- `ready`
- `blocked`
- `running`
- `review_needed`
- `complete`
- `deferred`
- `failed`
- `superseded`

## Queue Semantics

The queue is not FIFO. It is a dependency-aware run queue.

Before choosing work:

1. Read root `execution-queue.csv`.
2. Read the current session-local queue when present.
3. Ignore `complete`, `deferred`, `superseded`, and unrelated-session rows unless they block dependencies.
4. Mark a queued item `ready` only when all dependencies are complete or accepted deferred.
5. Choose the highest-priority ready item whose `non_overlap_key` does not conflict with another running item.
6. Prefer explicit user-priority and dependency order over row order.
7. Never start work whose prerequisites are incomplete, ambiguous, or only assumed complete.

## Skill Invocation Expansion

Every orchestration skill invocation must add its expected child work to the queue before executing child work.

Expansion rules:

- Add one queue item for every child skill that must run.
- Add one queue item for every review gate.
- Add one queue item for every docs/update hook.
- Add one queue item for every campaign, Super-Phase, phase, and task that is already known.
- Add placeholder queue items for not-yet-designed child work only when the parent cannot know the final children yet. Replace placeholders with concrete rows after design/build.
- Include `required_outputs` for ledgers, reports, tests, commits, docs, screenshots, or platform evidence expected from the item.
- Include `dependencies` as queue IDs, not prose, whenever possible.
- Include `non_overlap_key` for files, modules, databases, dashboards, browsers, deployments, migrations, queues, or external accounts that must not be touched concurrently.
- Include `allowed_parallelism` as `serial`, `parallel_safe`, or `coordinator_only`.
- Include `review_gate` as `none`, `adversarial`, `judge_verifier`, or `adversarial_then_judge`.

If a queue item is generated incorrectly, do not erase it. Mark it `superseded`, explain why in `notes`, and add corrected rows.

## Required Expansions

When `/computa-export-control` starts, queue at least:

- `computa-init`
- `computa-speak`
- `computa-docs-architecture-audit` when `docs/architecture/` exists
- `computa-export-control-codebase-audit` for existing codebases
- `computa-export-control-product-requirements`
- `computa-export-control-tech-radar`
- `computa-export-control-prior-art`
- `computa-export-control-skill-mcp-intake`
- `computa-export-control-technical-spec` when engineering contracts are needed
- `computa-export-control-implementation-strategy` when complexity, migrations, integrations, keys, rollout, or hard engineering risks exist
- `computa-export-control-audit-suite` for existing apps/codebases unless explicitly N/A
- research synthesis adversarial review
- research synthesis judge/verifier review
- campaign design
- per-campaign review gates
- `computa-export-control-execute`
- final Export Control security closeout through `computa-make-no-mistakes` invoking `security-audit` when a codebase/app exists, campaigns touched security/privacy-sensitive surfaces, or the audit suite found security backlog items
- final reports and closeout

When `/computa-4d-chess` starts, queue at least:

- `computa-init`
- `computa-speak`
- `computa-docs-architecture-audit` when `docs/architecture/` exists
- codebase audit for existing codebases
- `computa-4d-chess-architect`
- `computa-4d-chess-build`
- per-Super-Phase adversarial review after build
- per-Super-Phase judge/verifier review after build
- full Super-Phase plan adversarial review
- full Super-Phase plan judge/verifier review
- `computa-4d-chess-execute`
- every known Super-Phase execution through `computa-make-no-mistakes`
- 4D security/privacy checkpoint and Export Control handoff reconciliation
- architecture docs update
- final reports and closeout

When `/computa-make-no-mistakes` starts, queue at least:

- `computa-init`
- `computa-swarm-verify`
- `computa-swarm-verify-setup`
- `computa-speak`
- `computa-swarm-verify-investigate`
- `computa-swarm-verify-tdd-qa`
- `computa-swarm-verify-swarms`
- `computa-make-no-mistakes-docs-update` after every phase
- `computa-swarm-verify-closeout`
- phase-level adversarial review gates
- phase-level judge/verifier review gates
- task-level adversarial review gates
- task-level judge/verifier review gates
- verification and runtime QA gates

After Computa Phase 0 creates concrete phases/tasks/subtasks, replace generic placeholders with explicit phase and task queue rows.

## Activity Log Integration

Also append to `docs/computa-artifacts/activity-log.csv` for queue-level resume points:

- `queue_initialized`
- `queue_expanded`
- `queue_item_started`
- `queue_item_completed`
- `queue_item_blocked`
- `queue_item_deferred`
- `queue_item_superseded`

The activity log should point to the queue file and the relevant artifact path. Do not duplicate subtask detail in the root activity log unless a subtask is the current crash-resume point and no task-level ledger is sufficient.

## Resume Contract

On resume, `computa-resume` must inspect the queue before choosing the next skill. The next action should be the highest-priority ready item, not the most recent chat instruction.

If queue and local ledgers disagree:

- trust concrete evidence first
- update stale queue rows only after confirming the real state
- record a `queue_item_superseded` or `queue_item_completed` row as appropriate
- do not silently proceed from a stale queue

## Closeout Contract

No Export Control, 4D Chess, or Computa Make No Mistakes session may be marked complete until:

- all required queue items are `complete`, `deferred` with rationale, or `blocked` with evidence
- no required child skill remains `queued`, `ready`, `running`, or `review_needed`
- final reports identify any deferred/blocked queue items
- `execution-queue.csv`, session ledgers, and `activity-log.csv` agree on the next action
- hook validation passes with `computa_hooks.py validate --strict` and closeout validation passes with `computa_hooks.py validate --closeout --strict`, when the runner is available

Golden rule: invocation expands the queue; execution consumes the queue.
