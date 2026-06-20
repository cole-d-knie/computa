---
name: computa-md
description: Explicit-only skill for archiving existing project agent docs and writing concise task-specific AGENTS.md, CLAUDE.md, KIMI.md, Cursor, Goose, Codex, and OpenCode guidance for the current Computa session. Use only when the user invokes /computa-md or explicitly asks for task-local agent docs.
---

# Computa MD

Run only when invoked directly. Do not run as an automatic hook from Export Control, 4D Chess, Make No Mistakes, docs updates, or closeout unless the user explicitly requests `/computa-md`.

## Purpose

Create task-local harness docs that survive context loss:

- old docs archived
- new docs short
- task clear
- Computa artifacts clear
- resume path clear
- constraints preserved

## Inputs

Use source truth in this order:

1. Explicit user request for `/computa-md`.
2. Current Computa session artifacts under `docs/computa-artifacts/`.
3. `user-task.md`, then `normalized-task.md`.
4. `activity-log.csv`, `session-ledger.csv`, phase/task ledgers, reports.
5. Existing project docs: `AGENTS.md`, `CLAUDE.md`, `KIMI.md`, `CODEX.md`, `OPENCODE.md`, Cursor rules, Goose recipes.
6. Repo files only as needed to preserve project-specific rules.

Do not guess from chat after compaction when artifacts disagree. Artifacts win.

## Archive First

Before writing new docs:

1. Find project root. Prefer `git rev-parse --show-toplevel`; otherwise use invocation root.
2. Ensure `docs/computa-artifacts/` exists. If absent, create it.
3. Create archive directory:
   - `docs/computa-artifacts/md-archive/MD-YYYYMMDD-HHMMSS/`
4. Archive every existing target doc before overwrite:
   - `AGENTS.md`
   - `CLAUDE.md`
   - `KIMI.md`
   - `CODEX.md`
   - `OPENCODE.md`
   - `.cursor/rules/*.mdc`
   - `.goose/recipes/*.yaml`
   - `.goose/recipes/*.yml`
5. Write archive records:
   - `summary.md`
   - `archive-ledger.csv`

CSV columns:

```csv
timestamp,source_path,archive_path,action,notes
```

No secret values in archives, summaries, generated docs, terminal output, or git.

## Preserve Project Rules

Read old docs before replacing them. Carry forward only durable, relevant rules:

- do-not-touch paths
- repo layout
- branch/base rules
- verification commands
- deployment constraints
- dashboard/database/secrets boundaries
- project-specific style rules
- known artifact paths

Drop stale chat, vague advice, duplicate boilerplate, and obsolete task state.

If a rule is unclear, keep it with `VERIFY:` instead of deleting it silently.

## Generated Files

Write these when relevant:

- `AGENTS.md`
- `CLAUDE.md`
- `KIMI.md`
- `CODEX.md`
- `OPENCODE.md`
- `.cursor/rules/computa-task.mdc`
- `.goose/recipes/computa-task.yaml`

If a harness is not used, still write a concise equivalent unless the repo convention says otherwise.

## Required Content

Every generated doc must include compact sections:

- `Task`
- `Top Skill`
- `Artifacts`
- `Resume`
- `Rules`
- `Style`
- `Verify`
- `Do Not`

Use terse fragments. Almost caveman. No long tutorial prose.

Must mention:

- current task from `user-task.md`
- normalized task path if present
- top-level skill in use: `computa-export-control`, `computa-4d-chess`, `computa-make-no-mistakes`, or explicit unknown
- artifact root: `docs/computa-artifacts/`
- active session path if known
- resume flow: run/read `computa-resume`, then inspect `activity-log.csv`, `session-ledger.csv`, latest session ledgers, latest reports
- source truth: artifacts over chat
- important inherited project constraints
- `docs/architecture/` location when present
- `docs/computa-artifacts/secrets-needed/` for missing keys
- no secret values in docs or git
- small modular files: ideal `<300` lines, most files `<500` lines, split giant files by responsibility
- verify with tests/runtime evidence before claiming done

## Tone Template

Use this style:

```md
# AGENTS.md

## Task
- Current: <task>
- Source: docs/computa-artifacts/.../user-task.md
- Normalized: docs/computa-artifacts/.../normalized-task.md

## Top Skill
- <skill>
- Use artifacts. Not chat memory.

## Artifacts
- Root: docs/computa-artifacts/
- Session: <path>
- Reports: <path>
- Secrets: docs/computa-artifacts/secrets-needed/

## Resume
- Run/read: /computa-resume
- Then: activity-log.csv
- Then: session-ledger.csv
- Then: latest phase/task ledgers
- Continue only from last safe status.

## Rules
- Preserve project constraints below.
- Do not touch forbidden paths.
- Update ledgers as work changes.

## Style
- Small files.
- Ideal <300 lines.
- Most <500 lines.
- Modular. Narrow APIs.

## Verify
- Tests first when behavior changes.
- Runtime QA when user-facing.
- Evidence before done.
```

## Cursor Output

`.cursor/rules/computa-task.mdc` must use Cursor frontmatter:

```md
---
description: "Task-local Computa guidance for this repo."
globs:
alwaysApply: true
---
```

Keep the body as terse as `AGENTS.md`.

## Goose Output

`.goose/recipes/computa-task.yaml` must be valid YAML.

Include:

- task summary
- artifact root
- resume instructions
- Computa skill stack
- verification rules
- modularity rule

Do not encode secrets.

## Completion

Before finishing:

- generated docs exist
- archived docs exist when there were prior docs
- archive ledger written
- summary written
- old project constraints preserved or marked `VERIFY:`
- no secret values added
- generated docs mention resume path and artifact root
- generated docs are concise

Final response: list generated files, archive path, and any preserved/unclear constraints.
