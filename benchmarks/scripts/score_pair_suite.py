#!/usr/bin/env python3
"""Score paired vulnerable/fixed benchmark runs."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import score_suite


@dataclass
class PairResult:
    mode: str
    pair_id: str
    vulnerable_score: float
    vulnerable_recall: float
    vulnerable_extra: int
    fixed_score: float
    fixed_extra: int
    fixed_clean: bool
    pair_score: float


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def build_variant_manifest(pair_manifest: dict[str, Any], variant: str) -> dict[str, Any]:
    manifest = dict(pair_manifest["variants"][variant])
    manifest["id"] = f"{pair_manifest['id']}-{variant}"
    return manifest


def render_markdown(results: list[PairResult]) -> str:
    lines = [
        "# agent-rock Pair Regression Scoreboard",
        "",
        "| Mode | Pair | Vuln Recall | Vuln Extra | Fixed Extra | Fixed Clean | Pair Score |",
        "|------|------|-------------|------------|-------------|-------------|------------|",
    ]

    for result in results:
        lines.append(
            "| {mode} | {pair_id} | {vulnerable_recall:.2f} | {vulnerable_extra} | {fixed_extra} | {fixed_clean} | {pair_score:.2f} |".format(
                mode=result.mode,
                pair_id=result.pair_id,
                vulnerable_recall=result.vulnerable_recall,
                vulnerable_extra=result.vulnerable_extra,
                fixed_extra=result.fixed_extra,
                fixed_clean="yes" if result.fixed_clean else "no",
                pair_score=result.pair_score,
            )
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Score paired vulnerable/fixed benchmark runs.")
    parser.add_argument("--results-dir", required=True, help="Directory containing quick/ and deep/ pair results")
    parser.add_argument("--out", help="Optional markdown output file")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    pairs_root = repo_root / "benchmarks" / "pairs"
    results_dir = Path(args.results_dir).resolve()

    if not results_dir.is_dir():
        raise SystemExit(f"Missing pair results directory: {results_dir}")

    results: list[PairResult] = []

    for mode_dir in sorted(p for p in results_dir.iterdir() if p.is_dir()):
        mode = mode_dir.name
        for pair_dir in sorted(p for p in pairs_root.iterdir() if p.is_dir()):
            pair_manifest_path = pair_dir / "pair.json"
            if not pair_manifest_path.is_file():
                continue

            pair_manifest = load_json(pair_manifest_path)
            vulnerable_report = mode_dir / pair_manifest["id"] / "vulnerable" / "security-audit-report.json"
            fixed_report = mode_dir / pair_manifest["id"] / "fixed" / "security-audit-report.json"
            if not vulnerable_report.is_file() or not fixed_report.is_file():
                continue

            vulnerable_case = score_suite.score_case(
                build_variant_manifest(pair_manifest, "vulnerable"),
                load_json(vulnerable_report),
                mode,
            )
            fixed_case = score_suite.score_case(
                build_variant_manifest(pair_manifest, "fixed"),
                load_json(fixed_report),
                mode,
            )

            fixed_clean = fixed_case.extra == 0 and fixed_case.matched == 0 and fixed_case.expected == 0
            pair_score = round((vulnerable_case.score + fixed_case.score) / 2.0, 2)
            results.append(
                PairResult(
                    mode=mode,
                    pair_id=pair_manifest["id"],
                    vulnerable_score=vulnerable_case.score,
                    vulnerable_recall=vulnerable_case.recall,
                    vulnerable_extra=vulnerable_case.extra,
                    fixed_score=fixed_case.score,
                    fixed_extra=fixed_case.extra,
                    fixed_clean=fixed_clean,
                    pair_score=pair_score,
                )
            )

    markdown = render_markdown(results)

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown)
        print(f"Wrote pair scoreboard to {out_path}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
