---
description: "Computa hook enforcement for execution queues, resume, and closeout gates."
globs:
alwaysApply: false
---

# Cursor Computa Hooks

Cursor project rules provide soft hook enforcement. Use the portable hook runner for hard checks in terminal, CI, or pre-commit wrappers.

Run before Computa work:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py next
```

Run before closeout:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

If the closeout command fails, do not claim completion. Reconcile queue rows, ledgers, reviews, evidence, and docs hooks first.
