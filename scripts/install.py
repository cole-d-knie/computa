#!/usr/bin/env python3
"""Install the swarm-verify suite for multiple coding-agent harnesses."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE_DIR = ROOT / "skills"
KIMI_SUITE_DIR = ROOT / "harnesses" / "kimi" / "skills"
VENDOR_DIR = ROOT / "vendor" / "skills"
CURSOR_RULE = ROOT / "harnesses" / "cursor" / "rules" / "swarm-verify.mdc"
GOOSE_RECIPE = ROOT / "harnesses" / "goose" / "recipes" / "swarm-verify.yaml"
GENERIC_AGENTS = ROOT / "harnesses" / "generic" / "AGENTS.swarm-verify.md"

SKILL_HARNESSES = {"codex", "claude-code", "kimi", "opencode", "agent-skills"}
PROJECT_HARNESSES = {"cursor", "generic"}
RECIPE_HARNESSES = {"goose"}

SUITE_SKILLS = [
    "swarm-verify",
    "swarm-verify-setup",
    "swarm-verify-investigate",
    "swarm-verify-tdd-qa",
    "swarm-verify-swarms",
    "swarm-verify-closeout",
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
        description="Install swarm-verify for Codex, Claude Code, Kimi, OpenCode, Cursor, Goose, and generic AGENTS.md harnesses."
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
        help="Install only swarm-verify suite skills, not dependency skills.",
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
    log("note: swarm-verify can still use systematic-debugging/manual investigation, but gstack investigate may be unavailable.")
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


def install_skill_harness(args: argparse.Namespace, harness: str) -> bool:
    target = Path(args.target).expanduser() if args.target and args.harness != "all" else default_target(harness)
    target = target.resolve()
    log(f"[{harness}] target: {target}")
    ok = install_suite(harness, target, args.dry_run)
    if not args.skip_deps:
        ok = install_dependencies(args, harness, target) and ok
    if harness == "kimi" and not args.no_kimi_config:
        ok = append_kimi_extra_skill_dir(target, args.dry_run) and ok
    return ok


def install_cursor(args: argparse.Namespace) -> bool:
    if args.project:
        target = Path(args.project).expanduser().resolve() / ".cursor" / "rules" / "swarm-verify.mdc"
        log(f"[cursor] project rule: {target}")
        return copy_file(CURSOR_RULE, target, args.dry_run)

    target = Path.home() / ".cursor" / "rules" / "swarm-verify.mdc"
    log(f"[cursor] staging rule: {target}")
    ok = copy_file(CURSOR_RULE, target, args.dry_run)
    log("note: Cursor's reliable documented project install is <project>/.cursor/rules; rerun with --project for project-scoped rules.")
    return ok


def install_generic(args: argparse.Namespace) -> bool:
    if args.project:
        target = Path(args.project).expanduser().resolve() / "AGENTS.swarm-verify.md"
    else:
        target = Path.home() / ".swarm-verify-skills" / "AGENTS.swarm-verify.md"
    log(f"[generic] target: {target}")
    return copy_file(GENERIC_AGENTS, target, args.dry_run)


def install_goose(args: argparse.Namespace) -> bool:
    target = Path.home() / ".config" / "goose" / "recipes" / "swarm-verify.yaml"
    log(f"[goose] recipe: {target}")
    ok = copy_file(GOOSE_RECIPE, target, args.dry_run)
    log('note: run with `goose run --recipe ~/.config/goose/recipes/swarm-verify.yaml --recipe-param task="..."`.')
    log("note: add this directory to GOOSE_RECIPE_PATH if your Goose build does not discover it.")
    return ok


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
