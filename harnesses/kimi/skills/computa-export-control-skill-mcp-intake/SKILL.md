---
name: computa-export-control-skill-mcp-intake
description: Focused Computa Export Control research skill for discovering agentic skills, MCP servers, plugins, connectors, browser/devtools tools, and harness capabilities that may help execute a project. Use to decide what skills/tools should be imported, installed, invoked, or avoided across Codex, Claude Code, Kimi, OpenCode, Cursor, Goose, and related harnesses.
---

# Computa Export Control Skill MCP Intake

Use this to inventory agent capabilities before planning execution.

If invoked directly and `docs/computa-artifacts/activity-log.csv` exists or can be initialized, append `research_task_started` before intake and `research_task_completed`, `research_task_blocked`, or `research_task_deferred` after it, with `scope_name=skill-mcp-intake` and `artifact_path=skills-and-tools/`.

## Sources

Inspect available local and installable capabilities:

- local skill directories
- plugin-provided skills and tools
- MCP servers and connector metadata
- harness config files
- project `AGENTS.md`, rules, recipes, and docs
- official docs for candidate tools when current behavior matters

Use tool discovery when available. If a tool is named by the user but unavailable, record whether it can be installed, substituted, or must be skipped.

## Outputs

Write under `skills-and-tools/`:

- `capability-inventory.md`: available skills, MCPs, plugins, connectors, and browser/runtime tools.
- `recommended-imports.md`: what to use for this project and why.
- `harness-compatibility.csv`: capability, harness, install path, compatibility, caveats, recommendation.
- `tool-gap-analysis.md`: missing capabilities, substitutes, and blockers.
- `execution-tooling-plan.md`: which skills/tools each export-control campaign should use.

## Rules

- Prefer existing local skills/tools over inventing new workflows.
- Do not assume a tool exists just because it would be useful.
- Check whether capabilities are compatible with the current harness.
- Keep install recommendations separate from execution; do not install tools unless the user or execution plan permits it.
- Record credentials, account access, dashboard, or production-touching risks.
