#!/usr/bin/env python3
"""Score a benchmark run directory against seeded benchmark manifests."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SEVERITY_ORDER = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1, "Info": 0}


@dataclass
class CaseResult:
    mode: str
    case_id: str
    expected: int
    matched: int
    missed: int
    extra: int
    negative_hits: int
    severity_hits: int
    cwe_hits: int
    precision: float
    recall: float
    severity_accuracy: float
    cwe_accuracy: float
    score: float


def normalize_cwe(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return value.get("id")
    if isinstance(value, str):
        return value.strip() or None
    return None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).lower().split())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def endswith_path(actual: str | None, expected: str) -> bool:
    if not actual:
        return False
    normalized = actual.replace("\\", "/")
    return normalized.endswith(expected)


def accepted_values(expected: dict[str, Any], plural_key: str, singular_key: str) -> list[str]:
    values = expected.get(plural_key)
    if isinstance(values, list):
        return [str(value) for value in values if value]
    value = expected.get(singular_key)
    if value:
        return [str(value)]
    return []


def finding_locations(finding: dict[str, Any]) -> list[str]:
    locations: list[str] = []

    def add_location(value: Any) -> None:
        if isinstance(value, str) and value and value not in locations:
            locations.append(value)

    location = finding.get("location", {})
    if isinstance(location, dict):
        add_location(location.get("file"))

    related_locations = finding.get("related_locations", [])
    if isinstance(related_locations, list):
        for related in related_locations:
            if isinstance(related, dict):
                add_location(related.get("file"))
            else:
                add_location(related)

    return locations


def finding_text_blob(finding: dict[str, Any]) -> str:
    parts = [
        normalize_text(finding.get("title")),
        normalize_text(finding.get("description")),
    ]
    evidence = finding.get("evidence", {})
    if isinstance(evidence, dict):
        parts.append(normalize_text(evidence.get("summary")))
        parts.append(normalize_text(evidence.get("snippet")))
    return " ".join(part for part in parts if part)


def token_hits(text: str, tokens: list[str]) -> int:
    if not tokens:
        return 0
    normalized = normalize_text(text)
    return sum(1 for token in tokens if normalize_text(token) in normalized)


def score_match(finding: dict[str, Any], expected: dict[str, Any]) -> tuple[int, bool, bool] | None:
    accepted_locations = accepted_values(expected, "accepted_locations", "file")
    accepted_cwes = accepted_values(expected, "accepted_cwes", "cwe")
    accepted_severities = accepted_values(expected, "accepted_severities", "severity")
    match_hints = expected.get("match_hints", {})
    title_tokens = match_hints.get("title_contains", []) if isinstance(match_hints, dict) else []
    evidence_tokens = match_hints.get("evidence_contains", []) if isinstance(match_hints, dict) else []

    locations = finding_locations(finding)
    location_hit = any(
        endswith_path(location, accepted_location)
        for location in locations
        for accepted_location in accepted_locations
    )
    cwe_hit = normalize_cwe(finding.get("cwe")) in accepted_cwes if accepted_cwes else False
    severity_hit = finding.get("severity") in accepted_severities if accepted_severities else False

    title_text = normalize_text(finding.get("title"))
    blob = finding_text_blob(finding)
    title_hits = token_hits(title_text, title_tokens)
    evidence_hits = token_hits(blob, evidence_tokens)

    score = 0
    if location_hit:
        score += 100
    if cwe_hit:
        score += 25
    if severity_hit:
        score += 10
    score += title_hits * 6
    score += evidence_hits * 3

    if score == 0:
        return None
    return score, severity_hit, cwe_hit


def score_case(case_manifest: dict[str, Any], report: dict[str, Any], mode: str) -> CaseResult:
    findings = report.get("findings", [])
    unmatched = list(range(len(findings)))
    matched_findings: list[dict[str, Any]] = []
    severity_hits = 0
    cwe_hits = 0

    for expected in case_manifest["expected_findings"]:
        match_index = None
        best_score = -1
        best_severity_hit = False
        best_cwe_hit = False
        for idx in unmatched:
            finding = findings[idx]
            match_result = score_match(finding, expected)
            if match_result is None:
                continue
            candidate_score, candidate_severity_hit, candidate_cwe_hit = match_result
            if candidate_score > best_score:
                best_score = candidate_score
                best_severity_hit = candidate_severity_hit
                best_cwe_hit = candidate_cwe_hit
                match_index = idx
        if match_index is not None:
            matched_findings.append(findings[match_index])
            if best_severity_hit:
                severity_hits += 1
            if best_cwe_hit:
                cwe_hits += 1
            unmatched.remove(match_index)

    negative_hits = 0
    for idx in list(unmatched):
        finding = findings[idx]
        for negative in case_manifest.get("negative_controls", []):
            if any(endswith_path(location, negative["file"]) for location in finding_locations(finding)):
                negative_hits += 1
                break

    expected_count = len(case_manifest["expected_findings"])
    matched_count = len(matched_findings)
    missed_count = expected_count - matched_count
    extra_count = len(unmatched)

    precision = matched_count / (matched_count + extra_count) if (matched_count + extra_count) else 0.0
    recall = matched_count / expected_count if expected_count else 0.0
    severity_accuracy = severity_hits / matched_count if matched_count else 0.0
    cwe_accuracy = cwe_hits / matched_count if matched_count else 0.0
    score = round((recall * 50.0) + (precision * 30.0) + (severity_accuracy * 10.0) + (cwe_accuracy * 10.0), 2)

    return CaseResult(
        mode=mode,
        case_id=case_manifest["id"],
        expected=expected_count,
        matched=matched_count,
        missed=missed_count,
        extra=extra_count,
        negative_hits=negative_hits,
        severity_hits=severity_hits,
        cwe_hits=cwe_hits,
        precision=precision,
        recall=recall,
        severity_accuracy=severity_accuracy,
        cwe_accuracy=cwe_accuracy,
        score=score,
    )


def render_markdown(results: list[CaseResult]) -> str:
    lines = [
        "# agent-rock Benchmark Scoreboard",
        "",
        "| Mode | Case | Expected | Matched | Missed | Extra | Neg FP | Precision | Recall | Severity | CWE | Score |",
        "|------|------|----------|---------|--------|-------|--------|-----------|--------|----------|-----|-------|",
    ]

    for result in results:
        lines.append(
            "| {mode} | {case_id} | {expected} | {matched} | {missed} | {extra} | {negative_hits} | "
            "{precision:.2f} | {recall:.2f} | {severity_accuracy:.2f} | {cwe_accuracy:.2f} | {score:.2f} |".format(
                **result.__dict__
            )
        )

    if results:
        grouped: dict[str, list[CaseResult]] = {}
        for result in results:
            grouped.setdefault(result.mode, []).append(result)

        lines.extend(["", "## Mode Summary", ""])
        lines.append("| Mode | Cases | Avg Precision | Avg Recall | Avg Score |")
        lines.append("|------|-------|---------------|------------|-----------|")

        for mode, mode_results in sorted(grouped.items()):
            count = len(mode_results)
            avg_precision = sum(r.precision for r in mode_results) / count
            avg_recall = sum(r.recall for r in mode_results) / count
            avg_score = sum(r.score for r in mode_results) / count
            lines.append(
                f"| {mode} | {count} | {avg_precision:.2f} | {avg_recall:.2f} | {avg_score:.2f} |"
            )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Score benchmark JSON reports against seeded expectations.")
    parser.add_argument("--results-dir", required=True, help="Directory containing quick/ and deep/ results")
    parser.add_argument("--out", help="Optional markdown output file")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    cases_root = repo_root / "benchmarks" / "cases"
    results_dir = Path(args.results_dir).resolve()

    results: list[CaseResult] = []

    for mode_dir in sorted(p for p in results_dir.iterdir() if p.is_dir()):
        mode = mode_dir.name
        for case_dir in sorted(p for p in cases_root.iterdir() if p.is_dir()):
            manifest = load_json(case_dir / "benchmark.json")
            report_path = mode_dir / manifest["id"] / "security-audit-report.json"
            if not report_path.is_file():
                continue
            report = load_json(report_path)
            results.append(score_case(manifest, report, mode))

    markdown = render_markdown(results)

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown)
        print(f"Wrote scoreboard to {out_path}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
