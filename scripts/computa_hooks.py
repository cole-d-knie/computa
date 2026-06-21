#!/usr/bin/env python3
"""Portable Computa hook runner and artifact validator.

This script is intentionally dependency-free so it can run from Codex, Claude
Code, Kimi, OpenCode, Cursor, Goose, generic shells, CI, and git hooks.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


QUEUE_HEADER = [
    "queue_id",
    "parent_queue_id",
    "session_id",
    "layer",
    "scope_type",
    "scope_id",
    "scope_name",
    "skill",
    "action",
    "priority",
    "status",
    "dependencies",
    "non_overlap_key",
    "allowed_parallelism",
    "required_outputs",
    "review_gate",
    "artifact_path",
    "evidence_path",
    "next_action",
    "created_at",
    "started_at",
    "completed_at",
    "notes",
]
ACTIVITY_HEADER = [
    "timestamp",
    "session_id",
    "layer",
    "parent_session_id",
    "event_type",
    "scope_type",
    "scope_id",
    "scope_name",
    "status",
    "artifact_path",
    "evidence_path",
    "next_action",
    "notes",
]

ACTIVE_STATUSES = {"queued", "ready", "running", "review_needed"}
DONE_STATUSES = {"complete", "deferred", "blocked", "superseded"}
VALID_STATUSES = ACTIVE_STATUSES | DONE_STATUSES | {"failed"}
BLOCKING_CLOSEOUT_STATUSES = ACTIVE_STATUSES | {"failed"}
TEXT_HOOK_FORMATS = {"text", "generic", "kimi", "cursor", "opencode", "goose"}
JSON_HOOK_FORMATS = {"json", "codex", "claude", "claude-code"}
CONTEXT_EVENTS = {
    "SessionStart",
    "SubagentStart",
    "UserPromptSubmit",
    "PreCompact",
    "PostCompact",
    "PostToolBatch",
}
SESSION_TERMINAL_STATUSES = {
    "deferred",
    "blocked",
    "superseded",
    "session_blocked",
}
ROUTING_EXEMPT_STATUSES = {"deferred", "blocked", "superseded"}
EXPAND_EVENTS = {"SessionStart", "UserPromptSubmit", "PreCompact", "PostCompact"}
LAYER_SKILL = {
    "export-control": "computa-export-control",
    "export_control": "computa-export-control",
    "4d-chess": "computa-4d-chess",
    "4d_chess": "computa-4d-chess",
    "computa": "computa-make-no-mistakes",
}
SKILL_LAYER = {
    "computa-export-control": "export-control",
    "computa-4d-chess": "4d-chess",
    "computa-make-no-mistakes": "computa",
}
REQUIRED_CHILD_SKILLS = {
    "computa-export-control": [
        "computa-init",
        "computa-speak",
        "computa-execution-queue",
        "computa-export-control-codebase-audit",
        "computa-export-control-product-requirements",
        "computa-export-control-tech-radar",
        "computa-export-control-prior-art",
        "computa-export-control-skill-mcp-intake",
        "computa-export-control-technical-spec",
        "computa-export-control-implementation-strategy",
        "computa-export-control-audit-suite",
        "computa-export-control-design",
        "computa-export-control-execute",
        "computa-make-no-mistakes",
    ],
    "computa-4d-chess": [
        "computa-init",
        "computa-speak",
        "computa-execution-queue",
        "computa-4d-chess-architect",
        "computa-4d-chess-build",
        "computa-4d-chess-execute",
    ],
    "computa-make-no-mistakes": [
        "computa-init",
        "computa-swarm-verify",
        "computa-swarm-verify-setup",
        "computa-speak",
        "computa-execution-queue",
        "computa-swarm-verify-investigate",
        "computa-swarm-verify-tdd-qa",
        "computa-swarm-verify-swarms",
        "computa-make-no-mistakes-docs-update",
        "computa-swarm-verify-closeout",
    ],
}
CHILD_REQUIRED_OUTPUTS = {
    "computa-init": "artifact root, session ledger, activity log, execution queue",
    "computa-speak": "user-task.md, normalized-task.md, prompt-normalization-log.md",
    "computa-execution-queue": "root and session-local queue rows expanded",
    "computa-export-control-execute": "4D campaign invocations and campaign closeout",
    "computa-4d-chess-execute": "Super-Phase invocations and 4D closeout",
    "computa-make-no-mistakes": "nested Computa session, phases/tasks/subtasks, TDD/QA, reviews, closeout",
    "security-audit": "Export Control final security closeout evidence and report",
}
COMMAND_PAYLOAD_KEYS = {
    "command",
    "cmd",
    "shell_command",
    "bash_command",
    "script",
}
COMMAND_CONTAINER_KEYS = {
    "tool_input",
    "toolInput",
    "parameters",
    "params",
    "args",
    "arguments",
    "input",
}
UNSAFE_SHELL_EVENTS = {"PreToolUse", "PermissionRequest", "BeforeShellExecution"}
UNSAFE_GIT_ADD_PATTERNS = [
    re.compile(r"(^|[;&|]\s*)git\s+add\s+(?:--\s+)?\.(?:\s|$)"),
    re.compile(r"(^|[;&|]\s*)git\s+add\s+(?:--\s+)?:\/?(?:\s|$)"),
    re.compile(r"(^|[;&|]\s*)git\s+add\s+(?:-[^\s]*A[^\s]*|--all)(?:\s|$)"),
    re.compile(r"(^|[;&|]\s*)git\s+add\s+(?:-[^\s]*A[^\s]*|--all)\s+\.(?:\s|$)"),
    re.compile(r"(^|[;&|]\s*)git\s+add\s+(?:-[^\s]*u[^\s]*|--update)(?:\s|$)"),
]


@dataclass
class CheckResult:
    ok: bool
    messages: list[str]
    root: Path
    artifact_root: Path | None
    next_item: dict[str, str] | None
    routing_messages: list[str]


@dataclass
class ExpandResult:
    changed: bool
    messages: list[str]
    root: Path
    artifact_root: Path | None
    added_rows: list[dict[str, str]]


def read_stdin_json() -> dict[str, Any]:
    try:
        text = sys.stdin.read()
    except Exception:
        return {}
    if not text.strip():
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def iter_hook_command_strings(value: Any, depth: int = 0) -> list[str]:
    """Extract likely shell commands from hook payloads without scanning prose."""
    if depth > 8:
        return []
    commands: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = str(key)
            if normalized in COMMAND_PAYLOAD_KEYS and isinstance(nested, str):
                commands.append(nested)
            elif normalized in COMMAND_CONTAINER_KEYS:
                commands.extend(iter_hook_command_strings(nested, depth + 1))
        return commands
    if isinstance(value, list):
        for item in value:
            commands.extend(iter_hook_command_strings(item, depth + 1))
    return commands


def unsafe_git_add_reason(command: str) -> str | None:
    compact = " ".join(command.strip().split())
    if not compact:
        return None
    for pattern in UNSAFE_GIT_ADD_PATTERNS:
        if pattern.search(compact):
            return (
                "Broad git staging is blocked by Computa. Stage intentional files explicitly; "
                "do not use `git add .`, `git add -A`, `git add --all`, `git add -u`, or `git add :/`."
            )
    return None


def unsafe_shell_policy_messages(event: str, payload: dict[str, Any]) -> list[str]:
    if event not in UNSAFE_SHELL_EVENTS:
        return []
    messages: list[str] = []
    for command in iter_hook_command_strings(payload):
        reason = unsafe_git_add_reason(command)
        if reason:
            messages.append(reason)
    return messages


def git_root(start: Path) -> Path | None:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None
    return Path(out) if out else None


def detect_root(args_root: str | None, payload: dict[str, Any]) -> Path:
    candidates = [
        args_root,
        os.environ.get("COMPUTA_ROOT"),
        payload.get("cwd"),
        payload.get("working_dir"),
        payload.get("workspace"),
        os.getcwd(),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(str(candidate)).expanduser().resolve()
        if path.exists():
            root = git_root(path)
            return root or path
    return Path.cwd().resolve()


def find_artifact_root(root: Path) -> Path | None:
    current = root
    for path in [current, *current.parents]:
        artifact = path / "docs" / "computa-artifacts"
        if artifact.exists():
            return artifact
    return root / "docs" / "computa-artifacts"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return [{k: (v or "") for k, v in row.items()} for row in reader]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in header})


def append_csv_row(path: Path, header: list[str], row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in header})


def queue_rows(artifact_root: Path) -> tuple[list[dict[str, str]], list[str]]:
    messages: list[str] = []
    queue_path = artifact_root / "execution-queue.csv"
    if not queue_path.exists():
        return [], [f"Missing root execution queue: {queue_path}"]
    with queue_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        if header != QUEUE_HEADER:
            messages.append(
                "Invalid execution-queue.csv header. Expected exact Computa queue header."
            )
        rows = [{k: (v or "") for k, v in row.items()} for row in reader]
    return rows, messages


def write_queue_rows(artifact_root: Path, rows: list[dict[str, str]]) -> None:
    write_csv(artifact_root / "execution-queue.csv", QUEUE_HEADER, rows)


def has_computa_sessions(artifact_root: Path) -> bool:
    if not artifact_root.exists():
        return False
    session_ledger = artifact_root / "session-ledger.csv"
    if session_ledger.exists() and len(read_csv(session_ledger)) > 0:
        return True
    for child in ["export-control", "4d-chess", "computa"]:
        path = artifact_root / child
        if path.exists() and any(path.iterdir()):
            return True
    return False


def parse_dependencies(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.replace(";", ",").split(",") if part.strip()]


def priority_value(row: dict[str, str]) -> tuple[int, str]:
    try:
        priority = int(row.get("priority", "999") or "999")
    except ValueError:
        priority = 999
    return priority, row.get("queue_id", "")


def normalize_skill(value: str) -> str:
    return value.strip().lstrip("/")


def is_done_status(value: str) -> bool:
    return value.strip().lower() in DONE_STATUSES


def is_ready_status(value: str) -> bool:
    return value.strip().lower() in {"ready", "queued"}


def row_status(row: dict[str, str]) -> str:
    return row.get("status", "").strip().lower()


def row_is_terminal(row: dict[str, str]) -> bool:
    return row_status(row) in DONE_STATUSES


def row_has_rationale(row: dict[str, str]) -> bool:
    return bool(
        row.get("notes", "").strip()
        or row.get("evidence_path", "").strip()
        or row.get("next_action", "").strip()
    )


def next_queue_id(rows: list[dict[str, str]]) -> str:
    used = {row.get("queue_id", "") for row in rows}
    index = 1
    while True:
        candidate = f"QH-{index:04d}"
        if candidate not in used:
            return candidate
        index += 1


def parse_priority(value: str, fallback: int = 5000) -> int:
    try:
        return int(value or str(fallback))
    except ValueError:
        return fallback


def queue_row(
    *,
    queue_id: str,
    parent_queue_id: str = "",
    session_id: str = "",
    layer: str = "",
    scope_type: str = "skill",
    scope_id: str = "",
    scope_name: str = "",
    skill: str = "",
    action: str = "invoke_skill",
    priority: int = 5000,
    status: str = "queued",
    dependencies: str = "",
    artifact_path: str = "",
    required_outputs: str = "",
    next_action: str = "",
    notes: str = "",
) -> dict[str, str]:
    row = {key: "" for key in QUEUE_HEADER}
    row.update(
        {
            "queue_id": queue_id,
            "parent_queue_id": parent_queue_id,
            "session_id": session_id,
            "layer": layer,
            "scope_type": scope_type,
            "scope_id": scope_id,
            "scope_name": scope_name or scope_id or skill,
            "skill": skill,
            "action": action,
            "priority": str(priority),
            "status": status,
            "dependencies": dependencies,
            "allowed_parallelism": "coordinator_only",
            "required_outputs": required_outputs,
            "review_gate": "none",
            "artifact_path": artifact_path,
            "next_action": next_action or (f"invoke /{skill}" if skill else action),
            "created_at": utc_now(),
            "notes": notes,
        }
    )
    return row


def first_ready_item(rows: list[dict[str, str]]) -> dict[str, str] | None:
    by_id = {row.get("queue_id", ""): row for row in rows}
    ready: list[dict[str, str]] = []
    for row in rows:
        if row.get("status") not in {"ready", "queued"}:
            continue
        deps = parse_dependencies(row.get("dependencies", ""))
        if all(by_id.get(dep, {}).get("status") in {"complete", "deferred"} for dep in deps):
            ready.append(row)
    if not ready:
        return None
    return sorted(ready, key=priority_value)[0]


def child_skill_row(
    rows: list[dict[str, str]],
    parent: dict[str, str],
    skill: str,
) -> dict[str, str] | None:
    parent_id = parent.get("queue_id", "")
    session_id = parent.get("session_id", "")
    for row in rows:
        if normalize_skill(row.get("skill", "")) != skill:
            continue
        if row_status(row) == "superseded":
            continue
        if parent_id and row.get("parent_queue_id") == parent_id:
            return row
        if session_id and row.get("session_id") == session_id and not row.get("parent_queue_id"):
            return row
    return None


def child_skill_rows(
    rows: list[dict[str, str]],
    parent: dict[str, str],
    skill: str,
) -> list[dict[str, str]]:
    expected = normalize_skill(skill)
    parent_id = parent.get("queue_id", "")
    session_id = parent.get("session_id", "")
    matches: list[dict[str, str]] = []
    for row in rows:
        if normalize_skill(row.get("skill", "")) != expected:
            continue
        if row_status(row) == "superseded":
            continue
        if parent_id and row.get("parent_queue_id") == parent_id:
            matches.append(row)
            continue
        if (
            session_id
            and row.get("session_id") == session_id
            and row.get("scope_type", "").strip().lower() in {"child-skill", "recursive-skill"}
        ):
            matches.append(row)
    return matches


def queue_has_skill(rows: list[dict[str, str]], skill: str) -> bool:
    expected = normalize_skill(skill)
    return any(
        normalize_skill(row.get("skill", "")) == expected
        and row.get("status", "").strip().lower() != "superseded"
        for row in rows
    )


def dependencies_done(rows: list[dict[str, str]], dependencies: str) -> bool:
    if not dependencies:
        return True
    by_id = {row.get("queue_id", ""): row for row in rows}
    return all(by_id.get(dep, {}).get("status") in {"complete", "deferred"} for dep in parse_dependencies(dependencies))


def terminal_rationale_messages(rows: list[dict[str, str]]) -> list[str]:
    messages: list[str] = []
    for row in rows:
        status = row_status(row)
        if status in {"deferred", "blocked", "superseded"} and not row_has_rationale(row):
            messages.append(
                f"Queue row {row.get('queue_id')} is {status} without notes, evidence_path, or next_action rationale."
            )
    return messages


def parent_completion_messages(rows: list[dict[str, str]]) -> list[str]:
    messages: list[str] = []
    for parent in rows:
        parent_skill = normalize_skill(parent.get("skill", ""))
        if parent_skill not in REQUIRED_CHILD_SKILLS:
            continue
        if row_status(parent) != "complete":
            continue
        missing: list[str] = []
        non_terminal: list[str] = []
        weak_terminal: list[str] = []
        for skill in REQUIRED_CHILD_SKILLS[parent_skill]:
            matches = child_skill_rows(rows, parent, skill)
            if not matches:
                missing.append(skill)
                continue
            if not any(row_is_terminal(row) for row in matches):
                non_terminal.extend(
                    f"{row.get('queue_id')}:{row.get('status') or 'missing-status'}"
                    for row in matches
                )
                continue
            for row in matches:
                if row_status(row) in {"deferred", "blocked", "superseded"} and not row_has_rationale(row):
                    weak_terminal.append(f"{row.get('queue_id')}:{row_status(row)}")
        if missing:
            messages.append(
                f"Completed /{parent_skill} row {parent.get('queue_id')} is missing required child rows: "
                + ", ".join(f"/{skill}" for skill in missing[:12])
                + ("" if len(missing) <= 12 else f", +{len(missing) - 12} more")
            )
        if non_terminal:
            messages.append(
                f"Completed /{parent_skill} row {parent.get('queue_id')} has non-terminal child rows: "
                + ", ".join(non_terminal[:20])
            )
        if weak_terminal:
            messages.append(
                f"Completed /{parent_skill} row {parent.get('queue_id')} has deferred/blocked/superseded children without rationale: "
                + ", ".join(weak_terminal[:20])
            )
    return messages


def resolve_artifact_path(root: Path, artifact_root: Path, value: str) -> Path | None:
    raw = value.strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    candidates: list[Path]
    if path.is_absolute():
        candidates = [path]
    else:
        candidates = [
            root / path,
            artifact_root / path,
            artifact_root.parent.parent / path if artifact_root.parent.parent.exists() else root / path,
        ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0] if candidates else None


def row_artifact_messages(root: Path, artifact_root: Path, rows: list[dict[str, str]], closeout: bool) -> list[str]:
    messages: list[str] = []
    for row in rows:
        if row_status(row) != "complete" and not closeout:
            continue
        for field in ["artifact_path", "evidence_path"]:
            value = row.get(field, "").strip()
            if not value:
                continue
            candidate = resolve_artifact_path(root, artifact_root, value)
            if candidate and not candidate.exists():
                messages.append(
                    f"Queue row {row.get('queue_id')} is {row_status(row) or 'unknown'} but {field} does not exist: {value}"
                )
    return messages


def require_file(path: Path, rel: str, messages: list[str], label: str) -> None:
    if not (path / rel).exists():
        messages.append(f"{label} missing required artifact: {path / rel}")


def cmn_shape_messages(path: Path, label: str) -> list[str]:
    messages: list[str] = []
    if not path.exists() or not path.is_dir():
        messages.append(f"{label} artifact directory is missing: {path}")
        return messages
    require_file(path, "user-task.md", messages, label)
    if not ((path / "normalized-task.md").exists() or (path / "plan.md").exists()):
        messages.append(f"{label} missing normalized-task.md or plan.md: {path}")
    phases = path / "phases"
    if not phases.exists():
        messages.append(f"{label} missing phases/ directory: {phases}")
        return messages
    phase_dirs = sorted(child for child in phases.iterdir() if child.is_dir())
    if not phase_dirs:
        messages.append(f"{label} has phases/ but no phase directories: {phases}")
        return messages
    for phase in phase_dirs:
        require_file(phase, "phase.md", messages, f"{label} phase {phase.name}")
        if not ((phase / "phase-ledger.csv").exists() or (phase / "phase-task-ledger.csv").exists()):
            messages.append(f"{label} phase {phase.name} missing phase-ledger.csv or phase-task-ledger.csv")
        tasks = phase / "tasks"
        if not tasks.exists():
            messages.append(f"{label} phase {phase.name} missing tasks/ directory")
            continue
        task_dirs = sorted(child for child in tasks.iterdir() if child.is_dir())
        if not task_dirs:
            messages.append(f"{label} phase {phase.name} has no task directories")
        for task in task_dirs:
            require_file(task, "task.md", messages, f"{label} task {task.name}")
            require_file(task, "task-ledger.csv", messages, f"{label} task {task.name}")
            if not ((task / "subtasks.csv").exists() or (task / "subtask-ledger.csv").exists()):
                messages.append(f"{label} task {task.name} missing subtasks.csv or subtask-ledger.csv")
    return messages


def chess_shape_messages(path: Path, label: str) -> list[str]:
    messages: list[str] = []
    if not path.exists() or not path.is_dir():
        messages.append(f"{label} artifact directory is missing: {path}")
        return messages
    require_file(path, "user-task.md", messages, label)
    super_phases = path / "super-phases"
    if not super_phases.exists():
        messages.append(f"{label} missing super-phases/ directory: {super_phases}")
        return messages
    sp_dirs = sorted(child for child in super_phases.iterdir() if child.is_dir())
    if not sp_dirs:
        messages.append(f"{label} has super-phases/ but no Super-Phase directories")
    for sp_dir in sp_dirs:
        if not ((sp_dir / "super-phase.md").exists() or (sp_dir / "plan.md").exists()):
            messages.append(f"{label} Super-Phase {sp_dir.name} missing super-phase.md or plan.md")
        if not ((sp_dir / "super-phase-ledger.csv").exists() or (sp_dir / "phase-ledger.csv").exists()):
            messages.append(f"{label} Super-Phase {sp_dir.name} missing super-phase-ledger.csv or phase-ledger.csv")
        if not (
            (sp_dir / "computa-invocation.md").exists()
            or (sp_dir / "computa").exists()
            or any(sp_dir.glob("**/CMN-*"))
        ):
            messages.append(f"{label} Super-Phase {sp_dir.name} missing computa invocation or nested CMN artifact")
    return messages


def export_control_shape_messages(path: Path, label: str) -> list[str]:
    messages: list[str] = []
    if not path.exists() or not path.is_dir():
        messages.append(f"{label} artifact directory is missing: {path}")
        return messages
    for rel in ["user-task.md", "normalized-task.md", "execution-queue.csv"]:
        require_file(path, rel, messages, label)
    if not ((path / "campaigns").exists() or (path / "reports").exists()):
        messages.append(f"{label} missing campaigns/ or reports/ directory: {path}")
    return messages


def session_shape_messages(root: Path, artifact_root: Path, rows: list[dict[str, str]], closeout: bool) -> list[str]:
    messages: list[str] = []
    session_ledger = artifact_root / "session-ledger.csv"
    if session_ledger.exists():
        for session in read_csv(session_ledger):
            status = session.get("status", "").strip().lower()
            if status in SESSION_TERMINAL_STATUSES and not closeout:
                continue
            session_path = session.get("session_path", "").strip()
            if session_path:
                resolved = resolve_artifact_path(root, artifact_root, session_path)
                if resolved and not resolved.exists():
                    messages.append(f"Session {session.get('session_id')} path missing: {session_path}")

    for row in rows:
        if row_status(row) != "complete" and not closeout:
            continue
        skill = normalize_skill(row.get("skill", ""))
        artifact = row.get("artifact_path", "").strip()
        if not artifact:
            continue
        resolved = resolve_artifact_path(root, artifact_root, artifact)
        if not resolved or not resolved.exists():
            continue
        label = f"Queue row {row.get('queue_id')} /{skill}"
        if skill == "computa-make-no-mistakes":
            messages.extend(cmn_shape_messages(resolved, label))
        elif skill == "computa-4d-chess":
            messages.extend(chess_shape_messages(resolved, label))
        elif skill == "computa-export-control":
            messages.extend(export_control_shape_messages(resolved, label))
    return messages


def active_parent_skills(rows: list[dict[str, str]], artifact_root: Path) -> tuple[set[str], list[str]]:
    parents: set[str] = set()
    routing: list[str] = []

    for row in rows:
        skill = normalize_skill(row.get("skill", ""))
        if skill in REQUIRED_CHILD_SKILLS and row.get("status", "").strip().lower() not in ROUTING_EXEMPT_STATUSES:
            parents.add(skill)

    session_ledger = artifact_root / "session-ledger.csv"
    for session in read_csv(session_ledger):
        status = session.get("status", "").strip().lower()
        if status in SESSION_TERMINAL_STATUSES:
            continue
        skill = LAYER_SKILL.get(session.get("layer", "").strip().lower())
        if not skill:
            continue
        parents.add(skill)
        if not queue_has_skill(rows, skill):
            routing.append(
                f"Active {session.get('layer')} session {session.get('session_id')} has no root queue row for /{skill}."
            )

    return parents, routing


def active_parent_rows(rows: list[dict[str, str]], artifact_root: Path) -> tuple[list[dict[str, str]], list[str]]:
    parents: list[dict[str, str]] = []
    messages: list[str] = []
    seen: set[str] = set()

    for row in rows:
        skill = normalize_skill(row.get("skill", ""))
        if skill not in REQUIRED_CHILD_SKILLS:
            continue
        if row_status(row) in ROUTING_EXEMPT_STATUSES:
            continue
        parents.append(row)
        seen.add(row.get("queue_id", ""))

    session_ledger = artifact_root / "session-ledger.csv"
    for session in read_csv(session_ledger):
        status = session.get("status", "").strip().lower()
        if status in SESSION_TERMINAL_STATUSES:
            continue
        skill = LAYER_SKILL.get(session.get("layer", "").strip().lower())
        if not skill:
            continue

        existing = next(
            (
                row
                for row in rows
                if normalize_skill(row.get("skill", "")) == skill
                and row.get("session_id") == session.get("session_id", "")
                and row_status(row) != "superseded"
            ),
            None,
        )
        if existing:
            if existing.get("queue_id", "") not in seen:
                parents.append(existing)
                seen.add(existing.get("queue_id", ""))
            continue

        qid = next_queue_id(rows)
        parent = queue_row(
            queue_id=qid,
            session_id=session.get("session_id", ""),
            layer=session.get("layer", ""),
            scope_type="session",
            scope_id=session.get("session_id", ""),
            scope_name=f"{session.get('layer', '')} session {session.get('session_id', '')}",
            skill=skill,
            priority=100,
            status="running",
            artifact_path=session.get("session_path", ""),
            required_outputs="expanded child-skill queue rows and session closeout evidence",
            next_action=f"expand and execute /{skill} child queue",
            notes="auto-added by Computa queue expander hook from session-ledger.csv",
        )
        rows.append(parent)
        parents.append(parent)
        seen.add(qid)
        messages.append(f"Added missing parent row {qid} for /{skill} from session {session.get('session_id', '')}.")

    return parents, messages


def add_child_skill_rows(rows: list[dict[str, str]], parent: dict[str, str]) -> list[str]:
    parent_skill = normalize_skill(parent.get("skill", ""))
    required = REQUIRED_CHILD_SKILLS.get(parent_skill, [])
    if not required:
        return []

    messages: list[str] = []
    previous_id = ""
    parent_priority = parse_priority(parent.get("priority", ""), fallback=500)
    for index, skill in enumerate(required, start=1):
        existing = child_skill_row(rows, parent, skill)
        if existing:
            previous_id = existing.get("queue_id", "") or previous_id
            continue

        dependency = previous_id
        status = "ready" if dependencies_done(rows, dependency) else "queued"
        qid = next_queue_id(rows)
        scope_name = f"{parent_skill} -> {skill}"
        required_outputs = CHILD_REQUIRED_OUTPUTS.get(skill, f"/{skill} required outputs and evidence")
        next_action = f"invoke /{skill} as required child of /{parent_skill}"
        if parent_skill == "computa-export-control" and skill == "computa-make-no-mistakes":
            scope_name = "computa-export-control final security closeout -> computa-make-no-mistakes"
            required_outputs = "Export Control final security closeout through /computa-make-no-mistakes invoking /security-audit, or documented N/A/blocker"
            next_action = "invoke /computa-make-no-mistakes for final Export Control security closeout; inside that task invoke /security-audit once if applicable"
        child = queue_row(
            queue_id=qid,
            parent_queue_id=parent.get("queue_id", ""),
            session_id=parent.get("session_id", ""),
            layer=parent.get("layer") or SKILL_LAYER.get(parent_skill, ""),
            scope_type="child-skill",
            scope_id=skill,
            scope_name=scope_name,
            skill=skill,
            priority=parent_priority + index,
            status=status,
            dependencies=dependency,
            artifact_path=parent.get("artifact_path", ""),
            required_outputs=required_outputs,
            next_action=next_action,
            notes="auto-added by Computa queue expander hook",
        )
        rows.append(child)
        previous_id = qid
        messages.append(f"Added child row {qid}: /{parent_skill} -> /{skill}.")

    return messages


def add_recursive_execution_rows(rows: list[dict[str, str]]) -> list[str]:
    messages: list[str] = []
    for row in list(rows):
        if row_status(row) in ROUTING_EXEMPT_STATUSES:
            continue
        skill = normalize_skill(row.get("skill", ""))
        scope_type = row.get("scope_type", "").lower()
        scope_name = row.get("scope_name", "").lower()
        scope_id = row.get("scope_id", "")

        target = ""
        required_outputs = ""
        next_action = ""
        if ("campaign" in scope_type or "campaign" in scope_name) and skill != "computa-4d-chess":
            target = "computa-4d-chess"
            required_outputs = "4D session, Super-Phase plan, nested Computa execution, reviews, closeout"
            next_action = "invoke /computa-4d-chess with the campaign prompt"
        elif (
            "super-phase" in scope_type
            or "super_phase" in scope_type
            or scope_id.upper().startswith("SP-")
        ) and skill != "computa-make-no-mistakes":
            target = "computa-make-no-mistakes"
            required_outputs = "nested Computa session, phase/task ledgers, tests, reviews, closeout"
            next_action = "invoke /computa-make-no-mistakes with the Super-Phase computa-invocation.md prompt"

        if not target or child_skill_row(rows, row, target):
            continue

        qid = next_queue_id(rows)
        child = queue_row(
            queue_id=qid,
            parent_queue_id=row.get("queue_id", ""),
            session_id=row.get("session_id", ""),
            layer=row.get("layer", ""),
            scope_type="recursive-skill",
            scope_id=target,
            scope_name=f"{row.get('scope_name') or row.get('scope_id') or row.get('queue_id')} -> {target}",
            skill=target,
            priority=parse_priority(row.get("priority", ""), fallback=1000) + 1,
            status="ready" if row_status(row) in {"ready", "running", "complete"} else "queued",
            artifact_path=row.get("artifact_path", ""),
            required_outputs=required_outputs,
            next_action=next_action,
            notes="auto-added by Computa queue expander hook for recursive skill routing",
        )
        rows.append(child)
        messages.append(f"Added recursive row {qid}: {row.get('queue_id')} -> /{target}.")

    return messages


def write_queue_markdown(artifact_root: Path, rows: list[dict[str, str]], messages: list[str]) -> None:
    path = artifact_root / "execution-queue.md"
    next_item = first_ready_item(rows)
    lines = [
        "# Computa Execution Queue",
        "",
        f"Last hook expansion check: {utc_now()}",
        "",
        "## Safe Next Action",
        "",
        next_item_instruction(next_item),
        "",
        "## Recent Hook Expansion",
        "",
    ]
    if messages:
        lines.extend(f"- {message}" for message in messages)
    else:
        lines.append("- No missing deterministic queue rows found.")
    lines.extend(
        [
            "",
            "## Active Rows",
            "",
        ]
    )
    for row in sorted(
        [item for item in rows if row_status(item) in ACTIVE_STATUSES],
        key=priority_value,
    )[:50]:
        lines.append(
            f"- `{row.get('queue_id')}` `{row.get('status')}` `/{normalize_skill(row.get('skill', ''))}`: "
            f"{row.get('scope_name') or row.get('next_action')}"
        )
    path.write_text("\n".join(lines) + "\n")


def append_queue_activity(artifact_root: Path, messages: list[str]) -> None:
    if not messages:
        return
    append_csv_row(
        artifact_root / "activity-log.csv",
        ACTIVITY_HEADER,
        {
            "timestamp": utc_now(),
            "event_type": "queue_expanded",
            "scope_type": "execution-queue",
            "scope_id": "hook-expander",
            "scope_name": "Computa queue expander hook",
            "status": "complete",
            "artifact_path": str(artifact_root / "execution-queue.csv"),
            "next_action": "consume the highest-priority ready queue item",
            "notes": " | ".join(messages[:10]),
        },
    )


def expand_queue(root: Path) -> ExpandResult:
    artifact_root = find_artifact_root(root)
    if artifact_root is None or not artifact_root.exists():
        return ExpandResult(False, ["No Computa artifact root found; nothing to expand."], root, artifact_root, [])
    if not has_computa_sessions(artifact_root):
        return ExpandResult(False, ["No Computa sessions found; nothing to expand."], root, artifact_root, [])

    rows, queue_messages = queue_rows(artifact_root)
    if queue_messages and not rows:
        return ExpandResult(False, queue_messages, root, artifact_root, [])

    before_ids = {row.get("queue_id", "") for row in rows}
    messages: list[str] = []
    for _ in range(4):
        pass_messages: list[str] = []
        parents, parent_messages = active_parent_rows(rows, artifact_root)
        pass_messages.extend(parent_messages)
        for parent in parents:
            pass_messages.extend(add_child_skill_rows(rows, parent))
        pass_messages.extend(add_recursive_execution_rows(rows))
        if not pass_messages:
            break
        messages.extend(pass_messages)

    added_rows = [row for row in rows if row.get("queue_id", "") not in before_ids]
    if not added_rows:
        return ExpandResult(False, ["Execution queue already has deterministic recursive rows."], root, artifact_root, [])

    write_queue_rows(artifact_root, rows)
    write_queue_markdown(artifact_root, rows, messages)
    append_queue_activity(artifact_root, messages)
    return ExpandResult(True, messages, root, artifact_root, added_rows)


def recursive_routing_messages(rows: list[dict[str, str]], artifact_root: Path) -> list[str]:
    if not rows:
        return []

    routing: list[str] = []
    parents, session_messages = active_parent_skills(rows, artifact_root)
    routing.extend(session_messages)

    for parent in sorted(parents):
        missing = [skill for skill in REQUIRED_CHILD_SKILLS[parent] if not queue_has_skill(rows, skill)]
        if missing:
            preview = ", ".join(f"/{skill}" for skill in missing[:10])
            suffix = "" if len(missing) <= 10 else f", +{len(missing) - 10} more"
            routing.append(
                f"/{parent} has not expanded required child-skill queue rows: {preview}{suffix}. "
                "Invoke /computa-execution-queue now; if any child is N/A, add a deferred queue row with rationale."
            )

    export_execute_active = any(
        normalize_skill(row.get("skill", "")) == "computa-export-control-execute"
        and not is_done_status(row.get("status", ""))
        for row in rows
    )
    campaign_rows = [
        row
        for row in rows
        if "campaign" in row.get("scope_type", "").lower()
        or "campaign" in row.get("scope_name", "").lower()
    ]
    if (export_execute_active or campaign_rows) and not queue_has_skill(rows, "computa-4d-chess"):
        routing.append(
            "Export Control execution has campaign work but no /computa-4d-chess queue row. "
            "Campaign execution must invoke /computa-4d-chess through the queue."
        )

    chess_execute_active = any(
        normalize_skill(row.get("skill", "")) == "computa-4d-chess-execute"
        and not is_done_status(row.get("status", ""))
        for row in rows
    )
    super_phase_rows = [
        row
        for row in rows
        if "super-phase" in row.get("scope_type", "").lower()
        or "super_phase" in row.get("scope_type", "").lower()
        or row.get("scope_id", "").upper().startswith("SP-")
    ]
    if (chess_execute_active or super_phase_rows) and not queue_has_skill(rows, "computa-make-no-mistakes"):
        routing.append(
            "4D Chess execution has Super-Phase work but no /computa-make-no-mistakes queue row. "
            "Every Super-Phase must execute through /computa-make-no-mistakes."
        )

    return routing


def next_item_instruction(row: dict[str, str] | None) -> str:
    if not row:
        return "No ready Computa queue item found. Reconcile dependencies, blockers, and activity-log.csv before guessing a next action."

    skill = normalize_skill(row.get("skill", ""))
    queue_id = row.get("queue_id", "")
    label = row.get("scope_name") or row.get("scope_id") or row.get("action") or "unnamed item"
    next_action = row.get("next_action") or row.get("action") or "execute the queued item"
    artifact = row.get("artifact_path", "")
    required = row.get("required_outputs", "")

    if skill:
        instruction = (
            f"Next required queue action: mark {queue_id} running, then invoke /{skill} for {label}. "
            f"Use next_action='{next_action}'."
        )
    else:
        instruction = (
            f"Next required queue action: mark {queue_id} running and execute {label}. "
            f"Use next_action='{next_action}'."
        )
    if artifact:
        instruction += f" Start from artifact_path={artifact}."
    if required:
        instruction += f" Required outputs: {required}."
    instruction += " Do not skip to later queue rows or rely on chat memory."
    return instruction


def validate(root: Path, strict: bool = False, closeout: bool = False) -> CheckResult:
    artifact_root = find_artifact_root(root)
    messages: list[str] = []
    next_item: dict[str, str] | None = None

    if artifact_root is None or not artifact_root.exists():
        return CheckResult(True, ["No Computa artifact root found."], root, artifact_root, None, [])

    if not has_computa_sessions(artifact_root):
        return CheckResult(
            True,
            ["Computa artifact root exists but no sessions found."],
            root,
            artifact_root,
            None,
            [],
        )

    rows, queue_messages = queue_rows(artifact_root)
    messages.extend(queue_messages)

    if not rows:
        messages.append("Computa sessions exist but execution queue has no rows.")
    else:
        ids = [row.get("queue_id", "") for row in rows]
        missing_ids = [idx for idx, value in enumerate(ids, start=2) if not value]
        if missing_ids:
            messages.append(f"Queue rows missing queue_id at CSV line(s): {missing_ids[:10]}")
        duplicate_ids = sorted({qid for qid in ids if qid and ids.count(qid) > 1})
        if duplicate_ids:
            messages.append(f"Duplicate queue_id values: {', '.join(duplicate_ids[:20])}")
        invalid_status = sorted(
            {
                row.get("status", "")
                for row in rows
                if row.get("status", "") not in VALID_STATUSES
            }
        )
        if invalid_status:
            messages.append(f"Invalid queue status values: {', '.join(invalid_status)}")
        by_id = {row.get("queue_id", ""): row for row in rows}
        missing_deps: list[str] = []
        for row in rows:
            for dep in parse_dependencies(row.get("dependencies", "")):
                if dep not in by_id:
                    missing_deps.append(f"{row.get('queue_id')} -> {dep}")
        if missing_deps:
            messages.append(f"Missing dependency queue IDs: {', '.join(missing_deps[:20])}")
        active = [row for row in rows if row.get("status") in BLOCKING_CLOSEOUT_STATUSES]
        if closeout and active:
            labels = [
                f"{row.get('queue_id')}:{row.get('status')}:{row.get('skill') or row.get('scope_name')}"
                for row in active[:20]
            ]
            messages.append("Closeout blocked; active queue rows remain: " + "; ".join(labels))
        next_item = first_ready_item(rows)
        messages.extend(terminal_rationale_messages(rows))
        messages.extend(parent_completion_messages(rows))
        messages.extend(row_artifact_messages(root, artifact_root, rows, closeout))
        messages.extend(session_shape_messages(root, artifact_root, rows, closeout))

    routing_messages = recursive_routing_messages(rows, artifact_root)
    if closeout and routing_messages:
        messages.extend("Recursive routing blocked: " + message for message in routing_messages)

    ok = len(messages) == 0 or (not strict and not closeout)
    return CheckResult(
        ok,
        messages or ["Computa queue validation passed."],
        root,
        artifact_root,
        next_item,
        routing_messages,
    )


def output_text(result: CheckResult) -> None:
    print(f"root: {result.root}")
    print(f"artifact_root: {result.artifact_root}")
    for message in result.messages:
        print(f"- {message}")
    if result.next_item:
        print("next_item:")
        print(json.dumps(result.next_item, indent=2, sort_keys=True))
    for message in result.routing_messages:
        print(f"routing: {message}")


def hook_json(event: str, ok: bool, reason: str, additional_context: str | None = None) -> dict[str, Any]:
    if event in CONTEXT_EVENTS and additional_context:
        return {
            "hookSpecificOutput": {
                "hookEventName": event,
                "additionalContext": additional_context,
            }
        }
    if event in {"Stop", "SubagentStop"}:
        if ok:
            return {"continue": True, "systemMessage": reason}
        return {"continue": False, "stopReason": reason, "systemMessage": reason}
    if event == "PreToolUse" and not ok:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    return {"systemMessage": reason}


def output_hook_result(
    hook_format: str,
    event: str,
    ok: bool,
    reason: str,
    additional_context: str | None = None,
) -> int:
    if hook_format in TEXT_HOOK_FORMATS:
        if ok:
            print(additional_context or reason)
        else:
            print(reason, file=sys.stderr)
        return 0 if ok else 2

    if hook_format == "auto":
        hook_format = "json"

    if hook_format in JSON_HOOK_FORMATS:
        print(json.dumps(hook_json(event, ok, reason, additional_context=additional_context)))
        return 0 if ok else 2

    print(json.dumps(hook_json(event, ok, reason, additional_context=additional_context)))
    return 0 if ok else 2


def run_hook(args: argparse.Namespace) -> int:
    payload = read_stdin_json()
    event = args.event or str(payload.get("event") or payload.get("hook_event_name") or "")
    if not event:
        event = "Stop" if args.closeout else "SessionStart"

    root = detect_root(args.root, payload)
    policy_messages = unsafe_shell_policy_messages(event, payload)
    if policy_messages:
        context = "Computa hook blocked unsafe command. " + " ".join(policy_messages)
        return output_hook_result(args.format, event, False, context, additional_context=context)

    expand_messages: list[str] = []
    if args.expand_queue or event in EXPAND_EVENTS:
        expand_result = expand_queue(root)
        if expand_result.changed:
            expand_messages = expand_result.messages

    closeout = args.closeout or event in {"Stop", "SessionEnd"}
    result = validate(root, strict=args.strict, closeout=closeout)

    if args.quiet_ok and result.ok:
        return 0

    routing_text = ""
    if result.routing_messages:
        routing_text = "\nRecursive routing required: " + " ".join(result.routing_messages[:5])
    expand_text = ""
    if expand_messages:
        expand_text = "\nQueue expander added rows: " + " ".join(expand_messages[:5])
    next_text = "\n" + next_item_instruction(result.next_item)
    context = (
        "Computa hook check: "
        + ("passed." if result.ok else "blocked.")
        + " "
        + " ".join(result.messages[:5])
        + expand_text
        + routing_text
        + next_text
    )
    return output_hook_result(args.format, event, result.ok, context, additional_context=context)


def output_expand_result(result: ExpandResult, as_json: bool) -> None:
    if as_json:
        print(
            json.dumps(
                {
                    "changed": result.changed,
                    "root": str(result.root),
                    "artifact_root": str(result.artifact_root) if result.artifact_root else None,
                    "messages": result.messages,
                    "added_rows": result.added_rows,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    print(f"root: {result.root}")
    print(f"artifact_root: {result.artifact_root}")
    print(f"changed: {result.changed}")
    for message in result.messages:
        print(f"- {message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Computa portable hook runner")
    parser.add_argument("command", choices=["validate", "next", "hook", "expand"])
    parser.add_argument("--root", default=None, help="Project root. Defaults to cwd/git root/hook payload cwd.")
    parser.add_argument("--event", default=None, help="Hook event name.")
    parser.add_argument(
        "--format",
        default="json",
        choices=sorted(TEXT_HOOK_FORMATS | JSON_HOOK_FORMATS | {"auto"}),
        help="Hook output protocol for the invoking harness.",
    )
    parser.add_argument("--strict", action="store_true", help="Fail if queue is missing or malformed.")
    parser.add_argument("--closeout", action="store_true", help="Fail if active queue rows remain.")
    parser.add_argument("--expand-queue", action="store_true", help="Expand deterministic missing queue rows before validating.")
    parser.add_argument("--quiet-ok", action="store_true", help="Emit no output when the hook passes.")
    parser.add_argument("--json", action="store_true", help="Print JSON for validate/next.")
    args = parser.parse_args()

    if args.command == "hook":
        return run_hook(args)

    root = detect_root(args.root, {})

    if args.command == "expand":
        result = expand_queue(root)
        output_expand_result(result, args.json)
        return 0

    if args.expand_queue:
        expand_queue(root)

    result = validate(root, strict=args.strict, closeout=args.closeout)
    if args.command == "next":
        if args.json:
            print(json.dumps(result.next_item or {}, indent=2, sort_keys=True))
        elif result.next_item:
            print(json.dumps(result.next_item, indent=2, sort_keys=True))
        else:
            print("No ready Computa queue item found.")
        return 0 if result.next_item else 1

    if args.json:
        print(
            json.dumps(
                {
                    "ok": result.ok,
                    "root": str(result.root),
                    "artifact_root": str(result.artifact_root) if result.artifact_root else None,
                    "messages": result.messages,
                    "routing_messages": result.routing_messages,
                    "next_item": result.next_item,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        output_text(result)
    return 0 if result.ok else 2


if __name__ == "__main__":
    sys.exit(main())
