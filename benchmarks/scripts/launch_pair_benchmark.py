#!/usr/bin/env python3
"""Launch paired vulnerable/fixed Claude Code benchmark runs in Terminal.app."""

from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


DEFAULT_PAIRS = [
    "express-sqli-auth-regression",
]

DEFAULT_MODES = ["quick", "deep"]
DEFAULT_VARIANTS = ["vulnerable", "fixed"]


def run_materialize(repo_root: Path, pair_id: str, variant: str, out_dir: Path) -> None:
    script = repo_root / "benchmarks" / "scripts" / "materialize_pair_case.py"
    subprocess.run(
        [
            "python3",
            str(script),
            "--pair",
            pair_id,
            "--variant",
            variant,
            "--out",
            str(out_dir),
            "--skip-git",
        ],
        check=True,
        cwd=repo_root,
        capture_output=True,
        text=True,
    )


def build_launch_command(work_dir: Path, claude_cmd: str, permission_mode: str) -> str:
    return (
        f"cd {shlex.quote(str(work_dir))} && "
        f"{shlex.quote(claude_cmd)} --permission-mode {shlex.quote(permission_mode)}"
    )


def build_skill_command(mode: str) -> str:
    return "/rock-quick" if mode == "quick" else "/rock-deep"


def launch_terminal(command: str, skill_command: str, startup_delay: float) -> None:
    script = f'''
tell application "Terminal"
  activate
  set benchWindow to do script "{command}"
  delay {startup_delay}
  do script "{skill_command}" in benchWindow
end tell
'''
    subprocess.run(["osascript", "-e", script], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch paired vulnerable/fixed benchmark runs in Terminal.app.")
    parser.add_argument("--run-name", required=True, help="Run name under benchmarks/pair-runs/")
    parser.add_argument("--pairs", nargs="*", default=DEFAULT_PAIRS, help="Pair ids to launch")
    parser.add_argument("--modes", nargs="*", default=DEFAULT_MODES, help="Modes to launch (quick deep)")
    parser.add_argument(
        "--variants",
        nargs="*",
        default=DEFAULT_VARIANTS,
        help="Variants to launch (vulnerable fixed)",
    )
    parser.add_argument("--claude-cmd", default="claude", help="Claude Code command")
    parser.add_argument(
        "--permission-mode",
        default="bypassPermissions",
        help="Claude permission mode for automated benchmark runs",
    )
    parser.add_argument(
        "--work-root",
        default="/tmp/agent-rock-pairs",
        help="Temporary root for materialized paired benchmark repos",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated commands without opening Terminal.app",
    )
    parser.add_argument(
        "--startup-delay",
        type=float,
        default=2.0,
        help="Seconds to wait before sending the slash command into Claude",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    pairs_root = repo_root / "benchmarks" / "pairs"
    work_root = Path(args.work_root).resolve() / args.run_name

    for pair_id in args.pairs:
        if not (pairs_root / pair_id / "pair.json").is_file():
            raise SystemExit(f"Unknown pair: {pair_id}")

    for mode in args.modes:
        if mode not in {"quick", "deep"}:
            raise SystemExit(f"Unsupported mode: {mode}")

    for variant in args.variants:
        if variant not in {"vulnerable", "fixed"}:
            raise SystemExit(f"Unsupported variant: {variant}")

    for mode in args.modes:
        for pair_id in args.pairs:
            for variant in args.variants:
                work_dir = work_root / mode / pair_id / variant
                run_materialize(repo_root, pair_id, variant, work_dir)
                command = build_launch_command(
                    work_dir=work_dir,
                    claude_cmd=args.claude_cmd,
                    permission_mode=args.permission_mode,
                )
                skill_command = build_skill_command(mode)
                if args.dry_run:
                    print(f"[dry-run] {mode}/{pair_id}/{variant}")
                    print(command)
                    print(skill_command)
                    print()
                else:
                    launch_terminal(command, skill_command, args.startup_delay)

    if not args.dry_run:
        print(f"Launched paired benchmark run '{args.run_name}'.")
        print(f"Workdirs live under: {work_root}")
        print("After the Claude sessions finish, run collect_pair_results.py to copy reports into benchmarks/pair-runs/.")


if __name__ == "__main__":
    main()
