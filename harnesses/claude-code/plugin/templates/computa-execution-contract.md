# Computa Execution Contract

This contract is the shared enforcement target for Computa skills and hooks.

## 1. Invocation Expands, Execution Consumes

Loading a skill is not work completion. Every orchestration skill must expand its required child skills, phases, tasks, review gates, docs hooks, verification gates, closeout gates, and recursive invocations into `docs/computa-artifacts/execution-queue.csv` before execution.

Execute the highest-priority ready queue row whose dependencies are terminal and whose `non_overlap_key` is safe. Do not skip ahead based on chat memory.

## 2. Recursive Routing Is Mandatory

- Export Control campaign execution routes through `/computa-4d-chess`.
- 4D Chess Super-Phase execution routes through `/computa-make-no-mistakes`.
- Export Control final security closeout, when applicable, routes through `/computa-make-no-mistakes` with `/security-audit` inside that task.

If a route is not applicable, add a `deferred` queue row with evidence/rationale. Do not omit it.

## 3. Completion Requires Terminal Children

Do not mark a parent session, skill, campaign, Super-Phase, phase, or task complete until its required child queue rows exist and are terminal:

- `complete`
- `deferred` with rationale
- `blocked` with evidence
- `superseded` with rationale and replacement path

`queued`, `ready`, `running`, `review_needed`, and `failed` are not complete.

## 4. Artifact Shape Is Part Of Completion

Completed sessions must have the expected artifact shape:

- Export Control: `user-task.md`, `normalized-task.md`, session `execution-queue.csv`, campaign/report artifacts.
- 4D Chess: `user-task.md`, `super-phases/`, Super-Phase ledgers, and each Super-Phase's Computa invocation or nested CMN artifacts.
- Computa Make No Mistakes: `user-task.md`, `normalized-task.md` or `plan.md`, `phases/`, phase ledgers, task directories, task ledgers, and subtask ledgers.

Missing artifact shape is incomplete work, even if a ledger row says `complete`.

## 5. Completion Artifacts Are Resume Handshakes

Every terminal queue item, phase, task, Super-Phase, campaign, and top-level session should write a small completion artifact using `templates/computa-completion-artifact.md` when available.

The completion artifact must record:

- queue/session/scope IDs
- terminal status and rationale
- changed files or external systems
- verification evidence or blocked verification
- adversarial and judge/verifier review outcome
- commit SHA when code changed
- exact next queue item, blocker, or resume point

Then update `execution-queue.csv`, local ledgers, and `activity-log.csv` to reference the artifact path. If a context crashes, `computa-resume` and external orchestrators must be able to continue from the artifact without trusting chat memory.

## 6. Git Discipline

Never use broad staging commands:

- `git add .`
- `git add -A`
- `git add --all`
- `git add -u`
- `git add :/`

Stage intentional files explicitly. Do not let reference repos, secrets, `docs/computa-artifacts/`, dependency trees, generated caches, or unrelated user changes enter commits by accident.

## 7. Hook Checks Are Evidence Gates

Before closeout or handoff, run:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
python3 /path/to/computa/scripts/computa_hooks.py next
```

If the checker and a prose report disagree, trust the artifacts and fix the artifacts or the report before claiming completion.
