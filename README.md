# Swarm Verify Skills

Private multi-harness skill package for phased, evidence-first task execution.

## Recommendation

Keep this as a package, not one large skill.

The master `swarm-verify` skill orchestrates the workflow. Focused sub-skills own the repeatable parts:

- `swarm-verify-setup`: Phase 0 artifact setup, `user-task.md`, ledgers, tasks, subtasks.
- `swarm-verify-investigate`: Phase 1 source-truth investigation and baseline evidence.
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

- Codex installs the Codex-compatible dependency folders.
- Claude Code prefers the existing Claude-compatible `~/.claude/skills/investigate` when present.
- Kimi skips `subagent-driven-development` and uses Kimi agent swarm/delegation wording.
- OpenCode installs standard `SKILL.md` folders into its native global skills directory.
- Cursor uses an `.mdc` rule because Cursor rules are project-scoped instructions, not the same skill runtime.
- Goose uses a recipe because Goose packages reusable workflows as recipes.

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

Claude Code:

```bash
./install.sh --harness claude-code
```

Kimi Code:

```bash
./install.sh --harness kimi
```

OpenCode:

```bash
./install.sh --harness opencode
```

Cursor for a project:

```bash
./install.sh --harness cursor --project /path/to/project
```

Goose:

```bash
./install.sh --harness goose
goose run --recipe ~/.config/goose/recipes/swarm-verify.yaml --recipe-param task="audit PR 23 and 25"
```

Shared Agent Skills folder:

```bash
./install.sh --harness agent-skills
```

Generic fallback file:

```bash
./install.sh --harness generic --project /path/to/project
```

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

## Use

Codex, Claude Code, Kimi, OpenCode, and Agent Skills harnesses:

```text
/swarm-verify complete this task: ...
```

Cursor:

```text
Use the swarm-verify Cursor rule to complete this task: ...
```

Goose:

```bash
goose run --recipe ~/.config/goose/recipes/swarm-verify.yaml --recipe-param task="complete this task: ..."
```

## Required Behavior

The workflow must:

- save the raw request to `user-task.md` immediately
- create external artifacts outside the repo
- use phased planning
- run investigation before implementation
- use TDD for behavior changes
- run runtime QA and Playwright/browser checks when relevant
- run adversarial and judge/verifier swarms after each task and phase
- keep ledgers current
- make one commit per verified task when commits are allowed
- finish with concise Markdown reports for summary, verification needed, blockers/open issues, task gaps, and new issues found fixed/not fixed

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
