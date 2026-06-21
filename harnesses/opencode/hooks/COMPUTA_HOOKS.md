# OpenCode Computa Hooks

OpenCode installs Computa skill instructions through `opencode.json`. With `--install-hooks`, it also installs a native local plugin:

- global: `~/.config/opencode/plugins/computa-hooks.js`
- project: `<project>/.opencode/plugins/computa-hooks.js`

The plugin calls the portable hook runner on session, tool, permission, file edit, shell, and compaction events.

Recommended wrapper commands:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py next
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

The plugin already wires lifecycle events to the runner. For manual checks:

```bash
python3 /path/to/computa/scripts/computa_hooks.py hook --format opencode --event SessionStart
python3 /path/to/computa/scripts/computa_hooks.py hook --format opencode --event Stop --closeout --strict
```
