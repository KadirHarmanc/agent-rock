#!/usr/bin/env python3
"""Collect finished paired benchmark reports from workdirs into benchmarks/pair-runs/<run-name>/."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect paired benchmark reports from temp workdirs.")
    parser.add_argument("--run-name", required=True, help="Run name used by launch_pair_benchmark.py")
    parser.add_argument(
        "--work-root",
        default="/tmp/agent-rock-pairs",
        help="Temporary root used during paired benchmark launch",
    )
    parser.add_argument(
        "--results-root",
        help="Override paired benchmark results root (defaults to benchmarks/pair-runs/<run-name>)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    work_root = Path(args.work_root).resolve() / args.run_name
    results_root = (
        Path(args.results_root).resolve()
        if args.results_root
        else (repo_root / "benchmarks" / "pair-runs" / args.run_name)
    )

    copied = 0
    missing: list[str] = []

    for mode_dir in sorted(p for p in work_root.iterdir() if p.is_dir()):
        for pair_dir in sorted(p for p in mode_dir.iterdir() if p.is_dir()):
            for variant_dir in sorted(p for p in pair_dir.iterdir() if p.is_dir()):
                src_json = variant_dir / "security-audit-report.json"
                src_md = variant_dir / "security-audit-report.md"
                if not src_json.is_file():
                    missing.append(f"{mode_dir.name}/{pair_dir.name}/{variant_dir.name}")
                    continue

                dest_dir = results_root / mode_dir.name / pair_dir.name / variant_dir.name
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_json, dest_dir / "security-audit-report.json")
                if src_md.is_file():
                    shutil.copy2(src_md, dest_dir / "security-audit-report.md")
                copied += 1

    print(f"Collected {copied} completed paired benchmark results into {results_root}")
    if missing:
        print("Missing reports:")
        for item in missing:
            print(f"- {item}")


if __name__ == "__main__":
    main()
