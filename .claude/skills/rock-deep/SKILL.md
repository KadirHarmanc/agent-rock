---
name: rock-deep
description: >
  Exhaustive security audit for any codebase. Use when the user wants the most
  complete static security review, a deeper vulnerability assessment, or a more
  thorough follow-up after triage. Produces the same evidence-backed security
  report format as agent-rock, but always runs in deep mode.
argument-hint: "[target-directory]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Write, Bash(find *), Bash(ls *), Bash(wc *), Bash(git log *), Bash(git diff *), Bash(npm audit *), Bash(yarn audit *), Bash(pnpm audit *), Bash(pip audit *), Bash(pip-audit *), Bash(safety check *), Bash(cargo audit *), Bash(bundle audit *), Bash(bundle-audit *), Bash(composer audit *), Bash(dotnet list *), Bash(go list *), Bash(cat .gitignore)
---

# rock-deep

Read and follow the base workflow from [agent-rock](../agent-rock/SKILL.md).

Override the base workflow with these rules:

- Force the audit mode to `deep`.
- Treat `$ARGUMENTS` only as the target directory.
- If the user wants a faster first pass, tell them to use `rock-quick` instead.
- Keep the same evidence standard, report structure, Markdown output path, JSON output path, and confidence model as the base skill.

Use the same references, templates, and focused framework guides from the base `agent-rock` skill directory.
