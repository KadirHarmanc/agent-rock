# Finding Normalization Rules

Use this file during reporting to keep finding structure and wording consistent across Markdown and JSON output.

## Ordering

1. Sort findings by severity: Critical, High, Medium, Low, Info.
2. Within the same severity, sort by confidence: High, Medium, Low.
3. Within the same severity and confidence, sort by likely exploitability and blast radius.

## IDs

- Use `F-001`, `F-002`, `F-003`, and so on.
- Use the same ID in Markdown and JSON.
- Do not renumber findings differently between outputs.
- Use `H-001`, `H-002`, `H-003`, and so on for `hardening_observations`.

## Finding Classes

- `findings`: confirmed vulnerabilities only
- `hardening_observations`: evidence-backed defense-in-depth or configuration concerns that did not clear the confirmed finding bar
- Do not pad `findings` with generic hygiene notes just to make the report feel complete.
- Do not count `hardening_observations` in severity totals or the overall assessment.

## Titles

- Keep titles short and concrete.
- Prefer the verified root cause plus the affected surface.
- Good: `Missing Authorization Check on Admin User Export Route`
- Good: `User-Controlled URL Reaches Internal HTTP Client`
- Avoid vague titles such as `Security Issue` or `Potential Vulnerability`

## Confidence

- `High`: direct code or config evidence with clear exploit path
- `Medium`: strong evidence but some runtime assumptions remain
- `Low`: evidence-backed concern that still depends on important inferred behavior

## Severity

Apply the rubric from `SKILL.md` consistently. Do not inflate severity to compensate for weak confidence.
If confidence is low, the issue may still be real, but the severity should reflect the verified exploit path.

## Evidence

- Show only the minimum snippet needed to prove the issue.
- Prefer 5 to 20 lines of code or config.
- If a missing control is the issue, explain the entry point and show the exact location where the guard is absent.
- Avoid duplicating near-identical snippets across multiple findings unless the repetition itself matters.

## Locations

- Choose one primary `location` for each finding.
- If the verified root cause spans multiple files, keep the most causally important file as the primary location.
- Put additional supporting files in `related_locations`.
- Good examples:
- Controller as primary location with model in `related_locations` when both are required to prove mass assignment.
- Route as primary location with middleware definition in `related_locations` when the missing guard is the issue.

## Remediation

- Tie the fix to the verified root cause.
- Prefer a one-paragraph fix summary plus a compact corrected example.
- Do not add unrelated hardening advice.

## Clean Categories

- List a category as clean only when it was actually reviewed.
- If `quick` mode skipped deeper work in a category, note that in the executive summary or methodology instead of claiming the category passed clean.

## JSON Consistency

- Keep Markdown and JSON counts identical.
- Ensure every Markdown finding has a matching JSON object and vice versa.
- Use the same severity, confidence, CWE, location, and recommendation in both outputs.
- Keep `hardening_observations` aligned across Markdown and JSON too.
