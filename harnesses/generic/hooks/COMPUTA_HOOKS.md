# Generic Computa Hooks

For harnesses without native lifecycle hooks, use the portable hook runner directly.

Preflight:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py expand
python3 /path/to/computa/scripts/computa_hooks.py next
```

Closeout gate:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

The shared contract is `templates/computa-execution-contract.md`. Completion is blocked until the closeout gate passes. Parent rows must have terminal children, completed sessions must have required artifact shape, and broad staging commands such as `git add .`, `git add -A`, `git add --all`, `git add -u`, and `git add :/` are forbidden.
