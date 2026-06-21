#!/usr/bin/env python3
"""Audit the Computa skill package for cross-harness consistency.

The package intentionally supports several harnesses, which means stale copies
are the main failure mode. Keep this dependency-free so CI, installers, and
local agents can run it before trusting the package.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
CLAUDE_SKILLS_DIR = ROOT / "harnesses" / "claude-code" / "plugin" / "skills"
KIMI_SKILLS_DIR = ROOT / "harnesses" / "kimi" / "skills"

TEXT_SUFFIXES = {
    ".md",
    ".mdc",
    ".py",
    ".js",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".sh",
    ".txt",
}

KIMI_SWARM_DIFF_SKILLS = {
    "computa-swarm-verify",
    "computa-swarm-verify-closeout",
    "computa-swarm-verify-investigate",
    "computa-swarm-verify-setup",
    "computa-swarm-verify-swarms",
    "computa-swarm-verify-tdd-qa",
}

KIMI_SWARM_REPLACEMENTS = [
    (
        "- native agent swarm/delegation: safe swarm parallelism.",
        "- `dispatching-parallel-agents` and `subagent-driven-development`: safe swarm parallelism.",
    ),
    (
        "Use native agent swarm/delegation and `requesting-code-review` when available.",
        "Use `dispatching-parallel-agents`, `subagent-driven-development`, and `requesting-code-review` when available.",
    ),
]

TOP_LEVEL_CONTRACT_SKILLS = {
    "computa-export-control",
    "computa-4d-chess",
    "computa-make-no-mistakes",
    "computa-execution-queue",
    "computa-resume",
}

FORBIDDEN_TEXT = {
    "Every 4D Chess plan must include " + "final": "full security audit moved to Export Control final closeout",
    "For 4D Chess closeout, execute " + "final": "4D closeout now creates security/privacy checkpoints",
    "SP-999-post-run-" + "security-audit": "SP-999 is no longer a mandatory 4D closeout rule",
    "4D security " + "audits": "4D uses checkpoints; Export Control owns the final security closeout",
}


@dataclass
class Audit:
    failures: list[str]
    checks: list[str]

    def ok(self, message: str) -> None:
        self.checks.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def skill_dirs(root: Path) -> dict[str, Path]:
    if not root.exists():
        return {}
    return {
        path.name: path
        for path in sorted(root.iterdir())
        if path.is_dir() and (path / "SKILL.md").exists()
    }


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str] | None:
    text = path.read_text()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        return None

    frontmatter: dict[str, str] = {}
    for raw_line in lines[1:end]:
        if not raw_line.strip() or raw_line.startswith(" "):
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        frontmatter[key.strip()] = value
    body = "\n".join(lines[end + 1 :])
    return frontmatter, body


def iter_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def read_for_compare(path: Path, skill_name: str, target: str) -> str:
    text = path.read_text()
    if (
        target == "kimi"
        and skill_name in KIMI_SWARM_DIFF_SKILLS
        and path.name == "SKILL.md"
    ):
        for adapter_text, base_text in KIMI_SWARM_REPLACEMENTS:
            text = text.replace(adapter_text, base_text)
    return text


def compare_skill_tree(audit: Audit, base: Path, target: Path, skill_name: str, target_name: str) -> None:
    if not target.exists():
        audit.fail(f"{target_name} missing skill copy: {skill_name}")
        return

    base_files = {path.relative_to(base): path for path in iter_files(base)}
    target_files = {path.relative_to(target): path for path in iter_files(target)}

    missing = sorted(set(base_files) - set(target_files))
    extra = sorted(set(target_files) - set(base_files))
    for path in missing:
        audit.fail(f"{target_name} {skill_name} missing file: {path}")
    for path in extra:
        audit.fail(f"{target_name} {skill_name} has extra file: {path}")

    for relative_path in sorted(set(base_files) & set(target_files)):
        base_text = read_for_compare(base_files[relative_path], skill_name, "base")
        target_text = read_for_compare(target_files[relative_path], skill_name, target_name)
        if base_text != target_text:
            audit.fail(f"{target_name} skill drift: {skill_name}/{relative_path}")


def literal_from_install(name: str) -> object:
    tree = ast.parse((ROOT / "scripts" / "install.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise KeyError(name)


def audit_skill_frontmatter(audit: Audit) -> list[str]:
    skills = skill_dirs(SKILLS_DIR)
    seen_names: dict[str, str] = {}
    for skill_name, skill_dir in skills.items():
        skill_path = skill_dir / "SKILL.md"
        parsed = parse_frontmatter(skill_path)
        if parsed is None:
            audit.fail(f"{rel(skill_path)} missing valid YAML frontmatter")
            continue
        frontmatter, body = parsed
        declared = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if declared != skill_name:
            audit.fail(f"{rel(skill_path)} declares name={declared!r}, expected {skill_name!r}")
        if not description:
            audit.fail(f"{rel(skill_path)} missing description")
        elif len(description) < 40:
            audit.fail(f"{rel(skill_path)} description too thin for reliable triggering")
        if declared in seen_names:
            audit.fail(f"duplicate skill name {declared!r}: {seen_names[declared]} and {rel(skill_path)}")
        seen_names[declared] = rel(skill_path)
        if skill_name in TOP_LEVEL_CONTRACT_SKILLS and "templates/computa-execution-contract.md" not in body:
            audit.fail(f"{rel(skill_path)} does not reference the hook-enforced execution contract")
        line_count = len(skill_path.read_text().splitlines())
        if line_count > 500:
            audit.fail(f"{rel(skill_path)} has {line_count} lines; split into references/scripts")
    audit.ok(f"validated {len(skills)} base skill frontmatter blocks")
    return sorted(skills)


def audit_install_skill_list(audit: Audit, base_skills: list[str]) -> None:
    suite = sorted(literal_from_install("SUITE_SKILLS"))
    if suite != base_skills:
        missing = sorted(set(base_skills) - set(suite))
        stale = sorted(set(suite) - set(base_skills))
        if missing:
            audit.fail(f"scripts/install.py SUITE_SKILLS missing: {', '.join(missing)}")
        if stale:
            audit.fail(f"scripts/install.py SUITE_SKILLS stale: {', '.join(stale)}")
    else:
        audit.ok("installer SUITE_SKILLS matches base skills")


def audit_harness_skill_copies(audit: Audit, base_skills: list[str]) -> None:
    kimi_skills = sorted(skill_dirs(KIMI_SKILLS_DIR))
    if kimi_skills != base_skills:
        audit.fail("Kimi skill directory set does not match base skills")

    claude_skills = skill_dirs(CLAUDE_SKILLS_DIR)
    missing_claude = sorted(set(base_skills) - set(claude_skills))
    if missing_claude:
        audit.fail(f"Claude plugin missing base skills: {', '.join(missing_claude)}")

    for skill_name in base_skills:
        base = SKILLS_DIR / skill_name
        compare_skill_tree(audit, base, KIMI_SKILLS_DIR / skill_name, skill_name, "kimi")
        compare_skill_tree(audit, base, CLAUDE_SKILLS_DIR / skill_name, skill_name, "claude")
    audit.ok("validated base skill copies in Kimi and Claude plugin harnesses")


def audit_shared_files(audit: Audit) -> None:
    exact_pairs = [
        (
            ROOT / "scripts" / "computa_hooks.py",
            ROOT / "harnesses" / "goose" / "plugins" / "computa-hooks" / "scripts" / "computa_hooks.py",
            "Goose hook runner copy",
        ),
        (
            ROOT / "templates" / "computa-execution-contract.md",
            ROOT / "harnesses" / "kimi" / "templates" / "computa-execution-contract.md",
            "Kimi execution contract copy",
        ),
        (
            ROOT / "templates" / "computa-execution-contract.md",
            ROOT / "harnesses" / "claude-code" / "plugin" / "templates" / "computa-execution-contract.md",
            "Claude execution contract copy",
        ),
    ]
    for source, target, label in exact_pairs:
        if not target.exists():
            audit.fail(f"{label} missing: {rel(target)}")
        elif source.read_text() != target.read_text():
            audit.fail(f"{label} drift: {rel(source)} != {rel(target)}")
    audit.ok("validated shared hook runner and execution contract copies")


def audit_hook_contract(audit: Audit) -> None:
    hooks_module = ast.parse((ROOT / "scripts" / "computa_hooks.py").read_text())
    required_children = None
    for node in hooks_module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "REQUIRED_CHILD_SKILLS":
                    required_children = ast.literal_eval(node.value)
                    break
    if not isinstance(required_children, dict):
        audit.fail("scripts/computa_hooks.py missing REQUIRED_CHILD_SKILLS")
        return

    expected_parent_skills = {
        "computa-export-control",
        "computa-4d-chess",
        "computa-make-no-mistakes",
    }
    if set(required_children) != expected_parent_skills:
        audit.fail("REQUIRED_CHILD_SKILLS parent set drifted")

    base_skills = set(skill_dirs(SKILLS_DIR))
    for parent, children in required_children.items():
        for child in children:
            if child not in base_skills:
                audit.fail(f"REQUIRED_CHILD_SKILLS[{parent}] references missing skill: {child}")
    audit.ok("validated hook child-skill routing table")


def audit_forbidden_text(audit: Audit) -> None:
    roots = [
        ROOT / "skills",
        ROOT / "harnesses",
        ROOT / "templates",
        ROOT / "hooks",
        ROOT / "scripts",
        ROOT / "README.md",
        ROOT / "DEPENDENCIES.md",
    ]
    for root in roots:
        paths = [root] if root.is_file() else iter_files(root)
        for path in paths:
            if "__pycache__" in path.parts:
                continue
            if path.suffix not in TEXT_SUFFIXES and path.name not in {"README.md", "DEPENDENCIES.md"}:
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            for needle, reason in FORBIDDEN_TEXT.items():
                if needle in text:
                    audit.fail(f"{rel(path)} contains stale phrase {needle!r}: {reason}")
    audit.ok("checked stale security-closeout phrases")


def run_audit() -> Audit:
    audit = Audit(failures=[], checks=[])
    base_skills = audit_skill_frontmatter(audit)
    audit_install_skill_list(audit, base_skills)
    audit_harness_skill_copies(audit, base_skills)
    audit_shared_files(audit)
    audit_hook_contract(audit)
    audit_forbidden_text(audit)
    return audit


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Computa package consistency.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")
    args = parser.parse_args()

    audit = run_audit()
    if args.json:
        print(json.dumps({"ok": not audit.failures, "checks": audit.checks, "failures": audit.failures}, indent=2))
    else:
        for message in audit.checks:
            print(f"OK: {message}")
        for message in audit.failures:
            print(f"FAIL: {message}", file=sys.stderr)
    return 1 if audit.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
