---
name: computa-export-control-tech-radar
description: Focused Computa Export Control web-research skill for finding and evaluating technologies, packages, SaaS tools, APIs, frameworks, SDKs, and libraries that may help a project. Use when deciding whether to build, buy, import, add a dependency, or avoid reinventing existing work.
---

# Computa Export Control Tech Radar

Use this for current technology and package research.

If invoked directly and `docs/computa-artifacts/activity-log.csv` exists or can be initialized, append `research_task_started` before research and `research_task_completed`, `research_task_blocked`, or `research_task_deferred` after it, with `scope_name=tech-radar` and `artifact_path=tech-radar/`.

## Research Sources

Use current web research when available. Prefer:

- official docs and changelogs
- package registries
- GitHub repos, releases, issues, examples, and license files
- security advisories and vulnerability databases when available
- vendor docs and pricing pages for SaaS/API options
- credible engineering case studies only as secondary evidence

Use `context7` for current library/API docs when available. Record search queries and dates checked.

## Evaluation Criteria

For each option, assess:

- fit for the task and codebase
- license and attribution obligations
- maintenance activity and ecosystem health
- API stability and version compatibility
- security and privacy posture
- bundle/runtime/performance cost
- implementation complexity
- lock-in, migration path, and reversibility
- testability and observability
- required API keys, OAuth scopes, webhook secrets, provider accounts, rate-limit tiers, and whether missing credentials block verification
- whether it encourages modular code or giant files

## Outputs

Write under `tech-radar/`:

- `tech-radar.md`: adopt/trial/hold/avoid recommendations.
- `package-shortlist.csv`: name, source, version/date checked, license, fit, risk, recommendation.
- `integration-notes.md`: install/setup notes, APIs, docs links, gotchas.
- `secrets-needed.md`: required private config, target env/platform paths, owner actions, and links to `docs/computa-artifacts/secrets-needed/` entries.
- `build-vs-buy.md`: when to use an existing package/tool versus custom code.
- `security-license-notes.md`: license, security, privacy, and compliance concerns.

## Rules

- Do not recommend adding a dependency without evidence that it beats local implementation.
- Do not reject a proven library just because a custom implementation is possible.
- Prefer small focused packages and local adapters over large framework pivots unless the project genuinely needs the larger tool.
- If an option requires an API key, SaaS account, OAuth app, webhook secret, model-provider token, or deployment secret, invoke `computa-secrets-needed` and record safe setup/verification requirements without storing values.
- Mark stale or unverifiable findings clearly.
