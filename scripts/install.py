#!/usr/bin/env python3
"""Install the computa-make-no-mistakes suite for multiple coding-agent harnesses."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE_DIR = ROOT / "skills"
KIMI_SUITE_DIR = ROOT / "harnesses" / "kimi" / "skills"
VENDOR_DIR = ROOT / "vendor" / "skills"
CURSOR_RULE = ROOT / "harnesses" / "cursor" / "rules" / "computa-swarm-verify.mdc"
GOOSE_RECIPE = ROOT / "harnesses" / "goose" / "recipes" / "computa-swarm-verify.yaml"
GENERIC_AGENTS = ROOT / "harnesses" / "generic" / "AGENTS.computa-swarm-verify.md"
CODEX_HOOKS = ROOT / "harnesses" / "codex" / "hooks" / "hooks.json"
CLAUDE_HOOKS = ROOT / "harnesses" / "claude-code" / "hooks" / "settings.computa-hooks.json"
GOOSE_HOOK_PLUGIN = ROOT / "harnesses" / "goose" / "plugins" / "computa-hooks"
KIMI_HOOKS_TOML = ROOT / "harnesses" / "kimi" / "hooks" / "config-hooks.toml"
KIMI_HOOKS_DOC = ROOT / "harnesses" / "kimi" / "hooks" / "COMPUTA_HOOKS.md"
OPENCODE_HOOK_PLUGIN = ROOT / "harnesses" / "opencode" / "plugins" / "computa-hooks.js"
OPENCODE_HOOKS_DOC = ROOT / "harnesses" / "opencode" / "hooks" / "COMPUTA_HOOKS.md"
CURSOR_HOOKS = ROOT / "harnesses" / "cursor" / "hooks" / "hooks.json"
CURSOR_HOOKS_DOC = ROOT / "harnesses" / "cursor" / "hooks" / "COMPUTA_HOOKS.md"
GENERIC_HOOKS_DOC = ROOT / "harnesses" / "generic" / "hooks" / "COMPUTA_HOOKS.md"

KIMI_MCP_SERVERS = {
    "context7": {
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp"],
    },
    "playwright": {
        "command": "npx",
        "args": ["-y", "@playwright/mcp@latest"],
    },
}

CURSOR_MCP_SERVERS = {
    "context7": {
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp"],
    },
    "playwright": {
        "command": "npx",
        "args": ["-y", "@playwright/mcp@latest"],
    },
}

OPENCODE_MCP_SERVERS = {
    "context7": {
        "type": "remote",
        "url": "https://mcp.context7.com/mcp",
        "enabled": True,
    },
    "playwright": {
        "type": "local",
        "command": ["npx", "-y", "@playwright/mcp@latest"],
        "enabled": True,
    },
}

SKILL_HARNESSES = {"codex", "claude-code", "kimi", "opencode", "agent-skills"}
PROJECT_HARNESSES = {"cursor", "generic"}
RECIPE_HARNESSES = {"goose"}

SUITE_SKILLS = [
    "computa-init",
    "computa-speak",
    "computa-resume",
    "computa-execution-queue",
    "computa-secrets-needed",
    "computa-docs-architecture",
    "computa-docs-architecture-init",
    "computa-docs-architecture-audit",
    "computa-docs-architecture-update",
    "computa-make-no-mistakes-docs-update",
    "computa-export-control",
    "computa-export-control-design",
    "computa-export-control-execute",
    "computa-export-control-product-requirements",
    "computa-export-control-codebase-audit",
    "computa-export-control-tech-radar",
    "computa-export-control-prior-art",
    "computa-export-control-skill-mcp-intake",
    "computa-export-control-technical-spec",
    "computa-export-control-implementation-strategy",
    "computa-export-control-audit-suite",
    "computa-4d-chess",
    "computa-4d-chess-architect",
    "computa-4d-chess-build",
    "computa-4d-chess-execute",
    "security-audit",
    "performance-audit",
    "ui-audit",
    "computa-md",
    "computa-make-no-mistakes",
    "computa-swarm-verify",
    "computa-swarm-verify-setup",
    "computa-swarm-verify-investigate",
    "computa-swarm-verify-tdd-qa",
    "computa-swarm-verify-swarms",
    "computa-swarm-verify-closeout",
]

LEGACY_SUITE_SKILLS = [
    "swarm-verify",
    "swarm-verify-setup",
    "swarm-verify-investigate",
    "swarm-verify-tdd-qa",
    "swarm-verify-swarms",
    "swarm-verify-closeout",
    "swarm-verify-one-shot",
]

CODEX_DEPS = [
    "caveman",
    "context7",
    "gstack-investigate",
    "playwright",
    "using-superpowers",
    "writing-plans",
    "executing-plans",
    "test-driven-development",
    "systematic-debugging",
    "dispatching-parallel-agents",
    "subagent-driven-development",
    "requesting-code-review",
    "verification-before-completion",
]

CLAUDE_DEPS = [
    "caveman",
    "context7",
    "investigate",
    "playwright",
    "using-superpowers",
    "writing-plans",
    "executing-plans",
    "test-driven-development",
    "systematic-debugging",
    "dispatching-parallel-agents",
    "subagent-driven-development",
    "requesting-code-review",
    "verification-before-completion",
]

KIMI_DEPS = [
    "caveman",
    "context7",
    "investigate",
    "playwright",
    "using-superpowers",
    "writing-plans",
    "executing-plans",
    "test-driven-development",
    "systematic-debugging",
    "dispatching-parallel-agents",
    "requesting-code-review",
    "verification-before-completion",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install computa-make-no-mistakes for Codex, Claude Code, Kimi, OpenCode, Cursor, Goose, and generic AGENTS.md harnesses."
    )
    parser.add_argument(
        "--harness",
        default="codex",
        choices=[
            "all",
            "codex",
            "claude-code",
            "kimi",
            "opencode",
            "cursor",
            "goose",
            "agent-skills",
            "generic",
        ],
        help="Harness to install for. Default: codex.",
    )
    parser.add_argument(
        "--target",
        default="",
        help="Override target directory for a single skill-style harness.",
    )
    parser.add_argument(
        "--project",
        default="",
        help="Project root for project-scoped installs such as Cursor rules or AGENTS files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without changing files.",
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Install only computa-make-no-mistakes suite skills, not dependency skills.",
    )
    parser.add_argument(
        "--force-deps",
        action="store_true",
        help="Overwrite installed dependency skill folders with selected copies.",
    )
    parser.add_argument(
        "--install-local-gstack",
        action="store_true",
        help="Copy a local gstack core skill into the harness target if found. This can be large.",
    )
    parser.add_argument(
        "--gstack-source",
        default="",
        help="Optional local gstack source directory for --install-local-gstack.",
    )
    parser.add_argument(
        "--no-kimi-config",
        action="store_true",
        help="Do not update ~/.kimi-code/config.toml extra_skill_dirs.",
    )
    parser.add_argument(
        "--no-mcp-config",
        action="store_true",
        help="Do not update harness MCP config files for Kimi, OpenCode, or Cursor.",
    )
    parser.add_argument(
        "--install-hooks",
        action="store_true",
        help="Install Computa lifecycle hook configs/templates for the selected harness. Hooks can block closeout when queues are invalid.",
    )
    return parser.parse_args()


def log(message: str) -> None:
    print(message)


def default_target(harness: str) -> Path:
    home = Path.home()
    if harness == "codex":
        return Path(os.environ.get("CODEX_HOME", home / ".codex")) / "skills"
    if harness == "claude-code":
        return home / ".claude" / "skills"
    if harness == "kimi":
        return home / ".kimi-code" / "skills"
    if harness == "opencode":
        return home / ".config" / "opencode" / "skills"
    if harness == "agent-skills":
        return home / ".agents" / "skills"
    raise ValueError(f"no default skill target for {harness}")


def selected_harnesses(name: str) -> list[str]:
    if name == "all":
        return [
            "codex",
            "claude-code",
            "kimi",
            "opencode",
            "agent-skills",
            "cursor",
            "goose",
            "generic",
        ]
    return [name]


def backup_existing(path: Path, dry_run: bool) -> None:
    if not path.exists():
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.bak.{stamp}")
    log(f"backup {path} -> {backup}")
    if not dry_run:
        shutil.move(str(path), str(backup))


def copy_tree(src: Path, dst: Path, dry_run: bool, overwrite: bool) -> bool:
    if not src.exists():
        log(f"missing source: {src}")
        return False
    if dst.exists():
        if not overwrite:
            log(f"present: {dst}")
            return True
        backup_existing(dst, dry_run)
    log(f"install {src} -> {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)
    return True


def copy_file(src: Path, dst: Path, dry_run: bool, overwrite: bool = True) -> bool:
    if not src.exists():
        log(f"missing source: {src}")
        return False
    if dst.exists():
        if not overwrite:
            log(f"present: {dst}")
            return True
        backup_existing(dst, dry_run)
    log(f"install {src} -> {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return True


def skill_source_for_dependency(name: str, harness: str) -> tuple[Path, str]:
    if name == "investigate":
        if harness == "claude-code":
            claude = Path.home() / ".claude" / "skills" / "investigate"
            if claude.exists():
                return claude, "investigate"
        return VENDOR_DIR / "gstack-investigate", "investigate"
    return VENDOR_DIR / name, name


def suite_dir_for(harness: str) -> Path:
    if harness == "kimi":
        return KIMI_SUITE_DIR
    return SUITE_DIR


def dependencies_for(harness: str) -> list[str]:
    if harness == "codex":
        return CODEX_DEPS
    if harness == "kimi":
        return KIMI_DEPS
    if harness in {"claude-code", "opencode", "agent-skills"}:
        return CLAUDE_DEPS
    return []


def install_suite(harness: str, target: Path, dry_run: bool) -> bool:
    ok = True
    source_root = suite_dir_for(harness)
    for name in LEGACY_SUITE_SKILLS:
        legacy = target / name
        if legacy.exists():
            log(f"rename cleanup: backing up legacy skill {legacy}")
            backup_existing(legacy, dry_run)
    for name in SUITE_SKILLS:
        ok = copy_tree(source_root / name, target / name, dry_run, overwrite=True) and ok
    return ok


def candidate_skill_roots(target: Path, harness: str) -> list[Path]:
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    roots = [
        target,
        codex_home / "skills",
        home / ".codex" / "skills",
        home / ".claude" / "skills",
        home / ".config" / "opencode" / "skills",
        home / ".kimi-code" / "skills",
        home / ".agents" / "skills",
    ]
    if harness == "claude-code":
        plugin_root = home / ".claude" / "plugins" / "cache"
        if plugin_root.exists():
            roots.extend(plugin_root.glob("*/*/*/skills"))
    if harness == "codex":
        plugin_root = codex_home / "plugins" / "cache"
        if plugin_root.exists():
            roots.extend(plugin_root.glob("*/*/skills"))
            roots.extend(plugin_root.glob("*/*/*/skills"))
    return list(dict.fromkeys(path.resolve() for path in roots if path.exists()))


def has_gstack_core(target: Path, harness: str) -> bool:
    for root in candidate_skill_roots(target, harness):
        if (root / "gstack" / "bin" / "gstack-update-check").exists():
            return True
    return False


def local_gstack_source(args: argparse.Namespace, harness: str) -> Path | None:
    candidates: list[Path] = []
    if args.gstack_source:
        candidates.append(Path(args.gstack_source).expanduser())
    if harness == "claude-code":
        candidates.append(Path.home() / ".claude" / "skills" / "gstack")
    candidates.extend(
        [
            Path.home() / ".codex" / "skills" / "gstack",
            Path.home() / ".agents" / "skills" / "gstack",
            Path.home() / ".claude" / "skills" / "gstack",
        ]
    )
    for candidate in candidates:
        if (candidate / "bin" / "gstack-update-check").exists():
            return candidate
    return None


def install_dependencies(args: argparse.Namespace, harness: str, target: Path) -> bool:
    ok = True
    for name in dependencies_for(harness):
        src, dst_name = skill_source_for_dependency(name, harness)
        dst = target / dst_name
        overwrite = args.force_deps or not dst.exists()
        ok = copy_tree(src, dst, args.dry_run, overwrite=overwrite) and ok

    if has_gstack_core(target, harness):
        log(f"present: gstack core for {harness}")
        return ok

    if args.install_local_gstack:
        source = local_gstack_source(args, harness)
        if source:
            ok = copy_tree(source, target / "gstack", args.dry_run, overwrite=args.force_deps) and ok
            if has_gstack_core(target, harness) or args.dry_run:
                return ok
        log("missing local gstack source")

    log(f"warning: gstack core not found for {harness}")
    log("note: computa-swarm-verify can still use systematic-debugging/manual investigation, but gstack investigate may be unavailable.")
    return ok


def append_kimi_extra_skill_dir(skill_dir: Path, dry_run: bool) -> bool:
    config = Path.home() / ".kimi-code" / "config.toml"
    value = str(skill_dir)
    if not config.exists():
        content = f'merge_all_available_skills = true\nextra_skill_dirs = [\n  "{value}",\n]\n'
        log(f"create Kimi config {config}")
        if not dry_run:
            config.parent.mkdir(parents=True, exist_ok=True)
            config.write_text(content)
        return True

    text = config.read_text()
    if value in text:
        log(f"present: Kimi extra_skill_dirs includes {value}")
        return True

    lines = text.splitlines()
    out: list[str] = []
    inserted = False
    in_array = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("merge_all_available_skills"):
            out.append("merge_all_available_skills = true")
            continue
        out.append(line)
        if stripped.startswith("extra_skill_dirs") and "[" in stripped:
            if "]" in stripped and stripped.index("[") < stripped.index("]"):
                out[-1] = line.rstrip().replace("]", f', "{value}"]')
                inserted = True
            else:
                in_array = True
            continue
        if in_array and stripped == "]":
            out.insert(len(out) - 1, f'  "{value}",')
            inserted = True
            in_array = False

    if not inserted:
        out.append("merge_all_available_skills = true")
        out.append("extra_skill_dirs = [")
        out.append(f'  "{value}",')
        out.append("]")

    log(f"update Kimi config {config}")
    if not dry_run:
        backup_existing(config, dry_run=False)
        config.write_text("\n".join(out) + "\n")
    return True


def load_json_object(path: Path) -> dict | None:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        log(f"warning: cannot parse JSON config {path}: {exc}")
        return None
    if not isinstance(data, dict):
        log(f"warning: JSON config is not an object: {path}")
        return None
    return data


def write_json_config(path: Path, data: dict, dry_run: bool) -> None:
    log(f"update JSON config {path}")
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup_existing(path, dry_run=False)
    path.write_text(json.dumps(data, indent=2) + "\n")


def rendered_text(src: Path) -> str:
    return src.read_text().replace("/Users/cole/Desktop/swarm-verify-skills", str(ROOT))


def copy_rendered_file(src: Path, dst: Path, dry_run: bool, overwrite: bool = True) -> bool:
    if not src.exists():
        log(f"missing source: {src}")
        return False
    if dst.exists():
        if not overwrite:
            log(f"present: {dst}")
            return True
        backup_existing(dst, dry_run)
    log(f"install {src} -> {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(rendered_text(src))
    return True


def merge_hook_maps(existing: dict, additions: dict) -> bool:
    changed = False
    hooks = existing.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        log("warning: existing hooks value is not an object")
        return False
    for event, groups in additions.get("hooks", {}).items():
        current = hooks.setdefault(event, [])
        if not isinstance(current, list):
            log(f"warning: existing hooks.{event} is not a list")
            continue
        for group in groups:
            if group not in current:
                current.append(group)
                changed = True
                log(f"add: hook {event}")
    return changed


def merge_hooks_file(template: Path, target: Path, dry_run: bool) -> bool:
    if not template.exists():
        log(f"missing source: {template}")
        return False
    additions = json.loads(rendered_text(template))
    existing = load_json_object(target)
    if existing is None:
        return False
    changed = merge_hook_maps(existing, additions)
    if changed or not target.exists():
        write_json_config(target, existing, dry_run)
    else:
        log(f"present: hooks in {target}")
    return True


def merge_cursor_hooks_file(template: Path, target: Path, dry_run: bool) -> bool:
    if not template.exists():
        log(f"missing source: {template}")
        return False
    additions = json.loads(rendered_text(template))
    existing = load_json_object(target)
    if existing is None:
        return False

    changed = False
    if existing.get("version") != additions.get("version"):
        existing["version"] = additions.get("version", 1)
        changed = True
    hooks = existing.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        log(f"warning: existing Cursor hooks value is not an object: {target}")
        return False
    for event, entries in additions.get("hooks", {}).items():
        current = hooks.setdefault(event, [])
        if not isinstance(current, list):
            log(f"warning: existing Cursor hooks.{event} is not a list")
            continue
        for entry in entries:
            if entry not in current:
                current.append(entry)
                changed = True
                log(f"add: Cursor hook {event}")
    if changed or not target.exists():
        write_json_config(target, existing, dry_run)
    else:
        log(f"present: Cursor hooks in {target}")
    return True


def install_kimi_hooks_config(dry_run: bool) -> bool:
    config = Path.home() / ".kimi-code" / "config.toml"
    if not KIMI_HOOKS_TOML.exists():
        log(f"missing source: {KIMI_HOOKS_TOML}")
        return False
    block = rendered_text(KIMI_HOOKS_TOML).strip() + "\n"
    start = "# BEGIN COMPUTA HOOKS"
    end = "# END COMPUTA HOOKS"

    if config.exists():
        text = config.read_text()
    else:
        text = ""

    if start in text and end in text:
        before, rest = text.split(start, 1)
        _old, after = rest.split(end, 1)
        updated = before.rstrip() + "\n\n" + block + after.lstrip()
        action = "update"
    else:
        updated = text.rstrip() + ("\n\n" if text.strip() else "") + block
        action = "append"

    if updated == text:
        log(f"present: Kimi Computa hooks in {config}")
        return True

    log(f"{action}: Kimi hooks in {config}")
    if not dry_run:
        config.parent.mkdir(parents=True, exist_ok=True)
        if config.exists():
            backup_existing(config, dry_run=False)
        config.write_text(updated)
    return True


def add_missing_mapping_entries(existing: dict, additions: dict, label: str) -> bool:
    changed = False
    for name, spec in additions.items():
        if name in existing:
            log(f"present: {label} {name}")
            continue
        existing[name] = spec
        changed = True
        log(f"add: {label} {name}")
    return changed


def ensure_kimi_mcp_config(dry_run: bool) -> bool:
    config = Path.home() / ".kimi-code" / "mcp.json"
    data = load_json_object(config)
    if data is None:
        return False
    servers = data.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        log(f"warning: Kimi mcpServers is not an object: {config}")
        return False
    changed = add_missing_mapping_entries(servers, KIMI_MCP_SERVERS, "Kimi MCP server")
    if changed or not config.exists():
        write_json_config(config, data, dry_run)
    else:
        log(f"present: Kimi MCP config {config}")
    return True


def ensure_opencode_config(skill_target: Path, dry_run: bool) -> bool:
    config = Path.home() / ".config" / "opencode" / "opencode.json"
    data = load_json_object(config)
    if data is None:
        return False

    changed = False
    if "$schema" not in data:
        data["$schema"] = "https://opencode.ai/config.json"
        changed = True

    instruction_paths = [str(skill_target / name / "SKILL.md") for name in SUITE_SKILLS]
    existing_instructions = data.get("instructions", [])
    if isinstance(existing_instructions, str):
        existing_instructions = [existing_instructions]
        data["instructions"] = existing_instructions
        changed = True
    update_instructions = True
    if not isinstance(existing_instructions, list):
        log(f"warning: OpenCode instructions is not a list: {config}")
        update_instructions = False
    if update_instructions:
        original_count = len(existing_instructions)
        existing_instructions[:] = [
            instruction
            for instruction in existing_instructions
            if not any(f"/{legacy}/SKILL.md" in str(instruction) for legacy in LEGACY_SUITE_SKILLS)
        ]
        if len(existing_instructions) != original_count:
            changed = True
            log("remove: legacy OpenCode swarm-verify instruction")
        for instruction in instruction_paths:
            if instruction not in existing_instructions:
                existing_instructions.append(instruction)
                changed = True
                log(f"add: OpenCode instruction {instruction}")
        data["instructions"] = existing_instructions

    mcp = data.setdefault("mcp", {})
    if not isinstance(mcp, dict):
        log(f"warning: OpenCode mcp is not an object: {config}")
        return False
    changed = add_missing_mapping_entries(mcp, OPENCODE_MCP_SERVERS, "OpenCode MCP server") or changed

    if changed or not config.exists():
        write_json_config(config, data, dry_run)
    else:
        log(f"present: OpenCode config {config}")
    return True


def ensure_cursor_mcp_config(args: argparse.Namespace) -> bool:
    if args.project:
        config = Path(args.project).expanduser().resolve() / ".cursor" / "mcp.json"
    else:
        config = Path.home() / ".cursor" / "mcp.json"

    data = load_json_object(config)
    if data is None:
        return False
    servers = data.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        log(f"warning: Cursor mcpServers is not an object: {config}")
        return False
    changed = add_missing_mapping_entries(servers, CURSOR_MCP_SERVERS, "Cursor MCP server")
    if changed or not config.exists():
        write_json_config(config, data, args.dry_run)
    else:
        log(f"present: Cursor MCP config {config}")
    return True


def install_skill_harness(args: argparse.Namespace, harness: str) -> bool:
    target = Path(args.target).expanduser() if args.target and args.harness != "all" else default_target(harness)
    target = target.resolve()
    log(f"[{harness}] target: {target}")
    ok = install_suite(harness, target, args.dry_run)
    if not args.skip_deps:
        ok = install_dependencies(args, harness, target) and ok
    if harness == "kimi":
        if not args.no_kimi_config:
            ok = append_kimi_extra_skill_dir(target, args.dry_run) and ok
        if not args.no_mcp_config:
            ok = ensure_kimi_mcp_config(args.dry_run) and ok
    if harness == "opencode" and not args.no_mcp_config:
        ok = ensure_opencode_config(target, args.dry_run) and ok
    if args.install_hooks:
        ok = install_hooks(args, harness) and ok
    return ok


def install_cursor(args: argparse.Namespace) -> bool:
    if args.project:
        target = Path(args.project).expanduser().resolve() / ".cursor" / "rules" / "computa-swarm-verify.mdc"
        log(f"[cursor] project rule: {target}")
        ok = copy_file(CURSOR_RULE, target, args.dry_run)
    else:
        target = Path.home() / ".cursor" / "rules" / "computa-swarm-verify.mdc"
        log(f"[cursor] staging rule: {target}")
        ok = copy_file(CURSOR_RULE, target, args.dry_run)
        log("note: Cursor's reliable documented project install is <project>/.cursor/rules; rerun with --project for project-scoped rules.")

    if not args.no_mcp_config:
        ok = ensure_cursor_mcp_config(args) and ok
    if args.install_hooks:
        ok = install_hooks(args, "cursor") and ok
    return ok


def install_generic(args: argparse.Namespace) -> bool:
    if args.project:
        target = Path(args.project).expanduser().resolve() / "AGENTS.computa-swarm-verify.md"
    else:
        target = Path.home() / ".computa" / "AGENTS.computa-swarm-verify.md"
    log(f"[generic] target: {target}")
    ok = copy_file(GENERIC_AGENTS, target, args.dry_run)
    if args.install_hooks:
        ok = install_hooks(args, "generic") and ok
    return ok


def install_goose(args: argparse.Namespace) -> bool:
    target = Path.home() / ".config" / "goose" / "recipes" / "computa-swarm-verify.yaml"
    log(f"[goose] recipe: {target}")
    ok = copy_file(GOOSE_RECIPE, target, args.dry_run)
    log('note: run with `goose run --recipe ~/.config/goose/recipes/computa-swarm-verify.yaml --recipe-param task="..."`.')
    log("note: add this directory to GOOSE_RECIPE_PATH if your Goose build does not discover it.")
    if args.install_hooks:
        ok = install_hooks(args, "goose") and ok
    return ok


def install_hooks(args: argparse.Namespace, harness: str) -> bool:
    home = Path.home()
    if harness == "codex":
        target = (
            Path(args.project).expanduser().resolve() / ".codex" / "hooks.json"
            if args.project
            else Path(os.environ.get("CODEX_HOME", home / ".codex")) / "hooks.json"
        )
        log(f"[codex hooks] {target}")
        return merge_hooks_file(CODEX_HOOKS, target, args.dry_run)
    if harness == "claude-code":
        target = (
            Path(args.project).expanduser().resolve() / ".claude" / "settings.local.json"
            if args.project
            else home / ".claude" / "settings.json"
        )
        log(f"[claude-code hooks] {target}")
        return merge_hooks_file(CLAUDE_HOOKS, target, args.dry_run)
    if harness == "goose":
        target = (
            Path(args.project).expanduser().resolve() / ".agents" / "plugins" / "computa-hooks"
            if args.project
            else home / ".agents" / "plugins" / "computa-hooks"
        )
        log(f"[goose hooks] {target}")
        return copy_tree(GOOSE_HOOK_PLUGIN, target, args.dry_run, overwrite=True)
    if harness == "kimi":
        doc_target = home / ".kimi-code" / "COMPUTA_HOOKS.md"
        log(f"[kimi hooks] {home / '.kimi-code' / 'config.toml'}")
        ok = install_kimi_hooks_config(args.dry_run)
        log(f"[kimi hooks doc] {doc_target}")
        return copy_rendered_file(KIMI_HOOKS_DOC, doc_target, args.dry_run) and ok
    if harness == "opencode":
        if args.project:
            plugin_target = Path(args.project).expanduser().resolve() / ".opencode" / "plugins" / "computa-hooks.js"
            doc_target = Path(args.project).expanduser().resolve() / ".opencode" / "COMPUTA_HOOKS.md"
        else:
            plugin_target = home / ".config" / "opencode" / "plugins" / "computa-hooks.js"
            doc_target = home / ".config" / "opencode" / "COMPUTA_HOOKS.md"
        log(f"[opencode hooks plugin] {plugin_target}")
        ok = copy_rendered_file(OPENCODE_HOOK_PLUGIN, plugin_target, args.dry_run)
        log(f"[opencode hooks doc] {doc_target}")
        return copy_rendered_file(OPENCODE_HOOKS_DOC, doc_target, args.dry_run) and ok
    if harness == "cursor":
        hooks_target = (
            Path(args.project).expanduser().resolve() / ".cursor" / "hooks.json"
            if args.project
            else home / ".cursor" / "hooks.json"
        )
        doc_target = (
            Path(args.project).expanduser().resolve() / ".cursor" / "rules" / "computa-hooks.mdc"
            if args.project
            else home / ".cursor" / "rules" / "computa-hooks.mdc"
        )
        log(f"[cursor hooks] {hooks_target}")
        ok = merge_cursor_hooks_file(CURSOR_HOOKS, hooks_target, args.dry_run)
        log(f"[cursor hooks doc] {doc_target}")
        return copy_rendered_file(CURSOR_HOOKS_DOC, doc_target, args.dry_run) and ok
    if harness == "generic":
        target = (
            Path(args.project).expanduser().resolve() / "COMPUTA_HOOKS.md"
            if args.project
            else home / ".computa" / "COMPUTA_HOOKS.md"
        )
        log(f"[generic hooks doc] {target}")
        return copy_rendered_file(GENERIC_HOOKS_DOC, target, args.dry_run)
    if harness == "agent-skills":
        target = home / ".agents" / "COMPUTA_HOOKS.md"
        log(f"[agent-skills hooks doc] {target}")
        return copy_rendered_file(GENERIC_HOOKS_DOC, target, args.dry_run)
    return True


def install_harness(args: argparse.Namespace, harness: str) -> bool:
    if harness in SKILL_HARNESSES:
        return install_skill_harness(args, harness)
    if harness == "cursor":
        return install_cursor(args)
    if harness == "goose":
        return install_goose(args)
    if harness == "generic":
        return install_generic(args)
    raise ValueError(f"unsupported harness: {harness}")


def main() -> int:
    args = parse_args()
    ok = True
    for harness in selected_harnesses(args.harness):
        ok = install_harness(args, harness) and ok

    if ok:
        log("install complete")
        return 0

    log("install finished with missing dependencies or failed copies")
    return 2


if __name__ == "__main__":
    sys.exit(main())
