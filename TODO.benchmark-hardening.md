# agent-rock Benchmark Hardening TODO

This roadmap exists to turn the first benchmark runs into concrete product work.
Baseline takeaway: detection is already strong, but calibration and trust still need work.

## Benchmark Signals From `baseline-2`

- [x] Confirmed that seeded recall is strong across the starter suite.
- [x] Confirmed that `quick` currently behaves as the more trustworthy default mode.
- [x] Confirmed that `deep` mixes real exploit paths with hardening and hygiene observations too often.
- [x] Confirmed that the current scorer is too strict for semantic variants and multi-file root causes.

## P0: Trust And Signal Quality

- [x] Split output into `findings` and `hardening_observations`.
- [x] Keep overall assessment and severity counts driven by confirmed `findings` only.
- [ ] Add a stricter promotion rule so absence-only config and dependency leads stay out of `findings` unless exploit-relevant evidence exists.
- [x] Add a clear authentication decision tree.
- [ ] No auth gate on a reachable sensitive route -> authentication exposure.
- [ ] Auth exists but admin/function-level check is missing -> authorization issue.
- [ ] Auth exists but object ownership check is missing -> IDOR/BOLA.
- [x] Standardize multi-file findings with one primary location and secondary evidence locations.
- [ ] Keep `quick` optimized for confirmed exploit paths and leave broader hardening notes to `deep`.

## P1: Benchmark Fairness And Calibration

- [x] Upgrade the scorer from file-only matching to semantic matching using accepted locations, accepted CWEs, accepted severities, and textual hints.
- [x] Allow manifests to define alternate valid locations for multi-file findings.
- [x] Allow manifests to define alternate valid CWE mappings when multiple taxonomies are reasonable.
- [x] Allow manifests to define severity ranges when `High` versus `Critical` is a calibration question rather than a detection failure.
- [ ] Add explicit support for compound findings on the same route or file.
- [ ] Separate detection score from calibration score in the rendered scoreboard.

## P2: Product Hardening

- [ ] Position `/rock-quick` as the default public entry point until `deep` precision improves.
- [ ] Reframe `/rock-deep` as an investigator mode unless the extra noise is reduced.
- [ ] Add repo-level suppressions for known-safe framework patterns and intentional fixture shortcuts.
- [ ] Add trend reporting so each benchmark run can be compared against the previous baseline.
- [ ] Add CI-friendly summary output for benchmark runs.

## Next Benchmark Cases

- [ ] Add safe twin repos that look risky but are actually secure.
- [ ] Add config-fragment fixtures that should not trigger hard failure findings.
- [ ] Add more multi-file root-cause cases.
- [ ] Add noisy monorepos and generated-file trap cases.
