# Swarm Verify Skills

Private Codex skill suite for phased, evidence-first task execution.

## Recommendation

Yes: keep this as a small skill package, not one large skill.

The master `swarm-verify` skill orchestrates the workflow. Focused sub-skills own the repeatable parts:

- `swarm-verify-setup`: Phase 0 artifact setup, `user-task.md`, ledgers, tasks, subtasks.
- `swarm-verify-investigate`: Phase 1 source-truth investigation and baseline evidence.
- `swarm-verify-tdd-qa`: TDD, edge cases, unit/integration/smoke/runtime QA, Playwright.
- `swarm-verify-swarms`: task and phase adversarial plus judge/verifier swarms.
- `swarm-verify-closeout`: final reports, gap analysis, blockers, verification needs, commits.

This reduces context pressure while keeping the full master prompt available at:

`skills/swarm-verify/references/master-swarm-verification-prompt.md`

## Dependencies

The installer includes lightweight vendored dependency skills:

- `caveman`
- `gstack-investigate` whose skill name is `investigate`
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

Important: `gstack-investigate` expects the heavier `gstack` core skill at runtime. The installer checks for it. It does not vendor `gstack` core by default because it is large and machine-specific.

## Install

```bash
git clone git@github.com:cole-d-knie/swarm-verify-skills.git
cd swarm-verify-skills
./install.sh
```

The default target is:

```bash
${CODEX_HOME:-$HOME/.codex}/skills
```

Install to a custom target:

```bash
./install.sh --target "$HOME/.codex/skills"
```

Preview without writing:

```bash
./install.sh --dry-run
```

If a machine already has local `gstack` core and you want the installer to copy it:

```bash
./install.sh --install-local-gstack
```

If `gstack` is in a nonstandard location:

```bash
./install.sh --install-local-gstack --gstack-source /path/to/gstack
```

## Use

```text
/swarm-verify complete this task: ...
```

The skill must immediately save the raw request to `user-task.md`, create external artifacts, run investigation before implementation, use TDD and runtime QA, run task/phase swarms, and finish with concise Markdown reports.

## Validation

Validate suite skills with:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/swarm-verify
python3 /path/to/skill-creator/scripts/quick_validate.py skills/swarm-verify-setup
python3 /path/to/skill-creator/scripts/quick_validate.py skills/swarm-verify-investigate
python3 /path/to/skill-creator/scripts/quick_validate.py skills/swarm-verify-tdd-qa
python3 /path/to/skill-creator/scripts/quick_validate.py skills/swarm-verify-swarms
python3 /path/to/skill-creator/scripts/quick_validate.py skills/swarm-verify-closeout
```
