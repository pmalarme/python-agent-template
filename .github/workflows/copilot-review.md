---
description: Adds Copilot as a reviewer on a pull request after the security review
  agent approves it. Triggered when any review is submitted; only acts when the
  review is an approval from the security reviewer.

on:
  pull_request_review:
    types: [submitted]

permissions:
  contents: read
  pull-requests: read

tools:
  github:
    toolsets: [repos, pull_requests]

safe-outputs:
  add-reviewer:
    reviewers: [copilot]
    max: 1
    target: "triggering"
    github-token: ${{ secrets.GH_AW_AGENT_TOKEN }}
  noop:
    max: 1
---

# Add Copilot Reviewer After Security Approval

A review was just submitted on pull request
#${{ github.event.pull_request.number }}.

## Instructions

1. **Fetch the review that was just submitted.** Use the GitHub API to get the
   details of the review that triggered this workflow (review ID:
   ${{ github.event.review.id }}) on PR
   #${{ github.event.pull_request.number }}.

2. **Check if this is a security review approval.** Determine whether:
   - The review was submitted by the security review bot (look for a user
     whose login contains "github-actions" or whose review body references
     security review categories / security posture analysis).
   - The review state is `APPROVED`.
   - If **both** conditions are met, proceed to step 3.
   - If **either** condition is not met, use `noop` — this review is not
     relevant.

3. **Check if Copilot is already a reviewer.** Fetch the list of requested
   reviewers for PR #${{ github.event.pull_request.number }}. If Copilot
   (`copilot`) is already in the reviewer list, use `noop` — no action
   needed.

4. **Add Copilot as a reviewer.** If the security review approved the PR and
   Copilot is not yet a reviewer, add Copilot as a reviewer on the pull
   request.
