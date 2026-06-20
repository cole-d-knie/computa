---
name: security-audit
description: Security audit and hardening skill for authentication, access control, injection, secrets, data exposure, privacy, and related app security risks. Use directly with /security-audit, inside Computa Export Control audit-suite documentation mode, or inside the mandatory Computa 4D final Super-Phase SP-999 where /computa-make-no-mistakes orchestrates security remediation before 4D closeout.
allowed-tools: Read Edit Write Grep Glob Bash(git *) Bash(npm *) Bash(npx *) Bash(pnpm *) Bash(yarn *) Bash(bun *)
---

# Security Audit

Use this skill in one of three modes. Always determine the mode before loading `references/prompts.md`.

## Modes

### Export Control Audit Documentation Mode

Use when invoked by `computa-export-control-audit-suite`. Do not edit product code. Do not create audit-fix commits. Read `references/prompts.md`, split the 100 prompts into batches, investigate the codebase, and produce detailed Markdown/CSV findings that later 4D Chess campaigns can implement.

Write under the Export Control session:

- `standalone-audits/security/audit-invocation.md`
- `standalone-audits/security/prompt-coverage.csv`
- `standalone-audits/security/findings.csv`
- `standalone-audits/security/finding-details.md`
- `standalone-audits/security/recommendations.md`
- `standalone-audits/security/implementation-backlog.csv`
- `standalone-audits/security/issues-and-blockers.md`
- `standalone-audits/security/issues-and-blockers.csv`
- `standalone-audits/security/evidence-index.md`
- `standalone-audits/security/subagent-batches.csv`

For each prompt, record whether it is applicable, not applicable, already satisfied, uncertain, or blocked. Every finding needs evidence: file paths, commands, runtime observations, config values, tests, or exact unknowns. Recommendations must distinguish critical fixes, defense-in-depth, policy choices, and owner decisions.

Use subagents for read-only batch investigation when available. Suggested batches are 10 prompts each. Do not parallelize batches that require shared runtime state, credentials, dashboards, migrations, or write access.

### 4D Final Super-Phase Implementation Mode

Use when invoked by `/computa-make-no-mistakes` from `SP-999-post-run-security-audit`. This is the mandatory final 4D Super-Phase, not a hidden closeout hook.

The nested Computa run must:

- save its own `user-task.md`
- use the 4D-scoped branch `vibecoder/security-<4d-session-id-or-slug>` unless the parent task forbids branches
- use `.claude/vibecoder/security-<4d-session-id-or-slug>-progress.md`
- read `references/prompts.md`
- turn relevant prompt findings into Computa phases/tasks/subtasks
- create tests or verification evidence before and after fixes where possible
- make scoped commits only when commits are allowed
- update maps, ledgers, architecture docs, and final reports after security changes
- write or update `<4D-session>/security-audit/` and `reports/security-audit.md`

The final 4D session cannot append `session_completed` until this Super-Phase is completed, explicitly N/A, or blocked/deferred with evidence and owner acceptance.

### Direct Remediation Mode

Use when the user directly invokes `/security-audit` and asks for hardening. Work through `references/prompts.md` in order. If a prompt is not applicable, record N/A with evidence instead of forcing a change. Keep one prompt or one tightly grouped Computa task per commit when commits are allowed. Never weaken a real security control to make a prompt pass.

## Required CSV Fields

`findings.csv`:

`finding_id,prompt_id,area,title,severity,confidence,status,evidence_path,affected_files,recommendation,implementation_owner,dependencies,estimated_complexity,should_4d_implement`

`implementation-backlog.csv`:

`item_id,finding_ids,objective,risk_level,dependencies,suggested_campaign,suggested_super_phase,tests_required,runtime_qa_required,owner_decision_needed,status`

`prompt-coverage.csv`:

`prompt_id,title,area,applicability,status,evidence_path,finding_ids,notes`

## Review Gate

Before handing findings to Export Control or closing SP-999:

1. Run adversarial review of coverage, missed security surfaces, weak evidence, false positives, unsafe recommendations, and missing tests.
2. Run judge/verifier review of the adversarial findings.
3. Update artifacts only for judge-approved changes.
4. Mark the audit `approved_for_backlog`, `approved_with_risks`, `implemented`, `blocked`, or `deferred`.

Golden rule: security claims require evidence. If you cannot verify a surface, record the unknown explicitly.
