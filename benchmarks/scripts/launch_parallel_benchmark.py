#!/usr/bin/env python3
"""Launch parallel Claude Code benchmark runs in Terminal.app."""

from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


DEFAULT_CASES = [
    "express-api-basic",
    "django-invoices-basic",
    "laravel-preview-basic",
]

DEFAULT_MODES = ["quick", "deep"]


def run_materialize(repo_root: Path, case_id: str, out_dir: Path) -> None:
    script = repo_root / "benchmarks" / "scripts" / "materialize_case.py"
    subprocess.run(
        ["python3", str(script), "--case", case_id, "--out", str(out_dir), "--skip-git"],
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
    parser = argparse.ArgumentParser(description="Launch parallel Claude Code benchmark runs in Terminal.app.")
    parser.add_argument("--run-name", required=True, help="Run name under benchmarks/runs/")
    parser.add_argument("--cases", nargs="*", default=DEFAULT_CASES, help="Case ids to launch")
    parser.add_argument("--modes", nargs="*", default=DEFAULT_MODES, help="Modes to launch (quick deep)")
    parser.add_argument("--claude-cmd", default="claude", help="Claude Code command")
    parser.add_argument(
        "--permission-mode",
        default="bypassPermissions",
        help="Claude permission mode for automated benchmark runs",
    )
    parser.add_argument(
        "--work-root",
        default="/tmp/agent-rock-bench",
        help="Temporary root for materialized benchmark repos",
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
    cases_root = repo_root / "benchmarks" / "cases"
    work_root = Path(args.work_root).resolve() / args.run_name

    for case_id in args.cases:
        if not (cases_root / case_id / "benchmark.json").is_file():
            raise SystemExit(f"Unknown case: {case_id}")

    for mode in args.modes:
        if mode not in {"quick", "deep"}:
            raise SystemExit(f"Unsupported mode: {mode}")

    for mode in args.modes:
        for case_id in args.cases:
            work_dir = work_root / mode / case_id
            run_materialize(repo_root, case_id, work_dir)
            command = build_launch_command(
                work_dir=work_dir,
                claude_cmd=args.claude_cmd,
                permission_mode=args.permission_mode,
            )
            skill_command = build_skill_command(mode)
            if args.dry_run:
                print(f"[dry-run] {mode}/{case_id}")
                print(command)
                print(skill_command)
                print()
            else:
                launch_terminal(command, skill_command, args.startup_delay)

    if not args.dry_run:
        print(f"Launched benchmark run '{args.run_name}'.")
        print(f"Workdirs live under: {work_root}")
        print("After the Claude sessions finish, run collect_results.py to copy reports into benchmarks/runs/.")


if __name__ == "__main__":
    main()
