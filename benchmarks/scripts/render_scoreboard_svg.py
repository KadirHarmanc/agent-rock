#!/usr/bin/env python3
"""Render a benchmark scoreboard SVG suitable for embedding in GitHub README files."""

from __future__ import annotations

import argparse
import html
from pathlib import Path

import score_suite


WIDTH = 1200
PADDING_X = 32
HEADER_HEIGHT = 108
ROW_HEIGHT = 38
SECTION_GAP = 28
SUMMARY_CARD_HEIGHT = 92
BACKGROUND = "#0b1020"
PANEL = "#121a2f"
PANEL_ALT = "#0f1730"
TEXT = "#e6edf7"
MUTED = "#91a0bd"
GRID = "#25314d"
ACCENT = "#5eead4"


def score_color(score: float) -> str:
    if score >= 95:
        return "#2ecc71"
    if score >= 85:
        return "#f1c40f"
    if score >= 70:
        return "#e67e22"
    return "#e74c3c"


def pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def render_text(x: int, y: int, value: str, size: int = 18, weight: str = "400", fill: str = TEXT) -> str:
    safe = html.escape(value)
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
        f'font-size="{size}" font-weight="{weight}">{safe}</text>'
    )


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


def render_svg(results: list[score_suite.CaseResult], run_name: str) -> str:
    grouped: dict[str, list[score_suite.CaseResult]] = {}
    for result in results:
        grouped.setdefault(result.mode, []).append(result)

    summary_modes = sorted(grouped.items())
    table_rows = len(results)
    total_height = (
        HEADER_HEIGHT
        + PADDING_X
        + SUMMARY_CARD_HEIGHT
        + SECTION_GAP
        + 56
        + ((table_rows + 1) * ROW_HEIGHT)
        + PADDING_X
    )

    summary_width = (WIDTH - (PADDING_X * 2) - 16) // 2
    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{total_height}" viewBox="0 0 {WIDTH} {total_height}" role="img" aria-label="agent-rock benchmark scoreboard">',
        "<defs>",
        '<linearGradient id="hero" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0%" stop-color="#13203b" />',
        '<stop offset="100%" stop-color="#0f766e" />',
        "</linearGradient>",
        "</defs>",
        f'<rect width="{WIDTH}" height="{total_height}" fill="{BACKGROUND}" rx="24" />',
        f'<rect x="{PADDING_X}" y="{PADDING_X}" width="{WIDTH - (PADDING_X * 2)}" height="{HEADER_HEIGHT}" fill="url(#hero)" rx="20" />',
        render_text(PADDING_X + 28, PADDING_X + 42, "agent-rock benchmark", size=28, weight="700"),
        render_text(PADDING_X + 28, PADDING_X + 74, f"Latest committed run: {run_name}", size=16, fill="#d9fff8"),
        render_text(WIDTH - 260, PADDING_X + 42, "GitHub-ready SVG", size=18, weight="700", fill="#d9fff8"),
        render_text(WIDTH - 260, PADDING_X + 72, "Embed this in README.md", size=14, fill="#d9fff8"),
    ]

    summary_y = PADDING_X + HEADER_HEIGHT + 20
    for idx, (mode, mode_results) in enumerate(summary_modes):
        x = PADDING_X + idx * (summary_width + 16)
        avg_precision = sum(item.precision for item in mode_results) / len(mode_results)
        avg_recall = sum(item.recall for item in mode_results) / len(mode_results)
        avg_score = sum(item.score for item in mode_results) / len(mode_results)

        svg.extend(
            [
                f'<rect x="{x}" y="{summary_y}" width="{summary_width}" height="{SUMMARY_CARD_HEIGHT}" fill="{PANEL}" stroke="{GRID}" stroke-width="1" rx="18" />',
                render_text(x + 20, summary_y + 30, mode.upper(), size=22, weight="700"),
                render_text(x + 20, summary_y + 56, f"Precision {pct(avg_precision)}", size=16, fill=MUTED),
                render_text(x + 200, summary_y + 56, f"Recall {pct(avg_recall)}", size=16, fill=MUTED),
                render_text(x + 20, summary_y + 82, f"Avg Score {avg_score:.2f}", size=16, fill=score_color(avg_score), weight="700"),
            ]
        )

    table_y = summary_y + SUMMARY_CARD_HEIGHT + SECTION_GAP
    svg.extend(
        [
            render_text(PADDING_X, table_y, "Case Breakdown", size=22, weight="700"),
            f'<rect x="{PADDING_X}" y="{table_y + 18}" width="{WIDTH - (PADDING_X * 2)}" height="{ROW_HEIGHT}" fill="{PANEL}" stroke="{GRID}" stroke-width="1" rx="12" />',
        ]
    )

    columns = [
        ("Mode", 28),
        ("Case", 120),
        ("Matched", 430),
        ("Extra", 545),
        ("Precision", 645),
        ("Recall", 775),
        ("Severity", 880),
        ("CWE", 985),
        ("Score", 1070),
    ]
    for title, x in columns:
        svg.append(render_text(PADDING_X + x, table_y + 44, title, size=15, weight="700", fill=MUTED))

    row_y = table_y + 18 + ROW_HEIGHT
    for index, result in enumerate(results):
        fill = PANEL_ALT if index % 2 == 0 else PANEL
        svg.append(
            f'<rect x="{PADDING_X}" y="{row_y}" width="{WIDTH - (PADDING_X * 2)}" height="{ROW_HEIGHT}" fill="{fill}" stroke="{GRID}" stroke-width="1" rx="10" />'
        )
        svg.extend(
            [
                render_text(PADDING_X + 28, row_y + 25, result.mode, size=15),
                render_text(PADDING_X + 120, row_y + 25, result.case_id, size=15),
                render_text(PADDING_X + 430, row_y + 25, f"{result.matched}/{result.expected}", size=15),
                render_text(PADDING_X + 545, row_y + 25, str(result.extra), size=15, fill=score_color(100.0 if result.extra == 0 else max(0.0, 100 - result.extra * 25))),
                render_text(PADDING_X + 645, row_y + 25, pct(result.precision), size=15),
                render_text(PADDING_X + 775, row_y + 25, pct(result.recall), size=15),
                render_text(PADDING_X + 880, row_y + 25, pct(result.severity_accuracy), size=15),
                render_text(PADDING_X + 985, row_y + 25, pct(result.cwe_accuracy), size=15),
                render_text(PADDING_X + 1070, row_y + 25, f"{result.score:.2f}", size=15, weight="700", fill=score_color(result.score)),
            ]
        )
        row_y += ROW_HEIGHT

    svg.extend(
        [
            render_text(PADDING_X, total_height - 20, "Generated from benchmarks/scripts/render_scoreboard_svg.py", size=12, fill=MUTED),
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
