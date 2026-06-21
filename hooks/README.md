# Computa Hooks

Computa hooks are deterministic checks around the agent loop. They do not replace the skills; they enforce the artifact and queue contract the skills depend on.

## Portable Commands

Run from a project root:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py next
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

Use `COMPUTA_ROOT=/path/to/project` when the harness does not pass a working directory.

## Hook Modes

- `SessionStart` / `UserPromptSubmit`: add context reminding the agent to use the queue.
- `PreToolUse` / `BeforeShellExecution`: optionally block unsafe closeout attempts when the queue is invalid.
- `Stop` / `SessionEnd`: block completion when required queue rows are still active.
- `resume`: use `validate` and `next` before relying on chat history.

## Native vs Fallback Hooks

Codex, Claude Code, Goose, Kimi Code, OpenCode, and Cursor have native lifecycle hook integrations in this package:

- Codex: `harnesses/codex/hooks/hooks.json`
- Claude Code: `harnesses/claude-code/hooks/settings.computa-hooks.json`
- Goose: `harnesses/goose/plugins/computa-hooks/`
- Kimi Code: `harnesses/kimi/hooks/config-hooks.toml`
- OpenCode: `harnesses/opencode/plugins/computa-hooks.js`
- Cursor: `harnesses/cursor/hooks/hooks.json`

Generic harnesses can use the same scripts through wrappers, CI, or manual preflight/closeout commands.

The core enforcement is always the same:

1. `execution-queue.csv` must exist when Computa sessions exist.
2. Queue headers/statuses/dependencies must be valid.
3. Closeout is blocked while required queue rows are `queued`, `ready`, `running`, or `review_needed`.
4. Resume starts from the highest-priority safe queue item.
