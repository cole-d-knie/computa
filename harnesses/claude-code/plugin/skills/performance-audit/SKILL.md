---
name: performance-audit
description: Performance audit and optimization skill for rendering, bundle size, network behavior, caching, database queries, runtime latency, and resource usage. Use directly with /performance-audit or inside Computa Export Control audit-suite documentation mode to produce detailed findings and 4D implementation backlogs before optimization work is executed.
allowed-tools: Read Edit Write Grep Glob Bash(git *) Bash(npm *) Bash(npx *) Bash(pnpm *) Bash(yarn *) Bash(bun *)
---

# Performance Audit

Use this skill in one of two modes. Always determine the mode before loading `references/prompts.md`.

## Modes

### Export Control Audit Documentation Mode

Use when invoked by `computa-export-control-audit-suite`. Do not edit product code. Do not create optimization commits. Read `references/prompts.md`, split the 100 prompts into batches, investigate the codebase and available runtime evidence, and produce detailed Markdown/CSV findings that later 4D Chess campaigns can implement.

Write under the Export Control session:

- `standalone-audits/performance/audit-invocation.md`
- `standalone-audits/performance/prompt-coverage.csv`
- `standalone-audits/performance/findings.csv`
- `standalone-audits/performance/finding-details.md`
- `standalone-audits/performance/recommendations.md`
- `standalone-audits/performance/implementation-backlog.csv`
- `standalone-audits/performance/issues-and-blockers.md`
- `standalone-audits/performance/issues-and-blockers.csv`
- `standalone-audits/performance/evidence-index.md`
- `standalone-audits/performance/subagent-batches.csv`

For each prompt, record whether it is applicable, not applicable, already satisfied, uncertain, or blocked. Findings should include measurable evidence when possible: build stats, bundle analysis, profiler notes, database query traces, network waterfall observations, Core Web Vitals, runtime timing, cache behavior, or precise missing-measurement blockers.

Use subagents for read-only batch investigation when available. Suggested batches are 10 prompts each. Do not parallelize batches that require shared test servers, browser sessions, databases, production logs, deploys, or write access.

### Direct Remediation Mode

Use when the user directly invokes `/performance-audit` and asks for optimization. Work through `references/prompts.md` in order. If a prompt is not applicable, record N/A with evidence instead of forcing a change. Keep one prompt or one tightly grouped Computa task per commit when commits are allowed. Do not trade correctness, accessibility, security, or maintainability for speed.

## Required CSV Fields

`findings.csv`:

`finding_id,prompt_id,area,title,severity,confidence,status,evidence_path,affected_files,recommendation,implementation_owner,dependencies,estimated_complexity,should_4d_implement`

`implementation-backlog.csv`:

`item_id,finding_ids,objective,performance_metric,baseline_evidence,dependencies,suggested_campaign,suggested_super_phase,tests_required,runtime_qa_required,owner_decision_needed,status`

`prompt-coverage.csv`:

`prompt_id,title,area,applicability,status,evidence_path,finding_ids,notes`

## Review Gate

Before handing findings to Export Control:

1. Run adversarial review of coverage, weak measurements, false positives, optimizations that risk behavior changes, missing regressions, and missing runtime proof.
2. Run judge/verifier review of the adversarial findings.
3. Update artifacts only for judge-approved changes.
4. Mark the audit `approved_for_backlog`, `approved_with_risks`, `blocked`, or `deferred`.

Golden rule: performance claims need measurements or an explicit measurement blocker.
