# agent-rock Benchmark Hardening TODO

This roadmap exists to turn the first benchmark runs into concrete product work.
Baseline takeaway: detection is already strong, but calibration and trust still need work.

## Benchmark Signals From `pair-baseline-1`

- [x] Confirmed that the fixed variant stays clean in both `quick` and `deep`.
- [x] Confirmed that `deep` reproduces the full vulnerable finding set on the first paired regression case.
- [x] Confirmed that `quick` can miss a second authorization issue when a stronger exploit path already exists on the same route.

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
- [x] Score clean-case fixtures correctly when zero findings are expected and zero findings are reported.
- [ ] Add explicit support for compound findings on the same route or file.
- [ ] Separate detection score from calibration score in the rendered scoreboard.
- [ ] Add a holdout benchmark layer that is not used during active tuning.

## P2: Product Hardening

- [ ] Position `/rock-quick` as the default public entry point until `deep` precision improves.
- [ ] Reframe `/rock-deep` as an investigator mode unless the extra noise is reduced.
- [ ] Add repo-level suppressions for known-safe framework patterns and intentional fixture shortcuts.
- [x] Add trend reporting so each benchmark run can be compared against the previous baseline.
- [ ] Add CI-friendly summary output for benchmark runs.
- [x] Document benchmark validity limits so perfect core scores are not misread as general proof.

## Next Benchmark Cases

- [x] Add a first safe twin repo that looks risky but is actually secure (`express-safe-twin`).
- [x] Add a first paired vulnerable/fixed regression case (`express-sqli-auth-regression`).
- [x] Add a first config-fragment clean case (`django-config-fragment`).
- [x] Add a first noisy monorepo case (`express-monorepo-noisy`).
- [ ] Add more safe twin repos that look risky but are actually secure.
- [ ] Add more config-fragment fixtures that should not trigger hard failure findings.
- [ ] Add more multi-file root-cause cases.
- [ ] Add more noisy monorepos and generated-file trap cases.

## Paired Regression Workflow

- [x] Add a materialized vulnerable/fixed pair format with machine-readable manifests.
- [x] Add paired benchmark scoring for vulnerable recall and fixed cleanliness.
- [x] Add pair launch, collect, and finalize scripts so replay runs are as easy as normal baselines.
- [x] Run and review the first paired baseline (`pair-baseline-1`).
- [ ] Add the first external historical-CVE replay pair.
