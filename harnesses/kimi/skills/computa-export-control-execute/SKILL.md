---
name: computa-export-control-execute
description: Execution controller for Computa Export Control. Use after export-control design approval to quarterback sequential computa-4d-chess campaigns, enforce campaign dependencies, preserve research decisions, verify campaign outputs, run adversarial and judge/verifier reviews, and synthesize final massive-project reports.
---

# Computa Export Control Execute

Use this after `computa-export-control-design` has produced an approved campaign sequence. Execute controls sequential 4D Chess instances. It does not redesign the strategy unless new evidence proves the design is wrong.

## Preflight

Verify these exist:

- `user-task.md`
- `normalized-task.md`
- `research-agenda.md`
- focused research outputs
- `decision-matrix.md`
- `recommended-design.md`
- `reuse-plan.md`
- `technical-spec/spec-index.md` when the design says a technical spec is required
- `technical-spec/acceptance-contract.md` when campaigns depend on a technical spec
- `implementation-strategy/strategy-index.md` when the design says implementation strategy is required
- `implementation-strategy/keyless-test-strategy.md` when campaigns depend on secret-dependent integrations
- `implementation-strategy/campaign-readiness.md` when campaigns depend on complex engineering decisions
- `standalone-audits/remediation-backlog.csv` when a codebase/app audit suite was required
- `standalone-audits/implementation-campaign-map.md` when a codebase/app audit suite was required
- `security-closeout/` can be initialized for final Export Control security closeout when a codebase/app exists or campaigns may touch security/privacy-sensitive surfaces
- `secrets-needed-readout.md` and root `docs/computa-artifacts/secrets-needed/secrets-needed.csv` when the design found private config requirements
- `campaigns/campaign-sequence.md`
- `campaigns/campaign-ledger.csv`
- root and Export Control session-local `execution-queue.csv` include campaign execution, review, reconciliation, and closeout rows
- design review outputs

If any required artifact is missing, stop and record a blocker. Do not execute from chat memory.

If campaign prompts reference `technical-spec/`, verify `technical-spec/spec-index.md` marks the spec `approved_for_campaign_design` or `approved_with_risks`. Do not launch 4D campaigns from unreviewed technical specs.

If campaign prompts reference `implementation-strategy/`, verify `implementation-strategy/strategy-index.md` marks the strategy `approved_for_campaign_design` or `approved_with_risks`. Do not launch 4D campaigns when complex engineering issues or keyless test strategy remain unresolved.

If campaign prompts reference standalone audit findings, verify `standalone-audits/remediation-backlog.csv` and audit-suite review outputs mark the backlog `approved_for_campaign_design` or `approved_with_risks`. Do not launch audit-driven 4D campaigns from unreviewed security/performance/UI findings.

## Execution Loop

For each highest-priority ready approved campaign queue item in dependency order:

1. Confirm prerequisites and unresolved owner decisions.
2. Re-read campaign instructions, research evidence, technical specs when referenced, implementation strategy when referenced, standalone audit findings/backlog when referenced, and relevant maps.
3. Briefly justify why this campaign should start now and challenge why that might be wrong.
4. Append `campaign_started` to `docs/computa-artifacts/activity-log.csv` with the campaign prompt or directory as `artifact_path`.
5. Mark the campaign queue item `running`, append `queue_item_started`, then invoke `/computa-4d-chess` with the exact campaign prompt.
6. Require the 4D run to create its own child session under this Export Control session at `4d-chess/4D-YYYYMMDD-HHMMSS-slug/`, create Super-Phases, reviews, nested Computa runs, update root `activity-log.csv`, produce a security/privacy checkpoint and handoff, and closeout.
7. Link the 4D session path in `campaigns/campaign-ledger.csv` and register it in `docs/computa-artifacts/session-ledger.csv` with this Export Control session as parent.
8. Verify the 4D closeout against export-control decisions, standalone audit backlog items, campaign acceptance criteria, and the campaign security/privacy checkpoint.
9. Verify the campaign reconciled `docs/computa-artifacts/secrets-needed/` and did not hide private-config blockers.
10. Run campaign-level adversarial review.
11. Run campaign-level judge/verifier review.
12. Apply or schedule only judge-approved follow-up.
13. Update source ledgers, decision matrix, maps, campaign ledger, secrets-needed readout, and handoffs.
14. Append `campaign_completed`, `campaign_blocked`, or `campaign_deferred` to `activity-log.csv` with the review/evidence path and exact next action.
15. Mark the campaign queue item `complete`, `blocked`, or `deferred`, append the matching queue activity event, and update dependent campaign rows from `queued` to `ready` only when prerequisites are satisfied.

## Plan Changes

If a campaign reveals that the design is wrong:

- stop affected downstream campaigns
- preserve old decisions and evidence
- write `campaigns/plan-change-proposal.md`
- run adversarial review, then judge/verifier review
- update campaign order, prompts, requirements, and decisions only for approved changes
- resume from the corrected dependency point

Never silently skip, merge, reorder, or broaden campaigns.

## Final Security Closeout

After all campaign queue items are complete, blocked with accepted evidence, or deferred with rationale, reconcile security/privacy evidence before Export Control closeout:

1. Read standalone audit-suite security findings, each campaign's 4D security/privacy checkpoint, campaign closeout reports, secrets-needed entries, architecture docs, and current source truth.
2. Create or update `security-closeout/invocation.md`, `security-closeout/summary.md`, `security-closeout/issues-and-blockers.md`, `security-closeout/issues-and-blockers.csv`, and `security-closeout/security-closeout-ledger.csv`.
3. If a codebase/app exists or campaigns touched security/privacy-sensitive surfaces, invoke `/computa-make-no-mistakes` with a scoped task that invokes `/security-audit` once for the Export Control session. Use an Export-Control-scoped branch/progress file name and record command/test/runtime evidence.
4. If full security closeout is not applicable, read-only, or blocked by explicit constraints, write an evidence-backed N/A/blocker instead of running it.
5. Run adversarial review, then judge/verifier review of the final security closeout. Implement only judge-approved follow-up that is safe inside the Export Control scope; otherwise record follow-up or owner decision.
6. Append `security_closeout_started` and `security_closeout_completed`, `security_closeout_blocked`, or `security_closeout_deferred` rows to `docs/computa-artifacts/activity-log.csv`.

Do not run this final full `/security-audit` after every 4D campaign. 4D campaigns provide checkpoints and handoff items; Export Control owns the single whole-program closeout.

## Parallelism

Export Control defaults to sequential 4D campaigns because these are massive projects. Parallelize only if all are true:

- campaigns have no dependency relation
- they do not touch overlapping files, modules, concepts, data, dashboards, databases, deployments, credentials, or external accounts
- they have separate artifact roots and evidence paths
- a coordinator will reconcile outputs before dependent work starts

When unsure, execute serially.

## Closeout

Produce:

- `reports/export-control-summary.md`
- `reports/research-decisions.md`
- `reports/technology-and-reuse-report.md`
- `reports/implementation-strategy.md`
- `reports/standalone-audit-findings.md`
- `reports/final-security-closeout.md`
- `reports/campaign-execution-report.md`
- `reports/blockers-open-issues-and-owner-decisions.md`
- `reports/secrets-needed.md`
- `reports/gaps-vs-user-task.md`
- `reports/follow-up-roadmap.md`

Append `session_completed` or `session_blocked` for the Export Control session to `docs/computa-artifacts/activity-log.csv`.

Before session closeout, reconcile root and session-local execution queues. Do not mark Export Control complete while required child skill, campaign, review, reconciliation, or report rows remain `queued`, `ready`, `running`, or `review_needed`.

Do not mark Export Control complete until the final security closeout is completed, explicitly N/A, blocked/deferred with evidence, or outside the task scope by user instruction.

State whether the massive project is complete, partially complete, blocked, or ready for the next export-control cycle, and include the latest resume point from `activity-log.csv`.
