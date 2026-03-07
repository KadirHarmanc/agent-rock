---
name: rock-quick
description: >
  Fast triage security audit for any codebase. Use when the user wants a quick,
  high-signal security scan, rapid vulnerability triage, or a faster first-pass
  security review. Produces the same evidence-backed security report format as
  agent-rock, but always runs in quick mode.
argument-hint: "[target-directory]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Write, Bash(find *), Bash(ls *), Bash(wc *), Bash(git log *), Bash(git diff *), Bash(npm audit *), Bash(yarn audit *), Bash(pnpm audit *), Bash(pip audit *), Bash(pip-audit *), Bash(safety check *), Bash(cargo audit *), Bash(bundle audit *), Bash(bundle-audit *), Bash(composer audit *), Bash(dotnet list *), Bash(go list *), Bash(cat .gitignore)
---

# rock-quick

Read and follow the base workflow from [agent-rock](../agent-rock/SKILL.md).

Override the base workflow with these rules:

- Force the audit mode to `quick`.
- Treat `$ARGUMENTS` only as the target directory.
- If the user explicitly asks for a deep or exhaustive pass, tell them to use `rock-deep` instead.
- Keep the same evidence standard, report structure, Markdown output path, JSON output path, and confidence model as the base skill.

Use the same references, templates, and focused framework guides from the base `agent-rock` skill directory.
