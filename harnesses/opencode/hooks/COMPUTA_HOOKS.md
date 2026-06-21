# OpenCode Computa Hooks

OpenCode installs Computa skill instructions through `opencode.json`. Use the portable hook runner as the deterministic enforcement layer.

Recommended wrapper commands:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py next
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

If your OpenCode setup supports hook/plugin execution, wire those lifecycle events to:

```bash
python3 /path/to/computa/scripts/computa_hooks.py hook --event SessionStart
python3 /path/to/computa/scripts/computa_hooks.py hook --event Stop --closeout --strict
```
