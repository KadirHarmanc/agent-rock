# Benchmark Validity

This file exists to answer a harder question than "what was the latest score?"

The hard question is:

**Is this benchmark a good exam, or did agent-rock just memorize the current worksheet?**

## What The Current Benchmark Is Good For

Today the benchmark is strongest as a **regression benchmark**.

That means it is good at answering:

- did a recent change improve or hurt known seeded cases
- did false positives go down on known safe-twin fixtures
- does agent-rock still find the vulnerable variant and stay quiet on the fixed variant

It is **not yet strong enough** to claim broad real-world superiority on its own.

## What A Good Benchmark Must Do

A serious benchmark for agent-rock should satisfy all of these:

- **Discrimination**: good versions should score higher than worse versions
- **Headroom**: it should be hard to hit `100.00` unless the skill is genuinely strong
- **Realism**: at least part of the suite should resemble real project structure and bug shape
- **False-positive pressure**: safe but suspicious repos should stay clean
- **Replay value**: vulnerable versions should fail and fixed versions should pass
- **Holdout value**: some cases should remain unseen during day-to-day prompt tuning

## How To Read Scores Today

- A `100.00` on the core fixture suite means: agent-rock solved the current seeded regression sheet.
- It does **not** mean: agent-rock is finished or generally best-in-class.
- A high pair score is stronger evidence than a high core-fixture score, because replay cases are closer to real regression behavior.

So the current benchmark should be read like this:

- `core fixture score` = daily regression health
- `pair replay score` = stronger proof that fixes suppress findings and bugs reproduce
- `future holdout/external score` = the real test of generalization

## Signs The Benchmark Is Becoming Too Easy

Treat the current suite as saturated when one or more of these happen:

- the latest core score reaches `100.00`
- multiple consecutive runs stay near-perfect
- progress comes mostly from benchmark-aware tuning rather than broader capability
- new tricky negatives or paired replays immediately reveal blind spots anyway

When that happens, the right move is not to celebrate the score alone. The right move is to expand the exam.

## What We Still Need Before Public Claims

Before using benchmark results as a serious public proof point, the suite should add:

- more safe-twin repos
- config-fragment clean cases
- more multi-file and compound-vulnerability cases
- noisy monorepos and generated-file traps
- external historical-CVE replay pairs
- a holdout set that is not used during active tuning

## Current Position

Current honest position:

- the benchmark is already useful and meaningful
- it is strong enough for internal regression tracking
- it is not yet broad enough to be the final public exam
- `100.00` on the core suite means "time to make the exam harder"
