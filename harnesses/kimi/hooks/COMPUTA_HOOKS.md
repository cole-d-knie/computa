# Kimi Computa Hooks

Kimi hook enforcement is implemented with native `[[hooks]]` entries in `~/.kimi-code/config.toml`.

Install:

```bash
./install.sh --harness kimi --install-hooks
```

The installer appends or replaces the `# BEGIN COMPUTA HOOKS` managed block from `harnesses/kimi/hooks/config-hooks.toml`. Kimi passes hook JSON on stdin, uses exit code `2` to block, and runs hook commands from the active project directory.

Run before Computa work:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --strict
python3 /path/to/computa/scripts/computa_hooks.py expand
python3 /path/to/computa/scripts/computa_hooks.py next
```

Run before claiming completion:

```bash
python3 /path/to/computa/scripts/computa_hooks.py validate --closeout --strict
```

Kimi agents must treat a hook block as a real blocker and repair/reconcile `docs/computa-artifacts/execution-queue.csv` before continuing.

Hook-added queue rows are real. Consume the highest-priority ready row instead of re-planning from chat context.
