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

## Recursive Skill Routing

Hooks do not secretly spawn model sessions or run skills in the background. That would be unreliable across Codex, Claude Code, Kimi, OpenCode, Cursor, and Goose.

Instead, the hook runner makes recursive invocation unavoidable through the queue:

1. It detects active Export Control, 4D Chess, and Computa Make No Mistakes sessions.
2. It checks that required child-skill queue rows exist or are explicitly deferred with rationale.
3. It checks recursive execution routing:
   - Export Control campaign execution must route to `/computa-4d-chess`.
   - 4D Chess Super-Phase execution must route to `/computa-make-no-mistakes`.
   - SP-999 must still run through `/computa-make-no-mistakes`, which invokes `/security-audit`.
4. It injects the exact next queue item and required skill invocation into session/prompt/compaction context.
5. It blocks final `Stop` / `SessionEnd` if child-skill expansion or recursive routing was skipped.

If a required child skill is genuinely not applicable, add a `deferred` queue row with rationale. Do not omit it.

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
