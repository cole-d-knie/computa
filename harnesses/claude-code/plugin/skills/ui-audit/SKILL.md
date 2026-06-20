---
name: ui-audit
description: UI and UX audit skill for layout, typography, spacing, visual hierarchy, motion, accessibility, responsiveness, interaction states, and product polish. Use directly with /ui-audit or inside Computa Export Control audit-suite documentation mode to produce detailed findings, screenshots/evidence, and 4D implementation backlogs before UI work is executed.
allowed-tools: Read Edit Write Grep Glob Bash(git *) Bash(npm *) Bash(npx *) Bash(pnpm *) Bash(yarn *) Bash(bun *)
---

# UI Audit

Use this skill in one of two modes. Always determine the mode before loading `references/prompts.md`.

## Modes

### Export Control Audit Documentation Mode

Use when invoked by `computa-export-control-audit-suite`. Do not edit product code. Do not create UI-fix commits. Read `references/prompts.md`, split the 100 prompts into batches, inspect the codebase and runtime UI where possible, and produce detailed Markdown/CSV findings that later 4D Chess campaigns can implement.

Write under the Export Control session:

- `standalone-audits/ui/audit-invocation.md`
- `standalone-audits/ui/prompt-coverage.csv`
- `standalone-audits/ui/findings.csv`
- `standalone-audits/ui/finding-details.md`
- `standalone-audits/ui/recommendations.md`
- `standalone-audits/ui/implementation-backlog.csv`
- `standalone-audits/ui/issues-and-blockers.md`
- `standalone-audits/ui/issues-and-blockers.csv`
- `standalone-audits/ui/evidence-index.md`
- `standalone-audits/ui/subagent-batches.csv`

For each prompt, record whether it is applicable, not applicable, already satisfied, uncertain, or blocked. Findings should include visual evidence when possible: screenshots, route paths, viewport sizes, browser/device context, component paths, accessibility observations, contrast evidence, keyboard/focus behavior, and exact unknowns when runtime access is unavailable.

Use subagents for read-only batch investigation when available. Suggested batches are 10 prompts each. Do not parallelize batches that require the same browser session, running dev server, visual baseline, design file, deploy, or write access.

### Direct Remediation Mode

Use when the user directly invokes `/ui-audit` and asks for UI/UX polish. Work through `references/prompts.md` in order. If a prompt is not applicable, record N/A with evidence instead of forcing a change. Keep one prompt or one tightly grouped Computa task per commit when commits are allowed. Preserve functionality, content, accessibility, and product intent.

## Required CSV Fields

`findings.csv`:

`finding_id,prompt_id,area,title,severity,confidence,status,evidence_path,affected_routes,affected_files,recommendation,implementation_owner,dependencies,estimated_complexity,should_4d_implement`

`implementation-backlog.csv`:

`item_id,finding_ids,objective,affected_routes,visual_evidence,dependencies,suggested_campaign,suggested_super_phase,tests_required,runtime_qa_required,owner_decision_needed,status`

`prompt-coverage.csv`:

`prompt_id,title,area,applicability,status,evidence_path,finding_ids,notes`

## Review Gate

Before handing findings to Export Control:

1. Run adversarial review of coverage, weak visual evidence, false positives, accessibility gaps, responsive-state gaps, and recommendations that risk product regression.
2. Run judge/verifier review of the adversarial findings.
3. Update artifacts only for judge-approved changes.
4. Mark the audit `approved_for_backlog`, `approved_with_risks`, `blocked`, or `deferred`.

Golden rule: UI claims need route, viewport, and evidence. If runtime UI cannot be inspected, record that blocker.
