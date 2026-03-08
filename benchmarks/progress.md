# agent-rock Benchmark Progress

This report exists to answer one question quickly: is agent-rock getting better or not?

## Core Fixture Benchmarks

| Run | Quick | Deep | Overall | Delta |
|-----|-------|------|---------|-------|
| baseline-2 | 96.67 | 84.00 | 90.34 | - |
| baseline-3 | 98.89 | 94.17 | 96.53 | +6.19 |
| baseline-4 | 100.00 | 100.00 | 100.00 | +3.47 |
| baseline-5-newcases | 42.50 | 42.50 | 42.50 | -57.50 |

Latest: `baseline-5-newcases` scored `42.50`. Best so far: `baseline-4` with `100.00`.

## Paired Regression Benchmarks

| Run | Quick | Deep | Overall | Delta |
|-----|-------|------|---------|-------|
| pair-baseline-1 | 91.66 | 100.00 | 95.83 | - |

Latest: `pair-baseline-1` scored `95.83`. Best so far: `pair-baseline-1` with `95.83`.

## Current Read

Core suite latest score: `42.50` on `baseline-5-newcases`.
Paired regression latest score: `95.83` on `pair-baseline-1`.

Interpretation:
- Core score shows how well agent-rock performs on the seeded fixture suite.
- Pair score shows whether it finds the vulnerable version and stays quiet on the fixed version.
- If core rises but pair stalls, the skill is improving on fixtures but still weak on replay realism.
- If pair rises but core stalls, replay handling is improving but general benchmark coverage may be flat.

## Benchmark Health

The core fixture suite still has visible headroom, so score changes here remain highly informative.
Paired replay coverage is still thin. Treat pair results as promising evidence, not final proof.

Use this rule of thumb:
- `100.00` on core fixtures = regression health is excellent.
- `100.00` on core fixtures != the benchmark is complete.
- Once core saturates, the next honest move is to add harder or unseen cases.

