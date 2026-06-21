# GLM Computa Project Notes

Computa is available through GLM Coding Plan by running a GLM-configured coding tool such as Claude Code or OpenCode.

## Use

1. Configure GLM Coding Plan for the tool:

```bash
npx @z_ai/coding-helper
```

2. Run Computa from the tool:

```text
/computa-export-control <task>
```

For medium work:

```text
/computa-make-no-mistakes <task>
```

For ultra-long work:

```text
/computa-4d-chess <task>
```

## Important

- Do not commit Z.ai API keys.
- If keys are missing, use Computa keyless behavior: mocks, fixtures, adapters, dry-run modes, and `docs/computa-artifacts/secrets-needed/`.
- If hooks are installed and block completion, reconcile `docs/computa-artifacts/execution-queue.csv`.

