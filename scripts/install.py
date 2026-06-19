#!/usr/bin/env python3
"""Install the swarm-verify skill suite and its lightweight skill dependencies."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE_DIR = ROOT / "skills"
VENDOR_DIR = ROOT / "vendor" / "skills"

SUITE_SKILLS = [
    "swarm-verify",
    "swarm-verify-setup",
    "swarm-verify-investigate",
    "swarm-verify-tdd-qa",
    "swarm-verify-swarms",
    "swarm-verify-closeout",
]

VENDORED_DEPENDENCIES = [
    "caveman",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install swarm-verify skills into CODEX_HOME skills."
    )
    parser.add_argument(
        "--target",
        default=str(Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills"),
        help="Skill install directory. Default: ${CODEX_HOME:-~/.codex}/skills",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without changing files.",
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Install only swarm-verify suite skills, not dependencies.",
    )
    parser.add_argument(
        "--force-deps",
        action="store_true",
        help="Overwrite installed dependency skill folders with vendored copies.",
    )
    parser.add_argument(
        "--install-local-gstack",
        action="store_true",
        help="Copy a local gstack core skill into the target if found. This can be large.",
    )
    parser.add_argument(
        "--gstack-source",
        default="",
        help="Optional local gstack source directory for --install-local-gstack.",
    )
    return parser.parse_args()


def log(message: str) -> None:
    print(message)


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


def candidate_skill_roots(target: Path) -> list[Path]:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    roots = [
        target,
        codex_home / "skills",
        Path.home() / ".codex" / "skills",
        Path.home() / ".agents" / "skills",
    ]
    plugin_root = codex_home / "plugins" / "cache"
    if plugin_root.exists():
        roots.extend(plugin_root.glob("*/*/skills"))
        roots.extend(plugin_root.glob("*/*/*/skills"))
    return list(dict.fromkeys(path.resolve() for path in roots if path.exists()))


def has_gstack_core(target: Path) -> bool:
    for root in candidate_skill_roots(target):
        if (root / "gstack" / "bin" / "gstack-update-check").exists():
            return True
    return False


def local_gstack_source(args: argparse.Namespace) -> Path | None:
    candidates = []
    if args.gstack_source:
        candidates.append(Path(args.gstack_source).expanduser())
    candidates.extend(
        [
            Path.home() / ".codex" / "skills" / "gstack",
            Path.home() / ".agents" / "skills" / "gstack",
        ]
    )
    for candidate in candidates:
        if (candidate / "bin" / "gstack-update-check").exists():
            return candidate
    return None


def install_suite(target: Path, dry_run: bool) -> bool:
    ok = True
    for name in SUITE_SKILLS:
        ok = copy_tree(SUITE_DIR / name, target / name, dry_run, overwrite=True) and ok
    return ok


def install_dependencies(args: argparse.Namespace, target: Path) -> bool:
    ok = True
    for name in VENDORED_DEPENDENCIES:
        dst = target / name
        overwrite = args.force_deps or not dst.exists()
        ok = copy_tree(VENDOR_DIR / name, dst, args.dry_run, overwrite=overwrite) and ok

    if has_gstack_core(target):
        log("present: gstack core")
        return ok

    if args.install_local_gstack:
        source = local_gstack_source(args)
        if source:
            ok = copy_tree(source, target / "gstack", args.dry_run, overwrite=args.force_deps) and ok
            if has_gstack_core(target) or args.dry_run:
                return ok
        log("missing local gstack source")

    log("missing: gstack core")
    log("note: gstack-investigate is installed, but its generated preamble expects gstack core.")
    log("fix: install gstack separately, or rerun with --install-local-gstack on a machine that already has it.")
    return False


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    log(f"target: {target}")

    ok = install_suite(target, args.dry_run)
    if not args.skip_deps:
        ok = install_dependencies(args, target) and ok

    if ok:
        log("install complete")
        return 0

    log("install finished with missing dependencies")
    return 2


if __name__ == "__main__":
    sys.exit(main())
