#!/usr/bin/env python3
"""Collect paired benchmark results, score them, and optionally open the scoreboard."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Finalize a paired benchmark run.")
    parser.add_argument("--run-name", required=True, help="Paired benchmark run name")
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the generated scoreboard in the default macOS app",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    collect_script = repo_root / "benchmarks" / "scripts" / "collect_pair_results.py"
    score_script = repo_root / "benchmarks" / "scripts" / "score_pair_suite.py"
    progress_script = repo_root / "benchmarks" / "scripts" / "render_progress_report.py"
    results_dir = repo_root / "benchmarks" / "pair-runs" / args.run_name
    scoreboard = results_dir / "scoreboard.md"
    progress_report = repo_root / "benchmarks" / "progress.md"

    subprocess.run(
        ["python3", str(collect_script), "--run-name", args.run_name],
        cwd=repo_root,
        check=True,
    )
    subprocess.run(
        [
            "python3",
            str(score_script),
            "--results-dir",
            str(results_dir),
            "--out",
            str(scoreboard),
        ],
        cwd=repo_root,
        check=True,
    )
    subprocess.run(
        [
            "python3",
            str(progress_script),
            "--out",
            str(progress_report),
        ],
        cwd=repo_root,
        check=True,
    )

    print(f"Pair scoreboard written to {scoreboard}")
    print(f"Progress report written to {progress_report}")

    if args.open:
        subprocess.run(["open", str(scoreboard)], check=True)


if __name__ == "__main__":
    main()
