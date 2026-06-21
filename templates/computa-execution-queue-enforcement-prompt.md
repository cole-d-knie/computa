# Computa Execution Queue Enforcement Prompt

Use this prompt when an agent is skipping child skills, flattening phases, losing resume state, or treating a loaded skill as completed work.

```text
Use the Computa execution queue strictly.

Before executing any Export Control, 4D Chess, or Computa Make No Mistakes work, invoke /computa-execution-queue after /computa-init and /computa-speak.

Rules:
- Skill invocation expands the queue; execution consumes the queue.
- Hooks may deterministically expand missing queue rows. Treat hook-added rows as real queue rows, not suggestions.
- Create/update docs/computa-artifacts/execution-queue.csv and execution-queue.md, plus session-local queue files.
- The queue is dependency-aware, not FIFO.
- Add every required child skill, phase, task, Super-Phase, campaign, review gate, docs hook, verification gate, and closeout gate to the queue before executing it.
- Recursive execution is mandatory: Export Control campaign rows invoke /computa-4d-chess; 4D Super-Phase rows invoke /computa-make-no-mistakes; Export Control final security closeout invokes /security-audit once through /computa-make-no-mistakes when applicable.
- If a required child skill is not applicable, add a deferred queue row with rationale. Do not omit it.
- Do not mark a skill/session complete just because a skill was loaded. Mark it complete only after required outputs, evidence, reviews, ledgers, and queue rows are complete.
- Execute only the highest-priority unblocked ready item whose dependencies are satisfied and whose non-overlap key is safe.
- If new information changes the plan, mark stale queue rows superseded, explain why, and add corrected rows. Do not erase history.
- On resume, inspect execution-queue.csv before relying on chat history or activity-log.csv.
- Do not start Export Control final security closeout or any dependent work until prerequisite campaign queue rows are complete, deferred with rationale, or blocked with evidence.
- Final closeout is forbidden while required queue rows remain queued, ready, running, or review_needed.

If you notice the current artifacts do not have a valid execution queue, pause implementation, create/reconcile the queue from existing ledgers, then resume from the highest-priority safe item.
```
