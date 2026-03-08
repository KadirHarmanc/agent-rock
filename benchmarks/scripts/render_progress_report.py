#!/usr/bin/env python3
"""Render a benchmark progress report across baseline and paired runs."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RunSummary:
    run_name: str
    quick_score: float | None
    deep_score: float | None

    @property
    def overall_score(self) -> float | None:
        values = [value for value in (self.quick_score, self.deep_score) if value is not None]
        if not values:
            return None
        return round(sum(values) / len(values), 2)


def parse_mode_summary(scoreboard_path: Path, marker: str, score_column: int) -> RunSummary | None:
    lines = scoreboard_path.read_text().splitlines()
    if marker not in lines:
        return None

    start = lines.index(marker) + 3
    quick_score: float | None = None
    deep_score: float | None = None

    for line in lines[start:]:
        if not line.startswith("|"):
            break
        if line.startswith("|------"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) <= score_column:
            continue

        mode = parts[0]
        try:
            score = float(parts[score_column])
        except ValueError:
            continue

        if mode == "quick":
            quick_score = score
        elif mode == "deep":
            deep_score = score

    return RunSummary(
        run_name=scoreboard_path.parent.name,
        quick_score=quick_score,
        deep_score=deep_score,
    )


def baseline_sort_key(path: Path) -> tuple[int, str]:
    name = path.parent.name
    if name.startswith("baseline-"):
        suffix = name.removeprefix("baseline-")
        if suffix.isdigit():
            return (int(suffix), name)
    return (10_000, name)


def pair_sort_key(path: Path) -> tuple[int, str]:
    name = path.parent.name
    if name.startswith("pair-baseline-"):
        suffix = name.removeprefix("pair-baseline-")
        if suffix.isdigit():
            return (int(suffix), name)
    return (10_000, name)


def format_score(value: float | None) -> str:
    return f"{value:.2f}" if value is not None else "-"


def format_delta(current: float | None, previous: float | None) -> str:
    if current is None or previous is None:
        return "-"
    delta = round(current - previous, 2)
    if delta > 0:
        return f"+{delta:.2f}"
    return f"{delta:.2f}"


def render_table(title: str, summaries: list[RunSummary]) -> list[str]:
    lines = [f"## {title}", ""]
    if not summaries:
        lines.append("_No runs yet._")
        lines.append("")
        return lines

    lines.append("| Run | Quick | Deep | Overall | Delta |")
    lines.append("|-----|-------|------|---------|-------|")

    previous_overall: float | None = None
    for summary in summaries:
        overall = summary.overall_score
        lines.append(
            "| {run_name} | {quick} | {deep} | {overall} | {delta} |".format(
                run_name=summary.run_name,
                quick=format_score(summary.quick_score),
                deep=format_score(summary.deep_score),
                overall=format_score(overall),
                delta=format_delta(overall, previous_overall),
            )
        )
        previous_overall = overall

    lines.append("")
    latest = summaries[-1]
    best = max((summary for summary in summaries if summary.overall_score is not None), key=lambda item: item.overall_score)
    lines.append(
        "Latest: `{latest}` scored `{latest_score}`. Best so far: `{best}` with `{best_score}`.".format(
            latest=latest.run_name,
            latest_score=format_score(latest.overall_score),
            best=best.run_name,
            best_score=format_score(best.overall_score),
        )
    )
    lines.append("")
    return lines


def render_report(core_summaries: list[RunSummary], pair_summaries: list[RunSummary]) -> str:
    lines = [
        "# agent-rock Benchmark Progress",
        "",
        "This report exists to answer one question quickly: is agent-rock getting better or not?",
        "",
    ]

    lines.extend(render_table("Core Fixture Benchmarks", core_summaries))
    lines.extend(render_table("Paired Regression Benchmarks", pair_summaries))

    if core_summaries:
        latest_core = core_summaries[-1]
        lines.append("## Current Read")
        lines.append("")
        lines.append(
            "Core suite latest score: `{score}` on `{run_name}`.".format(
                score=format_score(latest_core.overall_score),
                run_name=latest_core.run_name,
            )
        )
        if pair_summaries:
            latest_pair = pair_summaries[-1]
            lines.append(
                "Paired regression latest score: `{score}` on `{run_name}`.".format(
                    score=format_score(latest_pair.overall_score),
                    run_name=latest_pair.run_name,
                )
            )
        lines.append("")
        lines.append("Interpretation:")
        lines.append("- Core score shows how well agent-rock performs on the seeded fixture suite.")
        lines.append("- Pair score shows whether it finds the vulnerable version and stays quiet on the fixed version.")
        lines.append("- If core rises but pair stalls, the skill is improving on fixtures but still weak on replay realism.")
        lines.append("- If pair rises but core stalls, replay handling is improving but general benchmark coverage may be flat.")
        lines.append("")

        lines.append("## Benchmark Health")
        lines.append("")
        if latest_core.overall_score is not None and latest_core.overall_score >= 99.0:
            lines.append(
                "The core fixture suite looks **saturated** right now. A `100.00` here means "
                "agent-rock solved the current seeded regression sheet, not that the product is finished."
            )
        else:
            lines.append(
                "The core fixture suite still has visible headroom, so score changes here remain highly informative."
            )
        if len(pair_summaries) < 3:
            lines.append(
                "Paired replay coverage is still thin. Treat pair results as promising evidence, not final proof."
            )
        else:
            lines.append(
                "Paired replay coverage is starting to become a meaningful secondary exam."
            )
        lines.append("")
        lines.append("Use this rule of thumb:")
        lines.append("- `100.00` on core fixtures = regression health is excellent.")
        lines.append("- `100.00` on core fixtures != the benchmark is complete.")
        lines.append("- Once core saturates, the next honest move is to add harder or unseen cases.")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a benchmark progress report across runs.")
    parser.add_argument("--out", help="Optional markdown output file")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    core_paths = sorted((repo_root / "benchmarks" / "runs").glob("*/scoreboard.md"), key=baseline_sort_key)
    pair_paths = sorted((repo_root / "benchmarks" / "pair-runs").glob("*/scoreboard.md"), key=pair_sort_key)

    core_summaries = [
        summary
        for path in core_paths
        if (summary := parse_mode_summary(path, "## Mode Summary", 4)) is not None
    ]
    pair_summaries = [
        summary
        for path in pair_paths
        if (summary := parse_mode_summary(path, "# agent-rock Pair Regression Scoreboard", 6)) is not None
    ]

    markdown = render_report(core_summaries, pair_summaries)

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown)
        print(f"Wrote benchmark progress report to {out_path}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
