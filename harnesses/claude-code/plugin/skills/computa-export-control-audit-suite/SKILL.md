---
name: computa-export-control-audit-suite
description: Export Control post-research audit coordinator that runs security-audit, performance-audit, and ui-audit in documentation mode, consolidates all findings into CSV/Markdown ledgers, and converts the findings into an implementation backlog for sequential computa-4d-chess campaigns. Use after Export Control codebase/research/spec work and before 4D campaign execution.
---

# Computa Export Control Audit Suite

Use this after Export Control has enough context to audit intelligently: raw task captured, normalized task created, codebase audit completed for existing repos, requirements researched, technology/prior-art/tool decisions drafted, and technical spec created or explicitly deferred.

This skill does not implement fixes. It produces the finding inventory and remediation backlog that Export Control uses to design 4D Chess campaigns.

## Required Inputs

Read from the current Export Control session:

- `user-task.md`
- `normalized-task.md`
- `research-agenda.md`
- `codebase-audit/` when a repo exists
- `requirements/` and product requirements outputs
- `tech-radar/`, `prior-art/`, and `skills-and-tools/`
- `technical-spec/` when present
- `decision-matrix.md`
- `recommended-design.md`

If an existing codebase was not audited, stop and record a blocker. These audits must evaluate the real repo, not a guessed architecture.

## Artifact Root

Create `standalone-audits/` in the Export Control session:

- `standalone-audits/audit-suite-plan.md`
- `standalone-audits/audit-suite-ledger.csv`
- `standalone-audits/cross-audit-finding-ledger.csv`
- `standalone-audits/remediation-backlog.csv`
- `standalone-audits/implementation-campaign-map.md`
- `standalone-audits/owner-decisions.md`
- `standalone-audits/issues-and-blockers.md`
- `standalone-audits/issues-and-blockers.csv`
- `standalone-audits/reviews/`
- `standalone-audits/security/`
- `standalone-audits/performance/`
- `standalone-audits/ui/`

Append `audit_suite_started`, `audit_task_started`, `audit_task_completed`, `audit_task_blocked`, `audit_suite_completed`, or `audit_suite_blocked` rows to root `docs/computa-artifacts/activity-log.csv` when available.

## Run The Three Audits

Run all three standalone audit skills in Export Control Audit Documentation Mode:

1. `security-audit`
2. `performance-audit`
3. `ui-audit`

Each audit reads its own `references/prompts.md`, splits the 100 prompts into batches, and writes category-specific Markdown/CSV findings. No product-code edits are allowed in this mode.

Use subagents for independent read-only batches when available:

- default batch size: 10 prompts
- one subagent per batch when safe
- never parallelize shared browser sessions, dev servers, databases, credentials, dashboards, deploys, migrations, or write operations
- require each subagent to return prompt coverage, findings, evidence paths, confidence, and implementation recommendations

If a category is not applicable, write a full no-op report with evidence. For example, UI audit can be N/A for a pure backend service, but it must say why and what was inspected.

## Consolidation

After the three audits complete:

1. Deduplicate overlapping findings across security, performance, and UI.
2. Preserve category-specific evidence links. Do not collapse away source findings.
3. Classify every consolidated item by severity, confidence, user impact, implementation complexity, risk, dependencies, and owner-decision status.
4. Create `standalone-audits/remediation-backlog.csv` as the source of truth for implementation planning.
5. Create `standalone-audits/implementation-campaign-map.md` mapping backlog groups to proposed `computa-4d-chess` campaigns and Super-Phase candidates.

`cross-audit-finding-ledger.csv` fields:

`finding_id,categories,source_finding_ids,title,severity,confidence,user_impact,technical_risk,affected_files,affected_routes,evidence_paths,recommendation,dependencies,owner_decision_needed,status`

`remediation-backlog.csv` fields:

`backlog_id,finding_ids,objective,categories,severity,dependencies,suggested_4d_campaign,suggested_super_phase,tests_required,runtime_qa_required,docs_update_required,owner_decision_needed,status`

## Review Gate

Before Export Control creates or updates 4D campaigns:

1. Run adversarial review of audit coverage, duplicate handling, evidence quality, false positives, unsafe recommendations, and campaign grouping.
2. Run judge/verifier review of the adversarial findings.
3. Update only for judge-approved changes.
4. Mark the audit suite `approved_for_campaign_design`, `approved_with_risks`, `blocked`, or `deferred`.

Do not launch 4D implementation campaigns from unreviewed audit-suite findings.

## Handoff To 4D Chess

Export Control campaign design must consume:

- `standalone-audits/remediation-backlog.csv`
- `standalone-audits/implementation-campaign-map.md`
- category-specific `implementation-backlog.csv` files
- category-specific `finding-details.md`
- audit-suite review outputs

The 4D campaigns should implement accepted findings in a dependency-aware order. They should not blindly run all 300 prompts as implementation tasks; the audit suite already converted those prompts into evidence-backed backlog items.

Golden rule: audits produce source-truth implementation evidence, not vibes. Every campaign should trace back to finding IDs and evidence paths.
