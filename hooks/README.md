# Computa Hooks

Computa hooks are deterministic checks around the agent loop. They do not replace the skills; they enforce the artifact and queue contract the skills depend on.

## Portable Commands

Run from a project root:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py next
python3 /path/to/computa/scripts/computa_hooks.py expand
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

The contract these commands enforce is documented at `templates/computa-execution-contract.md`.

Use `COMPUTA_ROOT=/path/to/project` when the harness does not pass a working directory.

## Hook Modes

- `SessionStart` / `UserPromptSubmit`: add context reminding the agent to use the queue.
- `expand`: deterministically append missing queue rows for known parent skills and recursive routing.
- `PreToolUse` / `BeforeShellExecution`: optionally block unsafe closeout attempts when the queue is invalid.
- `PreToolUse` / `PermissionRequest`: block broad `git add .`, `git add -A`, `git add --all`, `git add -u`, and `git add :/`; agents must stage intentional files explicitly.
- `Stop` / `SessionEnd`: block completion when required queue rows are still active.
- `resume`: use `validate` and `next` before relying on chat history.

## Recursive Skill Routing

Hooks do not secretly spawn model sessions or run skills in the background. That would be unreliable across Codex, Claude Code, Kimi, OpenCode, Cursor, and Goose.

Instead, the hook runner makes recursive invocation unavoidable through the queue:

1. It detects active Export Control, 4D Chess, and Computa Make No Mistakes sessions.
2. On session/prompt/compaction hooks, it expands deterministic queue structure without prompting:
   - missing parent rows from `session-ledger.csv`
   - required child-skill rows for Export Control, 4D Chess, and Make No Mistakes
   - recursive campaign/Super-Phase rows that route to the next required skill
3. It checks that required child-skill queue rows exist or are explicitly deferred with rationale.
4. It checks recursive execution routing:
   - Export Control campaign execution must route to `/computa-4d-chess`.
   - 4D Chess Super-Phase execution must route to `/computa-make-no-mistakes`.
   - Export Control final security closeout must route through `/computa-make-no-mistakes`, which invokes `/security-audit` once when applicable.
5. It injects the exact next queue item and required skill invocation into session/prompt/compaction context.
6. It blocks final `Stop` / `SessionEnd` if child-skill expansion or recursive routing was skipped.

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
4. Completed parent rows must have terminal required child rows.
5. Completed Export Control, 4D Chess, and Make No Mistakes sessions must have required artifact shape.
6. Resume starts from the highest-priority safe queue item.
