---
description: "Computa hook enforcement for execution queues, resume, and closeout gates."
globs:
alwaysApply: false
---

# Cursor Computa Hooks

Cursor uses native hook JSON plus project rules.

Install:

```bash
./install.sh --harness cursor --project /path/to/project --install-hooks
```

The installer merges native Cursor hooks into `<project>/.cursor/hooks.json` or `~/.cursor/hooks.json`, and keeps this rule file as readable context.

Run before Computa work:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py expand
python3 /path/to/computa/scripts/computa_hooks.py next
```

Run before closeout:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

The shared contract is `templates/computa-execution-contract.md`. It requires recursive skill routing, terminal child rows before parent completion, required artifact shape, and explicit file staging.

If the closeout command fails, do not claim completion. Reconcile queue rows, ledgers, reviews, evidence, and docs hooks first.

Hook-added rows are intentional deterministic expansions. Consume them through the queue.

Do not use `git add .`, `git add -A`, `git add --all`, `git add -u`, or `git add :/`. Stage intentional files explicitly.
