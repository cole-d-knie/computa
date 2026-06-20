# Computa Make No Mistakes Skills

Private multi-harness skill package for phased, evidence-first task execution.

## Recommendation

Keep this as a package, not one large skill.

The package has three execution levels:

- `computa-export-control`: research/intelligence layer for massive projects. It prevents reinvention, audits the codebase, researches technologies/packages/prior art/skills/tools, clarifies requirements, then quarterbacks sequential 4D Chess campaigns.
- `computa-4d-chess`: Super-Phase layer for ultra-long autonomous tasks, large edits, large system additions, and major build-from-scratch projects.
- `computa-make-no-mistakes`: phase/task layer for Jira tasks, bugfixes, system additions, code edits, and medium-scope build-from-scratch tasks.

Focused sub-skills own the repeatable parts:

- `computa-speak`: rewrites raw prompts into concise AI-ready task prompts while preserving the original request as source truth.
- `computa-init`: initializes `docs/computa-artifacts/`, session ledgers, raw task capture, and shared artifact structure.
- `computa-resume`: inspects `docs/computa-artifacts/activity-log.csv`, session ledgers, and nested session artifacts to identify the latest safe resume point after a crash or context loss.
- `computa-secrets-needed`: records required API keys, OAuth credentials, webhook secrets, model-provider keys, deployment secrets, dashboard credentials, target env/platform paths, blocked verification, and safe `@Computer` credential handoff prompts without storing secret values.
- `computa-docs-architecture`: creates or updates source-backed docs at `docs/architecture/`.
- `computa-docs-architecture-init`: initializes the `docs/architecture/` skeleton.
- `computa-docs-architecture-audit`: audits code and existing architecture docs against source truth.
- `computa-docs-architecture-update`: applies source-backed architecture doc updates.
- `computa-make-no-mistakes-docs-update`: end-of-phase hook that updates or builds `docs/architecture/`.
- `computa-export-control-design`: research, requirements, codebase audit, technical specs, decision matrix, and 4D campaign design.
- `computa-export-control-execute`: sequentially executes approved 4D Chess campaigns and reconciles results.
- `computa-export-control-product-requirements`: product goals, workflows, acceptance criteria, creative options, owner decisions.
- `computa-export-control-codebase-audit`: architecture/dependency/modularity/test/runtime audit.
- `computa-export-control-tech-radar`: web research for packages, SaaS, APIs, frameworks, and tools.
- `computa-export-control-prior-art`: web/GitHub/local research for prior implementations and reusable patterns.
- `computa-export-control-skill-mcp-intake`: local/importable skills, MCPs, plugins, connectors, and harness capabilities.
- `computa-export-control-technical-spec`: execution-grade engineering specs with module boundaries, contracts, flows, data, integrations, rollout, test strategy, implementation slices, and acceptance contract.
- `computa-export-control-implementation-strategy`: solves hard engineering challenges, keyless test strategy, integration risks, migration/rollout risks, and campaign readiness before 4D Chess starts.
- `computa-export-control-audit-suite`: runs security, performance, and UI audits in documentation mode, then consolidates findings into a 4D implementation backlog.
- `computa-4d-chess`: one-command Super-Phase entrypoint for very large tasks; runs architect, build, then execute.
- `computa-4d-chess-architect`: audits, specs, designs, and records decisions before Super-Phase planning.
- `computa-4d-chess-build`: creates Super-Phase design, ledgers, maps, handoffs, and review gates.
- `computa-4d-chess-execute`: executes approved Super-Phases through `computa-make-no-mistakes`.
- `security-audit`: security findings/hardening skill; Export Control uses it in documentation mode and 4D Chess runs it through `SP-999-post-run-security-audit`.
- `performance-audit`: performance findings/optimization skill for Export Control audit documentation and direct optimization work.
- `ui-audit`: UI/UX findings/polish skill for Export Control audit documentation and direct UI work.
- `computa-make-no-mistakes`: one command that loads the master skill, every subskill, and the full dependency set.
- `swarm-verify`: master orchestration and parity reference routing.
- `swarm-verify-setup`: Phase 0 artifact setup, `user-task.md`, ledgers, tasks, subtasks.
- `swarm-verify-investigate`: Phase 1 orientation audit/maps plus Phase 2 source-truth investigation and baseline evidence.
- `swarm-verify-tdd-qa`: TDD, edge cases, unit/integration/smoke/runtime QA, Playwright.
- `swarm-verify-swarms`: task and phase adversarial plus judge/verifier swarms.
- `swarm-verify-closeout`: final reports, gap analysis, blockers, verification needs, commits.

The full parity prompt remains available at:

`skills/swarm-verify/references/master-swarm-verification-prompt.md`

## Supported Harnesses

| Harness | Install path / adapter | Notes |
| --- | --- | --- |
| Codex | `${CODEX_HOME:-~/.codex}/skills` | Native `SKILL.md` folders. |
| Claude Code | `~/.claude/skills` | Native Agent Skills folders. A Claude plugin-shaped copy is also in `harnesses/claude-code/plugin`. |
| Kimi Code | `~/.kimi-code/skills` plus `~/.kimi-code/config.toml` `extra_skill_dirs` | Kimi-specific copy uses "agent swarm/delegation" wording and does not require Codex `subagent-driven-development`. |
| OpenCode | `~/.config/opencode/skills` | Native Agent Skills folders. |
| Cursor | `.cursor/rules/swarm-verify.mdc` for a project, or staged at `~/.cursor/rules` | Cursor project rules are the reliable path. Cursor may also import Claude skills/plugins if enabled in Cursor settings. |
| Goose | `~/.config/goose/recipes/swarm-verify.yaml` | Run as a Goose recipe. |
| Agent Skills open standard | `~/.agents/skills` | Useful for tools that read shared Agent Skills folders. |
| Generic | `AGENTS.swarm-verify.md` | Fallback instructions for harnesses without native skill support. |

## Dependencies

See [`DEPENDENCIES.md`](DEPENDENCIES.md) for upstream GitHub/npm provenance and per-harness compatibility notes.

Vendored lightweight dependency skills:

- `caveman`
- `context7`
- `gstack-investigate` / `investigate`
- `playwright`
- `using-superpowers`
- `writing-plans`
- `executing-plans`
- `test-driven-development`
- `systematic-debugging`
- `dispatching-parallel-agents`
- `subagent-driven-development`
- `requesting-code-review`
- `verification-before-completion`

Dependency handling is harness-specific:

- Codex installs the Codex-compatible dependency folders into `${CODEX_HOME:-~/.codex}/skills`.
- Claude Code installs dependency folders into `~/.claude/skills`; the plugin adapter also includes dependency skills and `.mcp.json`.
- Kimi installs Kimi-compatible skills, updates `~/.kimi-code/config.toml`, and adds missing Context7/Playwright entries to `~/.kimi-code/mcp.json`.
- OpenCode installs skills, then merges `~/.config/opencode/opencode.json` with instruction paths and Context7/Playwright MCP entries.
- Cursor installs a project/global `.mdc` rule and adds missing Context7/Playwright entries to project/global `mcp.json`.
- Goose installs a recipe with developer, Context7, and Playwright extensions.

Important: full `gstack` core is not vendored because it is large and machine-specific. The installer checks for it and can copy a local one with `--install-local-gstack`.

## Install

Clone:

```bash
git clone git@github.com:cole-d-knie/swarm-verify-skills.git
cd swarm-verify-skills
```

Codex:

```bash
./install.sh --harness codex
```

Installs suite and dependencies to `${CODEX_HOME:-~/.codex}/skills`. Use `--install-local-gstack` if you want to copy a local full `gstack` core.

Claude Code:

```bash
./install.sh --harness claude-code
```

Installs suite and dependencies to `~/.claude/skills`. The Claude plugin-shaped package is available at `harnesses/claude-code/plugin` and includes `.mcp.json` for Context7 and Playwright.

Kimi Code:

```bash
./install.sh --harness kimi
```

Installs Kimi-specific skills, updates `~/.kimi-code/config.toml` `extra_skill_dirs`, and adds missing Context7/Playwright MCP servers to `~/.kimi-code/mcp.json`. Kimi wording uses agent swarm/delegation and does not require `subagent-driven-development`.

OpenCode:

```bash
./install.sh --harness opencode
```

Installs skills to `~/.config/opencode/skills` and merges `~/.config/opencode/opencode.json` with `instructions` entries and MCP servers. Reference template: `harnesses/opencode/opencode.swarm-verify.json`.

Cursor for a project:

```bash
./install.sh --harness cursor --project /path/to/project
```

Installs `/path/to/project/.cursor/rules/swarm-verify.mdc` and merges `/path/to/project/.cursor/mcp.json` with Context7 and Playwright. Without `--project`, the installer stages global files under `~/.cursor`.

Goose:

```bash
./install.sh --harness goose
goose run --recipe ~/.config/goose/recipes/swarm-verify.yaml --recipe-param task="audit PR 23 and 25"
```

Installs a Goose recipe with the developer extension plus Context7 and Playwright stdio extensions.

Shared Agent Skills folder:

```bash
./install.sh --harness agent-skills
```

Installs suite and dependency skills to `~/.agents/skills`.

Generic fallback file:

```bash
./install.sh --harness generic --project /path/to/project
```

Installs `AGENTS.swarm-verify.md` for harnesses that do not support these skills directly.

Install all supported local targets:

```bash
./install.sh --harness all --project /path/to/project
```

Preview without writing:

```bash
./install.sh --harness all --project /path/to/project --dry-run
```

Copy a local `gstack` core if available:

```bash
./install.sh --harness codex --install-local-gstack
./install.sh --harness claude-code --install-local-gstack
```

Use a custom gstack source:

```bash
./install.sh --harness codex --install-local-gstack --gstack-source /path/to/gstack
```

Skip dependency skills:

```bash
./install.sh --harness codex --skip-deps
```

Skip MCP config mutation while still installing skills:

```bash
./install.sh --harness all --project /path/to/project --no-mcp-config
```

Skip Kimi `config.toml` mutation:

```bash
./install.sh --harness kimi --no-kimi-config
```

## Use

Codex, Claude Code, Kimi, OpenCode, and Agent Skills harnesses:

```text
/computa-export-control research and execute this massive project: ...
```

Ultra-long 4D task:

```text
/computa-4d-chess complete this large task: ...
```

Normal Computa task:

```text
/computa-make-no-mistakes complete this task: ...
```

Architecture docs:

```text
/computa-docs-architecture audit this codebase and build or update docs/architecture
```

Prompt cleanup:

```text
/computa-speak rewrite this raw task into a concise AI-ready coding prompt
```

Resume interrupted work:

```text
/computa-resume find the latest Computa work and tell me where to resume
```

Advanced internal master skill:

```text
/swarm-verify complete this task: ...
```

Cursor:

```text
Use the computa-make-no-mistakes Cursor rule to complete this task: ...
```

Goose:

```bash
goose run --recipe ~/.config/goose/recipes/swarm-verify.yaml --recipe-param task="complete this task: ..."
```

## Required Behavior

The workflow must:

- use `computa-export-control` for massive work that needs research, requirements analysis, technology/package/prior-art discovery, codebase audit, and sequential 4D Chess campaigns
- use `computa-export-control-technical-spec` before 4D campaign design when work needs concrete engineering contracts instead of broad product or architecture prose
- use `computa-export-control-implementation-strategy` before 4D campaign design when hard engineering issues, provider integrations, missing keys, migrations, state/concurrency risks, unclear testability, or rollout hazards could affect implementation
- run `computa-export-control-audit-suite` after Export Control research/spec work and before final 4D campaign design for existing codebases/apps
- include final `SP-999-post-run-security-audit` in every 4D Chess Super-Phase plan, executed through `computa-make-no-mistakes`, before marking the 4D session complete
- use `computa-4d-chess` for work that needs Super-Phases above normal Computa phases
- use `computa-make-no-mistakes` for Jira tasks, edits, system additions, bugfixes, and medium-scope scratch builds
- use `computa-docs-architecture` to create or update source-backed `docs/architecture/` docs, and use `computa-make-no-mistakes-docs-update` after every Computa phase
- read existing `docs/architecture/` first when Export Control, 4D Chess, or Computa runs on an existing codebase, then verify the docs against source
- run `computa-speak` immediately after raw request capture for direct Export Control, 4D Chess, or Make No Mistakes invocations; save the raw prompt unchanged and feed the optimized `normalized-task.md` to downstream skills
- audit the existing codebase first when Export Control or 4D Chess is used on an existing repo
- save the raw request to `user-task.md` immediately
- create `docs/` if missing and create or reuse `docs/computa-artifacts/` in the invocation/project root
- keep architecture docs as a sibling directory at `docs/architecture/`; never place the actual architecture docs under `docs/computa-artifacts/`
- gitignore `docs/computa-artifacts/` when it is inside a git repo
- support multiple sessions in one project with root `session-ledger.csv` entries and nested Export Control -> 4D Chess -> Computa child session directories
- maintain root `docs/computa-artifacts/activity-log.csv` for crash recovery, logging session/campaign/Super-Phase/phase/task start, finish, block, and defer events as they happen
- use `computa-resume` to recover the latest top-level or nested work item from `activity-log.csv`, `session-ledger.csv`, and local ledgers before relying on chat history
- update `docs/computa-artifacts/secrets-needed/` whenever any layer needs an API key, OAuth credential, webhook secret, model-provider token, deployment secret, dashboard credential, or other private config
- continue building/specing/testing with env var names, placeholders, mocks, fakes, provider adapters, contract tests, fixtures, dry-run modes, guards, and missing-secret tests; mark only real credential-dependent runtime/deploy verification as blocked
- treat missing API keys/private config as a keyless-test-design problem, not a reason to stop, unless the key is required to choose a safe architecture and no mock, fixture, docs, sandbox substitute, or owner decision can resolve it
- never store actual secret values in code, artifacts, logs, reports, screenshots, terminal output, or git; only store names, target env/platform paths, owner actions, and safe `@Computer` prompts
- prefer small, modular, readable components over giant files
- use phased planning
- invoke the full dependency set from every swarm-verify skill/subskill when run independently
- run an initial orientation audit of the task/codebase and save living maps under `maps/`
- allow maps to change at any time when evidence changes, tracking each material map update in both `maps/map-change-log.md` and `maps/map-change-ledger.csv`
- run investigation before implementation
- use TDD for behavior changes
- run runtime QA and Playwright/browser checks when relevant
- run adversarial and judge/verifier swarms after each task and phase
- keep ledgers current
- make one commit per verified task when commits are allowed
- finish with concise Markdown reports for summary, verification needed, blockers/open issues, task gaps, map artifacts, and new issues found fixed/not fixed

## Validation

Validate suite skills:

```bash
for d in skills/*; do python3 /path/to/quick_validate.py "$d"; done
```

Validate vendored skills:

```bash
for d in vendor/skills/*; do python3 /path/to/quick_validate.py "$d"; done
```

Validate Goose recipe:

```bash
goose recipe validate harnesses/goose/recipes/swarm-verify.yaml
```
