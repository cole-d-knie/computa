import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "computa_hooks.py"
SPEC = importlib.util.spec_from_file_location("computa_hooks", SCRIPT)
hooks = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["computa_hooks"] = hooks
SPEC.loader.exec_module(hooks)


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in header})


def base_project() -> tempfile.TemporaryDirectory:
    temp = tempfile.TemporaryDirectory()
    root = Path(temp.name)
    artifact = root / "docs" / "computa-artifacts"
    artifact.mkdir(parents=True)
    write_csv(
        artifact / "session-ledger.csv",
        [
            "session_id",
            "layer",
            "parent_session_id",
            "status",
            "invocation_root",
            "session_path",
            "user_task_path",
            "started_at",
            "completed_at",
            "task_slug",
            "summary_path",
            "next_action",
        ],
        [
            {
                "session_id": "EC-1",
                "layer": "export-control",
                "status": "active",
                "invocation_root": str(root),
                "session_path": "export-control/EC-1",
            }
        ],
    )
    write_csv(
        artifact / "activity-log.csv",
        hooks.ACTIVITY_HEADER,
        [
            {
                "timestamp": "2026-01-01T00:00:00Z",
                "session_id": "EC-1",
                "layer": "export-control",
                "event_type": "session_started",
                "scope_type": "session",
                "scope_id": "EC-1",
                "scope_name": "Export Control",
                "status": "running",
                "artifact_path": "export-control/EC-1",
            }
        ],
    )
    (artifact / "export-control" / "EC-1").mkdir(parents=True)
    return temp


def queue_row(**overrides: str) -> dict[str, str]:
    row = {key: "" for key in hooks.QUEUE_HEADER}
    row.update(
        {
            "queue_id": "Q1",
            "session_id": "EC-1",
            "layer": "export-control",
            "scope_type": "session",
            "scope_id": "EC-1",
            "scope_name": "Export Control",
            "skill": "computa-export-control",
            "action": "coordinate",
            "priority": "1",
            "status": "complete",
            "required_outputs": "children terminal",
            "created_at": "2026-01-01T00:00:00Z",
        }
    )
    row.update(overrides)
    return row


def run_hook(args: list[str], cwd: Path, payload: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(cwd),
        input=json.dumps(payload or {}),
        text=True,
        capture_output=True,
        check=False,
    )


class ComputaHookTests(unittest.TestCase):
    def test_strict_validate_blocks_completed_parent_without_terminal_children(self) -> None:
        with base_project() as temp:
            root = Path(temp)
            artifact = root / "docs" / "computa-artifacts"
            write_csv(artifact / "execution-queue.csv", hooks.QUEUE_HEADER, [queue_row()])

            result = run_hook(["validate", "--strict", "--json"], root)

            self.assertEqual(result.returncode, 2)
            data = json.loads(result.stdout)
            self.assertFalse(data["ok"])
            self.assertIn("missing required child rows", "\n".join(data["messages"]))

    def test_strict_validate_accepts_completed_parent_with_terminal_children(self) -> None:
        with base_project() as temp:
            root = Path(temp)
            artifact = root / "docs" / "computa-artifacts"
            parent = queue_row()
            rows = [parent]
            for index, skill in enumerate(hooks.REQUIRED_CHILD_SKILLS["computa-export-control"], start=2):
                status = "deferred" if skill == "computa-make-no-mistakes" else "complete"
                rows.append(
                    queue_row(
                        queue_id=f"Q{index}",
                        parent_queue_id="Q1",
                        scope_type="child-skill",
                        scope_id=skill,
                        scope_name=skill,
                        skill=skill,
                        status=status,
                        priority=str(index),
                        notes="not applicable in this test" if status == "deferred" else "",
                    )
                )
            write_csv(artifact / "execution-queue.csv", hooks.QUEUE_HEADER, rows)

            result = run_hook(["validate", "--strict", "--json"], root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(result.stdout)
            self.assertTrue(data["ok"])

    def test_pretooluse_blocks_broad_git_add(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = {"tool_input": {"command": "git add . && git commit -m test"}}

            result = run_hook(["hook", "--event", "PreToolUse", "--format", "json", "--strict"], root, payload)

            self.assertEqual(result.returncode, 2)
            self.assertIn("Broad git staging is blocked", result.stdout)

    def test_pretooluse_blocks_git_add_update(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = {"tool_input": {"command": "git add -u"}}

            result = run_hook(["hook", "--event", "PreToolUse", "--format", "json", "--strict"], root, payload)

            self.assertEqual(result.returncode, 2)
            self.assertIn("Broad git staging is blocked", result.stdout)

    def test_pretooluse_allows_explicit_git_add_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = {"tool_input": {"command": "git add README.md scripts/computa_hooks.py"}}

            result = run_hook(["hook", "--event", "PreToolUse", "--format", "json", "--strict"], root, payload)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_completed_cmn_requires_phase_task_subtask_shape(self) -> None:
        with base_project() as temp:
            root = Path(temp)
            artifact = root / "docs" / "computa-artifacts"
            cmn = artifact / "computa" / "CMN-1"
            cmn.mkdir(parents=True)
            write_csv(
                artifact / "execution-queue.csv",
                hooks.QUEUE_HEADER,
                [
                    queue_row(
                        queue_id="Q1",
                        skill="computa-make-no-mistakes",
                        layer="computa",
                        status="complete",
                        artifact_path="computa/CMN-1",
                    )
                ],
            )

            result = run_hook(["validate", "--strict", "--json"], root)

            self.assertEqual(result.returncode, 2)
            data = json.loads(result.stdout)
            self.assertIn("missing required artifact", "\n".join(data["messages"]))
            self.assertIn("missing phases/ directory", "\n".join(data["messages"]))

    def test_validate_flags_malformed_activity_log_extra_columns(self) -> None:
        with base_project() as temp:
            root = Path(temp)
            artifact = root / "docs" / "computa-artifacts"
            write_csv(artifact / "execution-queue.csv", hooks.QUEUE_HEADER, [queue_row(status="running")])
            with (artifact / "activity-log.csv").open("a") as handle:
                handle.write(
                    "2026-01-01T00:01:00Z,EC-1,export-control,,session_started,session,EC-1,"
                    "Export Control,running,export-control/EC-1,,,,unexpected-extra\n"
                )

            result = run_hook(["validate", "--strict", "--json"], root)

            self.assertEqual(result.returncode, 2)
            data = json.loads(result.stdout)
            self.assertIn("Malformed activity-log.csv row", "\n".join(data["messages"]))

    def test_validate_flags_duplicate_activity_start_with_different_artifact(self) -> None:
        with base_project() as temp:
            root = Path(temp)
            artifact = root / "docs" / "computa-artifacts"
            write_csv(artifact / "execution-queue.csv", hooks.QUEUE_HEADER, [queue_row(status="running")])
            rows = [
                {
                    "timestamp": "2026-01-01T00:00:00Z",
                    "session_id": "4D-1",
                    "layer": "4d-chess",
                    "event_type": "campaign_started",
                    "scope_type": "campaign",
                    "scope_id": "CAM-001",
                    "scope_name": "Foundation",
                    "status": "running",
                    "artifact_path": "4d-chess/4D-1",
                },
                {
                    "timestamp": "2026-01-01T00:01:00Z",
                    "session_id": "4D-2",
                    "layer": "4d-chess",
                    "event_type": "campaign_started",
                    "scope_type": "campaign",
                    "scope_id": "CAM-001",
                    "scope_name": "Foundation",
                    "status": "running",
                    "artifact_path": "4d-chess/4D-2",
                },
            ]
            write_csv(artifact / "activity-log.csv", hooks.ACTIVITY_HEADER, rows)

            result = run_hook(["validate", "--strict", "--json"], root)

            self.assertEqual(result.returncode, 2)
            data = json.loads(result.stdout)
            self.assertIn("Duplicate activity start", "\n".join(data["messages"]))


if __name__ == "__main__":
    unittest.main()
