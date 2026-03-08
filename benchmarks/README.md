# agent-rock Benchmark

This directory contains a small but scalable benchmark harness for agent-rock.
The initial goal is not to mimic every real application shape. The goal is to
measure change over time with repeatable seeded cases, comparable JSON reports,
and a simple scoreboard.

Important framing:

- today this benchmark is strongest as an internal regression exam
- a perfect score means the current seeded suite is saturated, not that the product is "done"
- the benchmark validity roadmap lives in [VALIDITY.md](/Users/emirhanakdeniz/Desktop/agent-rock/benchmarks/VALIDITY.md)

## Layout

```text
benchmarks/
  cases/
    <case-id>/
      benchmark.json
      repo/
        ...
  pairs/
    <pair-id>/
      pair.json
      vulnerable/
        repo/
          ...
      fixed/
        repo/
          ...
  external/
    README.md
  scripts/
    finalize_run.py
    finalize_pair_run.py
    launch_parallel_benchmark.py
    launch_pair_benchmark.py
    collect_results.py
    collect_pair_results.py
    materialize_case.py
    materialize_pair_case.py
    render_scoreboard_svg.py
    render_progress_report.py
    score_pair_suite.py
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

Paired cases under `pairs/` are for vulnerable vs fixed replay. They are best for proving that
agent-rock both detects the vulnerable version and stops reporting the issue in the fixed version.

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

Materialize a paired vulnerable/fixed variant:

```bash
python3 benchmarks/scripts/materialize_pair_case.py \
  --pair express-sqli-auth-regression \
  --variant vulnerable \
  --out /tmp/agent-rock-pairs/express-sqli-auth-regression-vulnerable
```

Score a full run:

```bash
python3 benchmarks/scripts/score_suite.py \
  --results-dir benchmarks/runs/2026-03-08-initial \
  --out benchmarks/runs/2026-03-08-initial/scoreboard.md
```

Score a paired replay run:

```bash
python3 benchmarks/scripts/score_pair_suite.py \
  --results-dir benchmarks/pair-runs/example-run \
  --out benchmarks/pair-runs/example-run/scoreboard.md
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
It also refreshes `benchmarks/progress.md`, which is the single best file for answering
"did the score actually improve after this change?"

Launch a paired vulnerable/fixed replay in Terminal.app:

```bash
python3 benchmarks/scripts/launch_pair_benchmark.py \
  --run-name pair-baseline-1
```

Collect finished paired reports from the temp workdirs:

```bash
python3 benchmarks/scripts/collect_pair_results.py \
  --run-name pair-baseline-1
```

Finalize a paired run in one step:

```bash
python3 benchmarks/scripts/finalize_pair_run.py \
  --run-name pair-baseline-1 \
  --open
```

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
- `express-safe-twin`
- `express-monorepo-noisy`
- `django-invoices-basic`
- `django-config-fragment`
- `laravel-preview-basic`

## Paired Regression Seed

The first paired regression seed is:

- `express-sqli-auth-regression`

These are designed to be expanded later with:

- more stacks
- more safe twin repos
- more noisy monorepos
- generated file traps
- framework-specific tricky negatives

## Important Note

`agent-rock` excludes the `benchmarks/` directory during normal scans so the benchmark harness
does not pollute real audits. Because of that, materialize runnable benchmark repos outside the
repository tree, for example under `/tmp/agent-rock-bench/`, and run Claude Code there.

The launcher opens real interactive Claude Code sessions and injects `/rock-quick` or `/rock-deep`
after startup. It does not use `claude -p`, because the benchmark should exercise the actual skill flow.

The paired launcher uses the same real interactive skill flow, but materializes both `vulnerable` and
`fixed` variants so you can verify that agent-rock finds the bug before the patch and stays quiet after it.
