---
applyTo: ".github/workflows/*.yml,.github/workflows/tests/**/*"
---

# Copilot Instructions (GitHub Actions Workflows)

This file documents the conventions for the regular GitHub Actions YAML
workflows in `.github/workflows/*.yml` and the bash regression tests in
`.github/workflows/tests/`. For the `.md` agentic workflows compiled with
`gh aw compile`, see [`agentic-workflows.instructions.md`](agentic-workflows.instructions.md).

## Workflow File Layout

- One workflow per file, kebab-case filename matching the workflow's purpose
  (e.g., `python-tests.yml`, `monorepo-release.yml`,
  `monorepo-release-version-regex-test.yml`).
- Set a `name:` that reads cleanly in the GitHub Actions UI and PR check list.
  Prefix domain-grouped workflows with a colon-separated category
  (e.g., `"Python: tests"`, `"Monorepo release: VERSION regex regression test"`).
- Declare the minimum `permissions:` the workflow needs (default to
  `contents: read` for test-only workflows).
- Pin third-party actions by full commit SHA with a trailing comment giving
  the human-readable version, matching the existing style:
  `uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2`.
- Use `persist-credentials: false` on `actions/checkout` unless the job
  genuinely needs to push back to the repository.

## Pattern: Dedicated Regression Test Workflow

When a workflow contains a non-trivial piece of logic that the workflow
itself cannot fully validate — most commonly a regex, allowlist, or guard
that is only exercised against a single real input at runtime — add a
dedicated regression test workflow rather than wedging the check into an
unrelated existing workflow (e.g., `python-code-quality.yml`).

### When to use this pattern

- The logic under test is a guard, allowlist, or transformation whose
  contract matters across many inputs but is only ever exercised at runtime
  against one input.
- A silent regression (e.g., a "simplifying" refactor that loosens a regex)
  would not fail the host workflow against the current real input but would
  defeat the guard's purpose.
- The test is fast, deterministic, and has no language-specific dependency.

### Conventions

- **Test script location:** `.github/workflows/tests/test_<target-workflow>_<concept>.sh`.
  Examples: `test_monorepo_release_version_regex.sh`. Bash, executable
  semantics (`set -u`, `set -o pipefail`), curated valid/invalid inputs in
  arrays, clear `[ OK ]` / `[FAIL]` per case, non-zero exit on any failure.
- **Workflow file location and name:**
  `.github/workflows/<target-workflow>-<concept>-test.yml` with an explicit
  `name:` such as `"Monorepo release: VERSION regex regression test"`.
- **Header comment is mandatory.** Every dedicated test workflow MUST open
  with a top-of-file comment block that answers two questions:
  1. **Why this workflow exists** — what regression it catches that the
     host workflow cannot, with a concrete failure scenario.
  2. **When it runs and who can trigger it** — enumerate each trigger and
     state explicitly which actors can invoke it.
- **Triggers:** `pull_request` (no `branches:` filter — guard regressions
  matter regardless of source branch, including `copilot/*`), `push` to
  `main`, and `workflow_dispatch`. Use a `paths:` filter that lists the
  host workflow, the test script, and the test workflow itself so the job
  only fires when actually relevant.
- **Single non-matrix job.** Tests of workflow logic almost never depend on
  Python/Node/etc.; use a plain `runs-on: ubuntu-latest` job with one
  checkout + one test step. Do not piggyback on an existing matrix job.
- **Cross-reference both directions:** the host workflow's comment near the
  logic under test must point at the test script AND the test workflow;
  the test script's docstring must point back at the host workflow.

### Template

Copy-adapt this skeleton when adding a new dedicated regression test
workflow:

```yaml
name: "<Host workflow>: <concept> regression test"

# ---------------------------------------------------------------------------
# Why this workflow exists
# ---------------------------------------------------------------------------
# <One paragraph: what the host workflow does, what guard/contract this
# test protects, and the concrete regression it catches that the host
# workflow cannot detect on its own.>
#
# ---------------------------------------------------------------------------
# When this workflow runs (and who can trigger it)
# ---------------------------------------------------------------------------
# * `pull_request` — automatically on every PR whose diff touches the host
#   workflow, the test script, or this workflow itself. No `branches`
#   filter, because regressions are critical regardless of source branch.
# * `push` to `main` — covers direct commits to `main` that change the
#   same files.
# * `workflow_dispatch` — manual trigger; any user with write access to
#   the repository can run it on demand from the Actions tab.

on:
  workflow_dispatch:
  pull_request:
    paths:
      - ".github/workflows/<host-workflow>.yml"
      - ".github/workflows/tests/test_<target-workflow>_<concept>.sh"
      - ".github/workflows/<target-workflow>-<concept>-test.yml"
  push:
    branches: ["main"]
    paths:
      - ".github/workflows/<host-workflow>.yml"
      - ".github/workflows/tests/test_<target-workflow>_<concept>.sh"
      - ".github/workflows/<target-workflow>-<concept>-test.yml"

permissions:
  contents: read

jobs:
  <concept>-regression-test:
    name: <host workflow> <concept> regression test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          persist-credentials: false

      - name: Run <concept> regression test
        run: bash .github/workflows/tests/test_<target-workflow>_<concept>.sh
```

### Reference implementation

`.github/workflows/monorepo-release-version-regex-test.yml` (workflow) +
`.github/workflows/tests/test_monorepo_release_version_regex.sh` (test
script) — guards the semver-shape regex in
`.github/workflows/monorepo-release.yml`.

## Bash Test Scripts

- Live under `.github/workflows/tests/`. One script per guard/concept.
- File extension `.sh`, shebang `#!/usr/bin/env bash`, invoked from the
  workflow with `bash <path>` (no chmod dance required).
- Start with `set -u` and `set -o pipefail` (omit `set -e` so per-case
  `[FAIL]` messages can be aggregated before exiting).
- Keep VALID / INVALID inputs in clearly named bash arrays so future edits
  add cases by appending to a list, not by editing control flow.
- When testing a regex, do NOT quote the right-hand side of `=~` —
  `[[ "$value" =~ $REGEX ]]`, never `[[ "$value" =~ "$REGEX" ]]`.
  Quoting disables regex interpretation and silently turns the check
  into a literal string compare.
- Open the script with a comment explaining (a) what host workflow it
  protects, (b) that the regex/expression must be kept in sync with the
  host, and (c) how to run it locally.
- All `.sh` files in the repo are pinned to LF line endings via
  `.gitattributes` (`*.sh text eol=lf`). Do not weaken or remove that
  rule — Bash misinterprets stray CRs on the right-hand side of `=~` and
  in arithmetic contexts, producing baffling failures on Windows
  contributors' machines.

## Cross-Workflow Hygiene

- Do not add ad-hoc unrelated steps to general-purpose workflows like
  `python-code-quality.yml` or `python-tests.yml`. If a step is not about
  Python code quality or Python tests, give it its own workflow following
  the pattern above.
- Existing PR-triggered Python workflows use `branches: ["main", "feature*", "fix*"]`,
  which skips `copilot/*` branches. Be aware of this when adding checks
  that must run on auto-generated branches — use the dedicated-test pattern
  (no `branches:` filter) instead of relying on those filters.
