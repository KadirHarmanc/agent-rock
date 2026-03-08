#!/usr/bin/env python3
"""Render a benchmark scoreboard SVG suitable for embedding in GitHub README files."""

from __future__ import annotations

import argparse
import html
from dataclasses import dataclass
from pathlib import Path

import score_suite


WIDTH = 1260
PADDING = 28
HEADER_HEIGHT = 90
SECTION_GAP = 24
TABLE_HEADER_HEIGHT = 34
ROW_HEIGHT = 34
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"

BACKGROUND = "#ffffff"
BORDER = "#d0d7de"
TEXT = "#1f2328"
MUTED = "#57606a"
HEADER_BG = "#f6f8fa"
ROW_ALT = "#f6f8fa"
ACCENT = "#0969da"
SUCCESS = "#1a7f37"
WARN = "#9a6700"
DANGER = "#cf222e"


@dataclass
class ModeSummary:
    mode: str
    avg_precision: float
    avg_recall: float
    avg_score: float


@dataclass
class RunHistory:
    run_name: str
    quick_score: float | None
    deep_score: float | None


def text(x: int, y: int, value: str, *, size: int = 16, weight: str = "400", fill: str = TEXT, mono: bool = False) -> str:
    safe = html.escape(value)
    family = FONT_MONO if mono else FONT
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}">{safe}</text>'
    )


def rect(x: int, y: int, width: int, height: int, *, fill: str = BACKGROUND, stroke: str = BORDER, radius: int = 12) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1" rx="{radius}" />'
    )


def pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def score_fill(score: float) -> str:
    if score >= 95:
        return SUCCESS
    if score >= 85:
        return WARN
    return DANGER


def collect_results(results_dir: Path) -> list[score_suite.CaseResult]:
    repo_root = Path(__file__).resolve().parents[2]
    cases_root = repo_root / "benchmarks" / "cases"
    results: list[score_suite.CaseResult] = []

    for mode_dir in sorted(p for p in results_dir.iterdir() if p.is_dir()):
        mode = mode_dir.name
        for case_dir in sorted(p for p in cases_root.iterdir() if p.is_dir()):
            manifest = score_suite.load_json(case_dir / "benchmark.json")
            report_path = mode_dir / manifest["id"] / "security-audit-report.json"
            if not report_path.is_file():
                continue
            report = score_suite.load_json(report_path)
            results.append(score_suite.score_case(manifest, report, mode))

    return results


def summarize_modes(results: list[score_suite.CaseResult]) -> list[ModeSummary]:
    grouped: dict[str, list[score_suite.CaseResult]] = {}
    for result in results:
        grouped.setdefault(result.mode, []).append(result)

    summaries: list[ModeSummary] = []
    for mode, mode_results in sorted(grouped.items()):
        count = len(mode_results)
        summaries.append(
            ModeSummary(
                mode=mode,
                avg_precision=sum(item.precision for item in mode_results) / count,
                avg_recall=sum(item.recall for item in mode_results) / count,
                avg_score=sum(item.score for item in mode_results) / count,
            )
        )
    return summaries


def run_sort_key(path: Path) -> tuple[int, str]:
    name = path.parent.name
    if name.startswith("baseline-"):
        suffix = name.removeprefix("baseline-")
        if suffix.isdigit():
            return (int(suffix), name)
    return (10_000, name)


def parse_history(scoreboard_path: Path) -> RunHistory | None:
    lines = scoreboard_path.read_text().splitlines()
    marker = "## Mode Summary"
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
        if len(parts) < 5:
            continue
        mode = parts[0]
        score = float(parts[4])
        if mode == "quick":
            quick_score = score
        elif mode == "deep":
            deep_score = score

    return RunHistory(run_name=scoreboard_path.parent.name, quick_score=quick_score, deep_score=deep_score)


def collect_history(repo_root: Path, limit: int = 5) -> list[RunHistory]:
    history: list[RunHistory] = []
    for scoreboard_path in sorted((repo_root / "benchmarks" / "runs").glob("*/scoreboard.md"), key=run_sort_key):
        parsed = parse_history(scoreboard_path)
        if parsed is not None:
            history.append(parsed)
    return history[-limit:]


def render_summary_table(x: int, y: int, width: int, summaries: list[ModeSummary]) -> list[str]:
    rows = len(summaries)
    height = 46 + TABLE_HEADER_HEIGHT + (rows * ROW_HEIGHT)
    svg = [
        rect(x, y, width, height),
        text(x + 18, y + 28, "Current Mode Summary", size=18, weight="700"),
        rect(x + 12, y + 46, width - 24, TABLE_HEADER_HEIGHT, fill=HEADER_BG, radius=8),
    ]

    columns = [("Mode", 18), ("Precision", 120), ("Recall", 240), ("Avg Score", 340)]
    for title, offset in columns:
        svg.append(text(x + offset, y + 68, title, size=13, weight="600", fill=MUTED))

    row_y = y + 46 + TABLE_HEADER_HEIGHT
    for index, summary in enumerate(summaries):
        fill = ROW_ALT if index % 2 == 0 else BACKGROUND
        svg.append(rect(x + 12, row_y, width - 24, ROW_HEIGHT, fill=fill, radius=8))
        svg.extend(
            [
                text(x + 18, row_y + 22, summary.mode.upper(), size=14, weight="600", mono=True),
                text(x + 120, row_y + 22, pct(summary.avg_precision), size=14, mono=True),
                text(x + 240, row_y + 22, pct(summary.avg_recall), size=14, mono=True),
                text(x + 340, row_y + 22, f"{summary.avg_score:.2f}", size=14, weight="700", fill=score_fill(summary.avg_score), mono=True),
            ]
        )
        row_y += ROW_HEIGHT
    return svg


def render_history_table(x: int, y: int, width: int, history: list[RunHistory], current_run: str) -> list[str]:
    rows = len(history)
    height = 46 + TABLE_HEADER_HEIGHT + (rows * ROW_HEIGHT)
    svg = [
        rect(x, y, width, height),
        text(x + 18, y + 28, "Baseline History", size=18, weight="700"),
        rect(x + 12, y + 46, width - 24, TABLE_HEADER_HEIGHT, fill=HEADER_BG, radius=8),
    ]

    columns = [("Run", 18), ("Quick Avg", 150), ("Deep Avg", 280)]
    for title, offset in columns:
        svg.append(text(x + offset, y + 68, title, size=13, weight="600", fill=MUTED))

    row_y = y + 46 + TABLE_HEADER_HEIGHT
    for index, item in enumerate(history):
        fill = ROW_ALT if index % 2 == 0 else BACKGROUND
        border = ACCENT if item.run_name == current_run else BORDER
        svg.append(rect(x + 12, row_y, width - 24, ROW_HEIGHT, fill=fill, stroke=border, radius=8))
        svg.extend(
            [
                text(x + 18, row_y + 22, item.run_name, size=14, weight="600", mono=True),
                text(x + 150, row_y + 22, f"{item.quick_score:.2f}" if item.quick_score is not None else "-", size=14, fill=score_fill(item.quick_score or 0.0), mono=True),
                text(x + 280, row_y + 22, f"{item.deep_score:.2f}" if item.deep_score is not None else "-", size=14, fill=score_fill(item.deep_score or 0.0), mono=True),
            ]
        )
        row_y += ROW_HEIGHT
    return svg


def render_case_table(x: int, y: int, width: int, results: list[score_suite.CaseResult]) -> list[str]:
    rows = len(results)
    height = 46 + TABLE_HEADER_HEIGHT + (rows * ROW_HEIGHT)
    svg = [
        rect(x, y, width, height),
        text(x + 18, y + 28, "Current Run Case Breakdown", size=18, weight="700"),
        rect(x + 12, y + 46, width - 24, TABLE_HEADER_HEIGHT, fill=HEADER_BG, radius=8),
    ]

    columns = [
        ("Mode", 18),
        ("Case", 98),
        ("Matched", 385),
        ("Extra", 485),
        ("Precision", 565),
        ("Recall", 665),
        ("Severity", 760),
        ("CWE", 860),
        ("Score", 940),
    ]
    for title, offset in columns:
        svg.append(text(x + offset, y + 68, title, size=13, weight="600", fill=MUTED))

    row_y = y + 46 + TABLE_HEADER_HEIGHT
    for index, result in enumerate(results):
        fill = ROW_ALT if index % 2 == 0 else BACKGROUND
        svg.append(rect(x + 12, row_y, width - 24, ROW_HEIGHT, fill=fill, radius=8))
        svg.extend(
            [
                text(x + 18, row_y + 22, result.mode, size=14, mono=True),
                text(x + 98, row_y + 22, result.case_id, size=14, mono=True),
                text(x + 385, row_y + 22, f"{result.matched}/{result.expected}", size=14, mono=True),
                text(x + 485, row_y + 22, str(result.extra), size=14, fill=score_fill(100.0 if result.extra == 0 else 0.0), mono=True),
                text(x + 565, row_y + 22, pct(result.precision), size=14, mono=True),
                text(x + 665, row_y + 22, pct(result.recall), size=14, mono=True),
                text(x + 760, row_y + 22, pct(result.severity_accuracy), size=14, mono=True),
                text(x + 860, row_y + 22, pct(result.cwe_accuracy), size=14, mono=True),
                text(x + 940, row_y + 22, f"{result.score:.2f}", size=14, weight="700", fill=score_fill(result.score), mono=True),
            ]
        )
        row_y += ROW_HEIGHT
    return svg


def render_svg(results: list[score_suite.CaseResult], run_name: str) -> str:
    repo_root = Path(__file__).resolve().parents[2]
    summaries = summarize_modes(results)
    history = collect_history(repo_root)

    summary_height = 46 + TABLE_HEADER_HEIGHT + (len(summaries) * ROW_HEIGHT)
    history_height = 46 + TABLE_HEADER_HEIGHT + (len(history) * ROW_HEIGHT)
    case_height = 46 + TABLE_HEADER_HEIGHT + (len(results) * ROW_HEIGHT)
    upper_height = max(summary_height, history_height)
    total_height = PADDING + HEADER_HEIGHT + SECTION_GAP + upper_height + SECTION_GAP + case_height + PADDING

    left_width = 560
    right_width = WIDTH - (PADDING * 2) - left_width - 16
    header_width = WIDTH - (PADDING * 2)

    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{total_height}" viewBox="0 0 {WIDTH} {total_height}" role="img" aria-label="agent-rock benchmark scoreboard">',
        rect(0, 0, WIDTH, total_height, fill=BACKGROUND, stroke=BACKGROUND, radius=0),
        rect(PADDING, PADDING, header_width, HEADER_HEIGHT, fill=HEADER_BG),
        text(PADDING + 22, PADDING + 34, "agent-rock benchmark snapshot", size=28, weight="700"),
        text(PADDING + 22, PADDING + 60, "Serious benchmark view for GitHub: current run, recent baselines, and case-level breakdown.", size=15, fill=MUTED),
        text(PADDING + 22, PADDING + 82, f"Latest run: {run_name}", size=14, fill=ACCENT, weight="600", mono=True),
        text(WIDTH - 280, PADDING + 82, f"Seed suite: {len(results)} checks", size=14, fill=MUTED, mono=True),
    ]

    upper_y = PADDING + HEADER_HEIGHT + SECTION_GAP
    svg.extend(render_summary_table(PADDING, upper_y, left_width, summaries))
    svg.extend(render_history_table(PADDING + left_width + 16, upper_y, right_width, history, run_name))

    case_y = upper_y + upper_height + SECTION_GAP
    svg.extend(render_case_table(PADDING, case_y, header_width, results))

    svg.extend(
        [
            text(PADDING, total_height - 12, "Generated from committed benchmark runs in benchmarks/runs/", size=12, fill=MUTED),
            "</svg>",
        ]
    )
    return "\n".join(svg) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a benchmark scoreboard SVG.")
    parser.add_argument("--results-dir", required=True, help="Directory containing quick/ and deep/ results")
    parser.add_argument("--out", required=True, help="Output SVG path")
    parser.add_argument("--run-name", required=True, help="Benchmark run name label")
    args = parser.parse_args()

    results_dir = Path(args.results_dir).resolve()
    out_path = Path(args.out).resolve()

    results = collect_results(results_dir)
    svg = render_svg(results, args.run_name)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg)
    print(f"Wrote scoreboard SVG to {out_path}")


if __name__ == "__main__":
    main()
