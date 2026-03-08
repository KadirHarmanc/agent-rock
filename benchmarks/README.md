# agent-rock Benchmark

This directory contains a small but scalable benchmark harness for agent-rock.
The initial goal is not to mimic every real application shape. The goal is to
measure change over time with repeatable seeded cases, comparable JSON reports,
and a simple scoreboard.

## Layout

```text
benchmarks/
  cases/
    <case-id>/
      benchmark.json
      repo/
        ...
  scripts/
    finalize_run.py
    launch_parallel_benchmark.py
    collect_results.py
    materialize_case.py
    render_scoreboard_svg.py
    score_suite.py
```

## Core Idea

Each case contains:

- a tracked mini-repo under `repo/`
- a `benchmark.json` manifest with expected findings
- negative-control files that should stay clean
- a local copy of the benchmarked skills when materialized, so the case can run outside this repo

Run the fixture in Claude Code with the actual slash commands `rock-quick` or `rock-deep`,
then collect `security-audit-report.json` and score the results with the harness.

## Recommended Results Layout

Store Claude Code outputs outside git under:

```text
benchmarks/runs/<run-name>/<mode>/<case-id>/security-audit-report.json
```

Example:

```text
benchmarks/runs/2026-03-08-initial/quick/express-api-basic/security-audit-report.json
benchmarks/runs/2026-03-08-initial/deep/express-api-basic/security-audit-report.json
```

## Workflow

1. Materialize one case into a temp working directory.
2. Open that temp directory in Claude Code.
3. Run `/rock-quick` or `/rock-deep`.
4. Let the generated reports land in the temp workdirs.
5. Collect the finished reports into the `benchmarks/runs/...` layout.
6. Score the run and render a markdown leaderboard.

## Commands

Materialize a case:

```bash
python3 benchmarks/scripts/materialize_case.py \
  --case express-api-basic \
  --out /tmp/agent-rock-bench/express-api-basic
```

Score a full run:

```bash
python3 benchmarks/scripts/score_suite.py \
  --results-dir benchmarks/runs/2026-03-08-initial \
  --out benchmarks/runs/2026-03-08-initial/scoreboard.md
```

Launch a full parallel run in Terminal.app:

```bash
python3 benchmarks/scripts/launch_parallel_benchmark.py \
  --run-name baseline-1
```

Collect finished reports from the temp workdirs:

```bash
python3 benchmarks/scripts/collect_results.py \
  --run-name baseline-1
```

Finalize a run in one step:

```bash
python3 benchmarks/scripts/finalize_run.py \
  --run-name baseline-1 \
  --open
```

This also refreshes a tracked GitHub-friendly SVG at `benchmarks/latest-scoreboard.svg`.

## Metrics

The scorer reports:

- expected findings
- matched findings
- missed findings
- extra findings
- negative-control hits
- precision
- recall
- severity accuracy
- CWE accuracy
- weighted score

The scorer supports semantic matching hints from each `benchmark.json` manifest:

- accepted alternate locations for multi-file root causes
- accepted alternate CWEs where multiple taxonomies are reasonable
- accepted alternate severities where calibration is debatable
- title and evidence text hints to distinguish multiple findings in the same file

## Seed Cases

The starter suite is intentionally small:

- `express-api-basic`
- `django-invoices-basic`
- `laravel-preview-basic`

These are designed to be expanded later with:

- more stacks
- safe twin repos
- noisy monorepos
- generated file traps
- framework-specific tricky negatives

## Important Note

`agent-rock` excludes the `benchmarks/` directory during normal scans so the benchmark harness
does not pollute real audits. Because of that, materialize runnable benchmark repos outside the
repository tree, for example under `/tmp/agent-rock-bench/`, and run Claude Code there.

The launcher opens real interactive Claude Code sessions and injects `/rock-quick` or `/rock-deep`
after startup. It does not use `claude -p`, because the benchmark should exercise the actual skill flow.
