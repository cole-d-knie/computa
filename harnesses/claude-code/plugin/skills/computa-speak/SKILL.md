---
name: computa-speak
description: Rewrite raw user prompts into concise, structured, AI-ready coding-agent task prompts while preserving all substantive requirements, constraints, permissions, exclusions, and ambiguities. Use as the first prompt-normalization step for direct computa-export-control, computa-4d-chess, and computa-make-no-mistakes invocations before planning, research, architecture, or implementation.
---

# Computa Speak

Use this to turn the user's raw request into a clearer prompt for coding agents.

The raw prompt is still source truth. The optimized prompt is the working prompt used by the rest of Computa.

## Inputs

Read the raw user request from the active invocation. If a Computa session exists, read `user-task.md`. If no session exists yet, use the exact user message and tell the caller to save it unchanged before relying on the rewrite.

Also read any explicit constraints already known:

- repo/path
- branch/base branch
- do-not-touch areas
- read-only or write permissions
- external systems involved
- test/runtime requirements
- user-provided files, tickets, prompts, or reports
- deadlines, output format, and handoff needs

## Output Files

When an active session exists, write:

- `normalized-task.md`: the optimized AI-ready task prompt.
- `prompt-normalization-log.md`: what was clarified, spelling/wording fixes made, ambiguities preserved, and constraints that must not be dropped.

When `docs/computa-artifacts/activity-log.csv` exists, append `prompt_normalization_started` before rewriting and `prompt_normalization_completed` or `prompt_normalization_blocked` after, with `artifact_path=normalized-task.md`.

If no session exists, return the optimized prompt and a short preservation note so the caller can save both after `computa-init`.

## Rewrite Rules

- Fix spelling, grammar, missing punctuation, and unclear phrasing.
- Make the prompt concise, structured, and easy for an AI coding agent to execute.
- Preserve every substantive requirement, constraint, permission, exclusion, blocker, dependency, and output request.
- Preserve user tone only where it carries technical priority or urgency.
- Convert rambling text into clear sections such as Task, Context, Scope, Constraints, Required Workflow, Verification, Deliverables, and Open Questions.
- Make implicit sequencing explicit when the raw prompt clearly implies it.
- Keep uncertainty explicit. Do not invent missing requirements.
- Mark ambiguities as `Open Questions` only when they matter; otherwise include reasonable assumptions as assumptions.
- Do not remove safety constraints like "do not push", "read only", "do not touch dashboards", or "use @Computer".
- Do not turn a question into permission to edit unless the raw prompt gave that permission.
- Do not add technologies, architecture, tests, or phases that the user did not ask for unless the prompt is explicitly asking for planning guidance.

## Reconciliation Check

Before handing off the optimized prompt:

1. Compare it against the raw request.
2. Confirm no requirement was dropped.
3. Confirm no new scope was added.
4. Confirm all do-not-touch constraints remain visible.
5. Confirm unresolved ambiguity is preserved rather than guessed.

Record the reconciliation in `prompt-normalization-log.md`.

## Downstream Contract

Downstream Computa skills should analyze `normalized-task.md` first, then cross-check `user-task.md` whenever scope, permission, or acceptance criteria are in doubt.

If the normalized prompt conflicts with the raw prompt, the raw prompt wins and `normalized-task.md` must be corrected.
