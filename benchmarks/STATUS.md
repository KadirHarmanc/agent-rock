# agent-rock Benchmark Status

This is the simplest honest read of where the benchmark stands right now.

## What We Know

- agent-rock improved meaningfully across the first core regression runs
- the old core suite moved from `90.34` to `100.00`
- the first paired vulnerable/fixed replay scored `95.83`
- that means the system is getting better on known cases and is already fairly good at replay-style validation

## What We Do Not Know Yet

- we still cannot say how agent-rock would do on a fresh `100-case` exam
- the current core suite is too small for that claim
- a `100.00` on the old core suite means the current exam is becoming saturated

## Current Benchmark Shape

The benchmark now has:

- multiple seeded vulnerable app fixtures
- clean safe-twin fixtures
- one paired vulnerable/fixed replay
- a progress report that shows run-over-run score changes

The suite was expanded again with harder cases after `baseline-4`.
That means the latest perfect core score belongs to the older, smaller core snapshot.

## What Needs To Happen Next

To make the benchmark feel like a real exam instead of a worksheet, the next steps are:

- rerun the enlarged core suite as a new baseline
- add more clean config-fragment and safe-twin cases
- add more noisy monorepos and generated-file traps
- add more paired vulnerable/fixed replays
- eventually add an external holdout layer that is not used during active tuning

## Practical Reading Rule

- `progress.md` tells us whether agent-rock is improving
- `VALIDITY.md` tells us how much trust to place in the exam itself
- a perfect score is good news, but also a signal that the exam must get harder
