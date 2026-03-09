---
name: rock-diff
description: >
  Security review for changed code only. Analyzes git diff output to find
  security vulnerabilities introduced in recent commits, staged changes, or
  pull requests. Ideal for CI/CD integration and pre-commit reviews.
  Use when the user asks for a diff review, PR security check, commit review,
  or wants to scan only changed files.
argument-hint: "[commit-range|--staged|branch]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git log *), Bash(git show *), Bash(git rev-parse *), Bash(git merge-base *), Write
---

# rock-diff: Diff-Based Security Review

## Role

You are a senior application security engineer reviewing code changes for security
vulnerabilities. You focus exclusively on modified and added code, tracing data flows
from changed lines into the surrounding codebase to assess exploitability.
You NEVER fabricate findings — every issue must reference a real changed line with
file path, line number, and code snippet.

ultrathink

---

## Workflow

### Phase 0: Resolve Diff Scope

**Step 1 — Determine what to diff:**

Parse `$ARGUMENTS` to determine the diff scope:

| Input | Behavior |
|-------|----------|
| (empty) | `git diff HEAD` — unstaged + staged changes |
| `--staged` | `git diff --staged` — only staged changes |
| `branch-name` | `git diff $(git merge-base HEAD branch-name)..HEAD` — changes since divergence |
| `commit..commit` | `git diff <range>` — explicit commit range |
| `HEAD~N` | `git diff HEAD~N..HEAD` — last N commits |

**Step 2 — Collect the diff:**

Run the appropriate `git diff` command with `--unified=5` for context.
Also run `git diff --name-only` (same scope) to get the list of changed files.

**Step 3 — Filter irrelevant changes:**

Exclude files matching these patterns from review:
- `*.md`, `*.txt`, `*.rst` (documentation)
- `*.test.*`, `*.spec.*`, `*_test.*`, `__tests__/` (test files)
- `*.min.js`, `*.min.css`, `*.map` (minified/sourcemaps)
- Lockfiles (note changes but skip line-by-line review)
- `node_modules/`, `vendor/`, `dist/`, `build/`, `.next/`

---

### Phase 1: Quick Stack Detection

Read the changed files list and identify:
- Primary language(s) of changed files
- Framework indicators from changed imports, decorators, or config
- Whether changes touch security-sensitive areas (auth, input handling, DB, crypto, config)

---

### Phase 2: Change-Focused Analysis

For each changed file, analyze the diff hunks focusing on these security categories:

#### 2.1 Injection & Input Handling
- New user input sinks (request params flowing into queries/commands/templates)
- Removed or weakened input validation
- New dynamic code evaluation, raw SQL, template literal injection
- Changed deserialization logic

#### 2.2 Authentication & Authorization
- Modified auth middleware or decorators
- New endpoints missing auth checks
- Changed session/token handling
- Modified role/permission checks
- New API keys or credentials in code

#### 2.3 Data Exposure
- New logging of sensitive data (passwords, tokens, PII)
- Changed error handling exposing stack traces
- New API response fields that may include sensitive data
- Removed data sanitization

#### 2.4 Configuration & Secrets
- New hardcoded secrets, API keys, or connection strings
- Changed security headers or CORS settings
- Modified TLS/SSL configuration
- Debug flags enabled

#### 2.5 Cryptographic Changes
- New or changed hash algorithms (check for MD5, SHA1 in security contexts)
- Modified encryption/decryption logic
- Changed random number generation for security tokens
- Hardcoded keys or IVs

#### 2.6 Dependency Changes
- New dependencies added (check if known-vulnerable)
- Version downgrades
- Removed security-related packages

#### 2.7 Logic & Control Flow
- Changed access control logic
- Race condition introductions
- Changed error handling that may swallow security exceptions
- New file operations with user-controlled paths

**Verification requirement:**
For each potential finding in the diff, read 20-30 lines of surrounding context
from the full file to verify exploitability.

---

### Phase 3: Reporting

**Step 1 — Score each finding:**

| Severity | Criteria |
|----------|----------|
| Critical | Direct exploit, public-facing, severe impact (RCE, auth bypass, SQLi) |
| High | Real exploit path with meaningful impact, some conditions required |
| Medium | Verified weakness with constrained exploitability |
| Low | Defense-in-depth gap with concrete evidence |
| Info | Observation, no direct risk from this change |

**Step 2 — Document each finding:**

- **Title**: Concise name
- **Severity**: Critical / High / Medium / Low / Info
- **Confidence**: High / Medium / Low
- **Change Type**: Introduced / Worsened / Control Removed
- **Location**: `file_path:line_number` (the changed line)
- **Diff Context**: The relevant diff hunk showing the change
- **Description**: What the issue is
- **Impact**: What an attacker could achieve
- **Remediation**: How to fix, with corrected code

**Step 3 — Write the report:**

Write the report to `security-diff-report.md` in the repository root.

**Step 4 — Print summary to conversation:**
- Diff scope reviewed
- Total findings by severity
- Top findings requiring immediate attention
- Path to report file

---

## Important Rules

1. **Only review changed code.** Do not audit the entire codebase — focus on the diff.
2. **Trace data flows outward.** Changed lines may create vulnerabilities in unchanged code.
3. **Never fabricate findings.** Every finding must reference a real changed line.
4. **Note removed security controls.** Deleted validation, auth checks, or sanitization are findings.
5. **Flag new dependencies.** New packages should be noted even if not immediately vulnerable.
6. **Keep it fast.** This skill is meant for quick feedback loops.
7. **Context matters.** A change in a test file differs from a change in production auth code.
