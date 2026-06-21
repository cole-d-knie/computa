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
import subprocess
import sys
from dataclasses import dataclass
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
LAYER_SKILL = {
    "export-control": "computa-export-control",
    "export_control": "computa-export-control",
    "4d-chess": "computa-4d-chess",
    "4d_chess": "computa-4d-chess",
    "computa": "computa-make-no-mistakes",
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
    ],
    "computa-4d-chess": [
        "computa-init",
        "computa-speak",
        "computa-execution-queue",
        "computa-4d-chess-architect",
        "computa-4d-chess-build",
        "computa-4d-chess-execute",
        "security-audit",
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


@dataclass
class CheckResult:
    ok: bool
    messages: list[str]
    root: Path
    artifact_root: Path | None
    next_item: dict[str, str] | None
    routing_messages: list[str]


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


def queue_has_skill(rows: list[dict[str, str]], skill: str) -> bool:
    expected = normalize_skill(skill)
    return any(
        normalize_skill(row.get("skill", "")) == expected
        and row.get("status", "").strip().lower() != "superseded"
        for row in rows
    )


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
            "Every Super-Phase must execute through /computa-make-no-mistakes, including SP-999."
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
    closeout = args.closeout or event in {"Stop", "SessionEnd"}
    result = validate(root, strict=args.strict, closeout=closeout)

    if args.quiet_ok and result.ok:
        return 0

    routing_text = ""
    if result.routing_messages:
        routing_text = "\nRecursive routing required: " + " ".join(result.routing_messages[:5])
    next_text = "\n" + next_item_instruction(result.next_item)
    context = (
        "Computa hook check: "
        + ("passed." if result.ok else "blocked.")
        + " "
        + " ".join(result.messages[:5])
        + routing_text
        + next_text
    )
    return output_hook_result(args.format, event, result.ok, context, additional_context=context)


def main() -> int:
    parser = argparse.ArgumentParser(description="Computa portable hook runner")
    parser.add_argument("command", choices=["validate", "next", "hook"])
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
    parser.add_argument("--quiet-ok", action="store_true", help="Emit no output when the hook passes.")
    parser.add_argument("--json", action="store_true", help="Print JSON for validate/next.")
    args = parser.parse_args()

    if args.command == "hook":
        return run_hook(args)

    root = detect_root(args.root, {})

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
