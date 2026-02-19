---
description: Automated security review for pull requests. Analyzes changed files against
  15 security posture categories and posts inline review comments on findings.

on:
  workflow_call:

permissions:
  contents: read
  pull-requests: read

engine:
  id: copilot
  agent: security-reviewer

tools:
  cache-memory:
    - id: pull-request-review-context
      key: "security-review-pr-${{ github.event.pull_request.number }}"
    - id: review patterns
      key: "security-review-patterns"
      retention-days: 30
  github:
    toolsets: [repos, pull_requests]

safe-outputs:
  create-pull-request-review-comment:
    max: 20
    target: "triggering"
  submit-pull-request-review:
    max: 1
    footer: false
---

# Security Review

Review the code changes in pull request
#${{ github.event.pull_request.number }} using the imported security review
agent instructions.

## Instructions

1. **Access memory first.** Use cache memory at
   `/tmp/gh-aw/cache-memory/` to:
   - Check prior review context for this PR at
     `/tmp/gh-aw/cache-memory/security-review-pr-${{ github.event.pull_request.number }}.json`. This correspond to the cache memory tool with id `pull-request-review-context` and can contain information about previous review findings, categories, files reviewed, and timestamps for this PR.
   - Identify recurring security patterns in this repository from
     `/tmp/gh-aw/cache-memory/security-review-patterns.json`. This correspond to the cache memory tool with id `review-patterns` and can contain information about recurring security issues and patterns in the repository.
   - Avoid repeating the same inline comments from previous reviews if the previous comment is not resolved yet nor outdated (e.g., if the same issue is still present in the code or if the code has not changed since the last review).

2. **Fetch the pull request diff.** Read the pull request details and all
   changed files for PR #${{ github.event.pull_request.number }}.

3. **Review every changed file** against all 15 security posture categories
   from the imported agent instructions. Focus only on the lines that were
   added or modified in the diff — do not flag pre-existing code that was not
   touched.

4. **Post inline review comments** on specific code lines where you find
   security issues. Each comment must include:
   - The security category (e.g., "Input Validation", "Secrets")
   - Severity: critical, high, medium, low, or informational
   - A clear description of the issue and why it matters
   - A concrete, actionable recommendation or code fix

5. **Submit the review.** After posting all inline comments:
   - If you found any **critical** or **high** severity issues, submit the
     review with `REQUEST_CHANGES` and a summary body listing the top findings.
   - If you found only **medium** or **low** issues, submit with `APPROVE` and
     a brief summary noting the medium/low findings. These are not blocking.
   - If no issues were found, submit with `APPROVE` and a body stating the
     changes look secure.
   - **Supersede previous review if resolved.** Check the cache memory for
     this PR to see if a previous security review submitted
     `REQUEST_CHANGES`. If it did, compare the previous findings against the
     current diff. If the previously flagged issues have been fixed and no
     new critical/high issues are found, submit the new review as `APPROVE`
     with a detailed body that includes:
     - A summary stating the previous issues have been resolved.
     - A list of the previously flagged findings and how each was addressed
       (e.g., "**Input Validation** (high): User input is now sanitized in
       `validators.py` — resolved.").
     - Any remaining medium/low findings from the current review, if any.
     - This replaces the old `REQUEST_CHANGES` review and unblocks the PR.

6. **Update memory.** After submitting the review:
   - Write/update PR-specific memory at
     `/tmp/gh-aw/cache-memory/security-review-pr-${{ github.event.pull_request.number }}.json`
     including review timestamp, findings summary, categories found, and files
     reviewed. The id of the cache memory tool for this is `pull-request-review-context`.
   - Update shared pattern memory at
     `/tmp/gh-aw/cache-memory/security-review-patterns.json` with recurring
     issue themes and counts. The id of the cache memory tool for this is `review-patterns`.

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
- **Use memory intentionally.**
  - Track patterns: notice if the same issue types keep recurring
  - Avoid repetition: do not post duplicate comments in the same PR
  - Build context: use previous review outcomes to improve prioritization
