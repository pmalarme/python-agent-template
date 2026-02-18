---
description: Automated security review for pull requests. Analyzes changed files against
  15 security posture categories and posts inline review comments on findings,
  then requests Copilot code review.

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: read

engine:
  id: copilot
  agent: security-reviewer

tools:
  github:
    toolsets: [repos, pull_requests]

safe-outputs:
  create-pull-request-review-comment:
    max: 20
    target: "triggering"
  submit-pull-request-review:
    max: 1
    footer: false
  add-reviewer:
    reviewers: [copilot]
    max: 1
    target: "triggering"
---

# Security Review

Review the code changes in pull request
#${{ github.event.pull_request.number }} using the imported security review
agent instructions.

## Instructions

1. **Fetch the pull request diff.** Read the pull request details and all
   changed files for PR #${{ github.event.pull_request.number }}.

2. **Review every changed file** against all 15 security posture categories
   from the imported agent instructions. Focus only on the lines that were
   added or modified in the diff — do not flag pre-existing code that was not
   touched.

3. **Post inline review comments** on specific code lines where you find
   security issues. Each comment must include:
   - The security category (e.g., "Input Validation", "Secrets")
   - Severity: critical, high, medium, low, or informational
   - A clear description of the issue and why it matters
   - A concrete, actionable recommendation or code fix

4. **Submit the review.** After posting all inline comments:
   - If you found any **critical** or **high** severity issues, submit the
     review with `REQUEST_CHANGES` and a summary body listing the top findings.
   - If you found only **medium** or **low** issues, submit with `COMMENT` and
     a brief summary.
   - If no issues were found, submit with `COMMENT` and a body stating the
     changes look secure.

5. **Request Copilot review.** After submitting the security review, add
   `copilot` as a reviewer on the pull request for an additional code quality
   review.

## Review Guidelines

- **Only review changed lines.** Do not flag pre-existing issues in untouched
  code.
- **Be specific and actionable.** Each finding must include a concrete fix.
- **Prioritize by severity.** Focus on critical and high issues first.
- **Use the project context.** This is a Python monorepo using Ruff, Pyright
  strict mode, Bandit, and pytest. The project follows secure-by-default
  principles documented in `CODING_STANDARDS.md`.
- **Do not produce false positives.** If you are unsure whether something is a
  real issue, state your uncertainty and classify it as informational.
