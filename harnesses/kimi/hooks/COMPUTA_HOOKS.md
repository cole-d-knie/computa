# Kimi Computa Hooks

Kimi hook enforcement is implemented as portable preflight/closeout commands plus skill instructions.

Run before Computa work:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py next
```

Run before claiming completion:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

Kimi agents must treat a nonzero exit code as a blocker and repair/reconcile `docs/computa-artifacts/execution-queue.csv` before continuing.
