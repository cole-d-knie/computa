---
name: computa-export-control-prior-art
description: Focused Computa Export Control research skill for finding prior implementations, open-source examples, reference architectures, reusable code patterns, demos, templates, and lessons learned. Use to determine whether the requested feature/system has been built before and what can be reused safely.
---

# Computa Export Control Prior Art

Use this to avoid reinventing the wheel.

If invoked directly and `docs/computa-artifacts/activity-log.csv` exists or can be initialized, append `research_task_started` before research and `research_task_completed`, `research_task_blocked`, or `research_task_deferred` after it, with `scope_name=prior-art` and `artifact_path=prior-art/`.

## Research Targets

Search for:

- open-source repos and examples
- official sample apps and templates
- reference architectures
- blog posts or talks with implementation detail
- issue threads that reveal pitfalls
- comparable products or workflows
- internal prior artifacts, reports, branches, PRs, or docs

Use web, GitHub, package registries, local repo search, and docs tools when available.

## License And Reuse Rules

- Record the license before recommending code reuse.
- Prefer ideas, APIs, architecture, tests, and patterns over copying code.
- Do not copy code from incompatible, unclear, or missing-license sources.
- If reuse is allowed, record attribution needs and exact source paths/URLs.
- Treat generated snippets and copied examples as untrusted until tested and reviewed.

## Outputs

Write under `prior-art/`:

- `prior-art-map.md`: what similar work exists and what it teaches.
- `reusable-patterns.md`: patterns worth adapting.
- `repo-shortlist.csv`: repo/source, owner, URL/path, license, stars/activity if available, relevance, risk, recommendation.
- `implementation-lessons.md`: pitfalls, edge cases, test ideas, architecture warnings.
- `reuse-permissions.md`: license/attribution summary and allowed/prohibited reuse.

## Rules

- Compare prior art against the actual codebase and task constraints.
- Prefer mature, well-tested patterns over novelty.
- Call out when no good prior art exists and a custom build is justified.
- Preserve source links and dates checked for every material claim.
