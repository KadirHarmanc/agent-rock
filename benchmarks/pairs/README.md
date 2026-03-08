# Paired Regression Cases

This directory is for vulnerable/fixed benchmark pairs.

Use this format for:

- historical CVE replay
- internal regression cases
- vulnerable vs patched comparisons on the same app shape

## Layout

```text
benchmarks/pairs/
  <pair-id>/
    pair.json
    vulnerable/
      repo/
        ...
    fixed/
      repo/
        ...
```

## Pair Manifest

Each `pair.json` contains:

- pair metadata such as `id`, `name`, `description`, and `stack`
- a `variants.vulnerable` manifest with expected findings
- a `variants.fixed` manifest that should usually stay clean

The scoring rule is intentionally simple:

- the vulnerable variant should reproduce the expected findings
- the fixed variant should not reproduce them

## Commands

Materialize a pair variant:

```bash
python3 benchmarks/scripts/materialize_pair_case.py \
  --pair express-sqli-auth-regression \
  --variant vulnerable \
  --out /tmp/agent-rock-pairs/express-sqli-auth-regression-vulnerable
```

Score a collected pair run:

```bash
python3 benchmarks/scripts/score_pair_suite.py \
  --results-dir benchmarks/pair-runs/example-run \
  --out benchmarks/pair-runs/example-run/scoreboard.md
```

Launch a full paired replay in Terminal.app:

```bash
python3 benchmarks/scripts/launch_pair_benchmark.py \
  --run-name pair-baseline-1
```

Finalize a paired replay in one step:

```bash
python3 benchmarks/scripts/finalize_pair_run.py \
  --run-name pair-baseline-1 \
  --open
```

## Why This Exists

Normal fixture cases are best for day-to-day regression testing.
Paired cases are the next layer: they prove that agent-rock can see a real bug in the vulnerable version
and stop reporting it in the fixed version.
