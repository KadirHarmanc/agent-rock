# agent-rock TODO

## Reliability

- [ ] Build a fixture repo suite with intentionally vulnerable sample apps across major stacks.
- [ ] Add `expected-findings.md` or equivalent assertions for each fixture repo.
- [ ] Measure true positives, false positives, and missed findings on every iteration.
- [x] Add partially deterministic helpers for scope resolution, exclude handling, tech stack detection, finding tables, and CWE mapping.
- [x] Add a `confidence` field to each finding in the generated report.
- [x] Tighten severity scoring using exploit path, required privileges, public exposure, and blast radius.
- [x] Mirror the evidence standard in the report template so "missing control" findings require concrete proof.

## Coverage

- [x] Split framework-specific guidance into focused reference files such as Express, Django, Spring, Rails, and Laravel.
- [x] Strengthen dependency audit fallbacks for missing lockfiles, broad version ranges, Git dependencies, postinstall hooks, and unpinned CI actions.
- [x] Add placeholder suppression rules for secret detection to ignore obvious examples and fixtures.
- [x] Expand stack detection and audit heuristics where current coverage is shallow or noisy.

## Product

- [x] Add `quick` and `deep` audit modes for different repo sizes and time budgets.
- [x] Generate both human-readable Markdown and machine-readable JSON output.
- [x] Keep remediation output tightly scoped to verified findings only.
- [x] Document known limitations such as runtime-only issues, business logic bugs, and infra controls outside the repo.

## Repo Hygiene

- [x] Remove `.DS_Store` files from the skill package and keep them out of future copies.
