# GLM Coding Plan + Computa

GLM Coding Plan is a provider layer for coding tools, not a separate Computa skill runtime.

Context7 docs source used: `/websites/z_ai_devpack`.

The Z.ai docs describe GLM Coding Plan support through mainstream coding tools, including Claude Code, OpenCode, Crush, and Factory Droid. For Computa, the reliable path is:

1. Configure GLM Coding Plan for the coding tool using Z.ai's helper or manual settings.
2. Install Computa into that coding tool.
3. Run Computa normally from the tool.

## Install

From the Computa repo:

```bash
./install.sh --harness glm
```

This installs Computa into the GLM-supported adapters that Computa can automate safely:

- Claude Code skills in `~/.claude/skills`
- OpenCode skills/instructions in `~/.config/opencode`
- GLM setup notes/templates in `~/.computa/glm/`

For project-scoped hooks/docs:

```bash
./install.sh --harness glm --project /path/to/project --install-hooks
```

## Configure GLM Coding Plan

Preferred official helper:

```bash
npx @z_ai/coding-helper
```

The helper can connect GLM Coding Plan to supported coding tools and manage MCP configuration.

## Claude Code GLM Settings

The Z.ai docs show Claude Code can use GLM through Anthropic-compatible environment variables in `~/.claude/settings.json`.

Use `claude-code-settings.example.json` as a template. Replace `your_zai_api_key` manually or through the official helper. Do not commit the real key.

## OpenCode

The Z.ai docs say the Coding Tool Helper supports OpenCode. Run the helper first, then run Computa through the OpenCode install:

```bash
./install.sh --harness opencode --install-hooks
```

The GLM install target already runs the OpenCode Computa setup.

## Secrets

Do not store actual Z.ai keys in this repo or in committed project files. Keep API keys in the target coding tool's private config only.

