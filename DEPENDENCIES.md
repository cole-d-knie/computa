# Dependency Matrix

Checked on 2026-06-19 using GitHub, npm package metadata, installed local plugin metadata, Context7 docs, and official harness docs.

## Skill Dependencies

| Dependency | Upstream checked | Local package role | Install behavior |
| --- | --- | --- | --- |
| `caveman` | [`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman), latest GitHub release checked: `v1.9.0` | Terse communication discipline for the workflow. | Vendored as a lightweight skill for Codex, Claude Code, Kimi, OpenCode, Agent Skills, and the Claude plugin adapter. |
| `context7` | [`upstash/context7`](https://github.com/upstash/context7); npm package `@upstash/context7-mcp` checked at `3.2.1` | Current docs lookup for libraries, APIs, CLIs, and harness behavior. | Vendored skill plus MCP config. Claude plugin uses `.mcp.json`; Kimi/Cursor use `mcp.json`; OpenCode uses `opencode.json`; Goose recipe includes an extension. |
| `gstack-investigate` / `investigate` | [`garrytan/gstack`](https://github.com/garrytan/gstack), public repo, no GitHub release found during check | Systematic investigation/root-cause workflow. | Lightweight generated `investigate` skill is vendored. Full `gstack` core is not vendored; install with `--install-local-gstack` when available. |
| `playwright` | [`microsoft/playwright-mcp`](https://github.com/microsoft/playwright-mcp); npm package `@playwright/mcp` checked at `0.0.76` | Browser-visible runtime QA and UI verification. | Vendored skill plus MCP config for Claude plugin, Kimi, Cursor, OpenCode, and Goose. Requires Node/npm `npx`. |
| Superpowers family | [`obra/superpowers`](https://github.com/obra/superpowers), latest GitHub release checked: `v6.0.3` | Planning, TDD, debugging, swarm/delegation, review, completion proof. | Vendored as individual skills: `using-superpowers`, `writing-plans`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `dispatching-parallel-agents`, `subagent-driven-development`, `requesting-code-review`, `verification-before-completion`. |

## Harness-Specific Compatibility

| Harness | Dependency strategy | Notes |
| --- | --- | --- |
| Codex | Copy suite skills and vendored dependency skills into `${CODEX_HOME:-~/.codex}/skills`. | Codex-specific tool/plugin availability still depends on the host. Full `gstack` core is optional and copied only with `--install-local-gstack`. |
| Claude Code | Copy suite and dependency skills into `~/.claude/skills`; plugin adapter also contains the suite, dependency skills, and `.mcp.json`. | Claude plugin `.mcp.json` follows current Claude plugin docs for multiple MCP servers. |
| Kimi Code | Copy Kimi-specific suite skills into `~/.kimi-code/skills`; copy compatible dependency skills; update `config.toml` `extra_skill_dirs`; add missing `context7` and `playwright` MCP servers to `~/.kimi-code/mcp.json`. | Kimi suite wording uses agent swarm/delegation and does not require `subagent-driven-development`. |
| OpenCode | Copy suite/dependency skills into `~/.config/opencode/skills`; merge `~/.config/opencode/opencode.json` with `instructions` and MCP server entries. | OpenCode uses `instructions` and `mcp` config rather than the exact Codex/Claude skill loader. Template: `harnesses/opencode/opencode.computa-swarm-verify.json`. |
| Cursor | Install `.cursor/rules/computa-swarm-verify.mdc`; add missing `context7` and `playwright` entries to `.cursor/mcp.json` for project installs or `~/.cursor/mcp.json` for global installs. | Cursor rules are the reliable instruction path. MCP config is project/global JSON and should be reviewed like infrastructure config. |
| Goose | Install `~/.config/goose/recipes/computa-swarm-verify.yaml`. | Recipe includes built-in developer extension plus Context7 and Playwright stdio extensions. |
| Agent Skills open standard | Copy suite/dependency skill folders into `~/.agents/skills`. | Useful for tools that read shared Agent Skills folders; MCP/tooling still depends on the harness. |
| Generic | Install `AGENTS.computa-swarm-verify.md`. | Fallback instructions only; user must configure equivalent tools manually. |

## Config Files Installed Or Generated

| File | Purpose |
| --- | --- |
| `harnesses/claude-code/plugin/.mcp.json` | Claude plugin MCP config for Context7 and Playwright. |
| `harnesses/kimi/mcp.json` | Reference Kimi MCP config; installer merges missing entries into `~/.kimi-code/mcp.json`. |
| `harnesses/cursor/mcp.json` | Reference Cursor MCP config; installer merges missing entries into project/global Cursor MCP config. |
| `harnesses/opencode/opencode.computa-swarm-verify.json` | Reference OpenCode config for instructions and MCP servers; installer merges equivalent entries into global OpenCode config. |
| `harnesses/goose/recipes/computa-swarm-verify.yaml` | Goose recipe with task parameter, instructions, developer extension, Context7, and Playwright. |

## Verification Sources

- GitHub checks: `gh repo view obra/superpowers`, `gh repo view garrytan/gstack`, `gh repo view upstash/context7`, `gh repo view microsoft/playwright-mcp`, `gh repo view JuliusBrussee/caveman`.
- npm checks: `npm view @upstash/context7-mcp ...`, `npm view @playwright/mcp ...`.
- Context7 docs checks: Claude Code plugin MCP config, Kimi Code `extra_skill_dirs` and `mcp.json`, OpenCode `instructions` and `mcp`.
- Official docs/web checks: Cursor MCP docs and Goose MCP/recipe docs.
