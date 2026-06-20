---
name: computa-secrets-needed
description: Shared Computa secret-requirement ledger skill. Use whenever Export Control, 4D Chess, Computa Make No Mistakes, or a nested task builds, specs, tests, or deploys functionality that needs an API key, OAuth credential, webhook secret, model-provider key, dashboard credential, deployment secret, or other private configuration value. Records what secret is needed, where it belongs, and a safe Computer Use handoff prompt without storing secret values.
---

# Computa Secrets Needed

Use this whenever work discovers that a secret is required, including API keys such as OpenRouter, OpenAI, Stripe, Vercel, Supabase, GitHub, Google, Meta, analytics providers, OAuth apps, webhooks, database URLs, signing keys, or deployment credentials.

Do not stop building just because a secret is missing unless the secret is required to choose the architecture safely and no mock, fixture, docs, local emulator, sandbox substitute, or owner decision can resolve the choice. Treat missing secrets as a keyless-test-design problem. Build with env placeholders, mocks, fakes, provider adapters, contract tests, fixture payloads, dry-run modes, and clear runtime guards, then record the missing secret and only the live-credential verification that remains blocked.

## Artifact Location

Use the project root selected by `computa-init`. Create or update:

- `docs/computa-artifacts/secrets-needed/`
- `docs/computa-artifacts/secrets-needed/index.md`
- `docs/computa-artifacts/secrets-needed/secrets-needed.csv`
- `docs/computa-artifacts/secrets-needed/computer-use-prompts/`

Never write actual secret values in `docs/computa-artifacts/`, chat, screenshots, test logs, git commits, or reports.

## Required CSV Fields

`secrets-needed.csv` must use:

`secret_id,provider,secret_name,env_var_names,target_env_paths,platform_targets,needed_for,discovered_by_session,discovered_in_phase_or_super_phase,code_paths,verification_blocked,status,owner_action,artifact_path,computer_use_prompt_path,created_at,updated_at`

Statuses:

- `needed`
- `provided`
- `configured`
- `verified_present`
- `verification_blocked`
- `not_needed`
- `owner_decision`

## Per-Secret Markdown

Create one Markdown file per secret:

`docs/computa-artifacts/secrets-needed/SECRET-YYYYMMDD-HHMMSS-provider-purpose.md`

Include:

- secret ID
- provider/service
- account/project/workspace/org expected
- secret name and env var names
- target local env path, such as `.env.local`, `.env`, `.env.production`, `.dev.vars`, or harness-specific env file
- target deployment/platform secret path, such as Vercel project env, Cloudflare Worker secret, GitHub Actions secret, Supabase Edge Function secret, Netlify env, Railway variable, or other system
- code paths that read the secret
- why the secret is needed
- what was built with placeholders, mocks, fakes, adapters, fixtures, contract tests, or dry-run modes
- exact behavior blocked until the secret is configured
- verification commands that can run before the secret exists
- verification commands/runtime QA that must run after the secret exists
- rotation/security notes
- owner action needed
- safe Computer Use prompt path

## Computer Use Prompt

For every needed secret, create:

`docs/computa-artifacts/secrets-needed/computer-use-prompts/SECRET-ID-computer-use-prompt.md`

The prompt must be copy-pasteable for a future Codex session and include:

```md
Task: Configure <provider/service> secret for <project>.

Use @Computer only after the user explicitly authorizes account access. If login is needed, let the user enter credentials or MFA interactively. Do not ask the user to paste passwords or API keys into chat.

Safety rules:
- Do not print, summarize, screenshot, or store the secret value.
- Do not write the secret value to docs/computa-artifacts, logs, reports, terminal history, or git.
- Write the value only to the target env file or platform secret field listed below.
- After configuration, verify only the key name/presence and functional behavior, never the raw value.

Secret to configure:
- Provider:
- Account/project/workspace:
- Secret/env var names:
- Target local env path:
- Target platform secret location:
- Code paths that require it:
- Post-config verification commands:
- Post-config runtime QA:

Steps:
1. Open the provider/dashboard or local target path.
2. Have the user complete login/MFA if needed.
3. Create or reveal the needed secret according to provider UI.
4. Copy the value directly into the target env/platform secret field.
5. Save the file/platform setting without exposing the value.
6. Run the listed verification.
7. Update the per-secret Markdown status and `secrets-needed.csv` without including the secret value.
```

## Build Policy

When a secret is missing:

- Continue architecture/spec/build work using a documented env var name and placeholder example.
- Add runtime validation that fails clearly when the env var is absent.
- Add tests for missing-secret behavior when applicable.
- Add keyless tests for secret-dependent behavior wherever possible: request construction, response parsing, validation, retries, error handling, synthetic webhook/event handling, provider adapter contracts, fixture payloads, dry-run behavior, and missing/invalid credential paths.
- Do not commit real secrets.
- Do not silently disable the feature.
- Mark runtime/deployment verification as blocked only when it truly requires the live secret.

## Closeout

Every Computa closeout, 4D closeout, and Export Control closeout must report:

- whether `docs/computa-artifacts/secrets-needed/` exists
- new secrets added or updated
- verification blocked by missing secrets
- target env/platform paths
- where to find the Computer Use prompts

Golden rule: secret values never belong in artifacts; only names, destinations, status, and safe handoff instructions do.
