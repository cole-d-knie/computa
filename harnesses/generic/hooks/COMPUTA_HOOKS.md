# Generic Computa Hooks

For harnesses without native lifecycle hooks, use the portable hook runner directly.

Preflight:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py next
```

Closeout gate:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

Completion is blocked until the closeout gate passes.
