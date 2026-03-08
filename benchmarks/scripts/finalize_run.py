#!/usr/bin/env python3
"""Collect benchmark results, score them, and optionally open the scoreboard."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Finalize a benchmark run.")
    parser.add_argument("--run-name", required=True, help="Benchmark run name")
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the generated scoreboard in the default macOS app",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    collect_script = repo_root / "benchmarks" / "scripts" / "collect_results.py"
    score_script = repo_root / "benchmarks" / "scripts" / "score_suite.py"
    render_script = repo_root / "benchmarks" / "scripts" / "render_scoreboard_svg.py"
    results_dir = repo_root / "benchmarks" / "runs" / args.run_name
    scoreboard = results_dir / "scoreboard.md"
    scoreboard_svg = results_dir / "scoreboard.svg"
    latest_svg = repo_root / "benchmarks" / "latest-scoreboard.svg"

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
            str(render_script),
            "--results-dir",
            str(results_dir),
            "--out",
            str(scoreboard_svg),
            "--run-name",
            args.run_name,
        ],
        cwd=repo_root,
        check=True,
    )
    subprocess.run(
        [
            "python3",
            str(render_script),
            "--results-dir",
            str(results_dir),
            "--out",
            str(latest_svg),
            "--run-name",
            args.run_name,
        ],
        cwd=repo_root,
        check=True,
    )

    print(f"Scoreboard written to {scoreboard}")
    print(f"GitHub-ready SVG written to {latest_svg}")

    if args.open:
        subprocess.run(["open", str(scoreboard)], check=True)


if __name__ == "__main__":
    main()
