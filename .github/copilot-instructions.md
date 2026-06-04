# Project Overview

This project is a template for creating Python-based agents. It provides a structured layout, development guidelines, and best practices to help developers build, test, document, and deploy their agents efficiently and securely.

## Folder Structure
- `agents/`: multiple agent packages
  - `agents/<agent>/src/python_agent_template/agents/<agent>/`: agent code
  - `agents/<agent>/tests/`: agent tests
  - `agents/<agent>/docs/`: agent docs (`source/` for inputs, `generated/` for outputs)`
- `docs/`: unified docs (`source/` inputs, `generated/` outputs)
- `scripts/`: shared tooling (e.g., docs generation helpers)
- `LICENSE`: license file
- `pyproject.toml`: project configuration and dependencies
- `DEVELOPMENT.md`: development guide
- `README.md`: project overview

## Libraries and Frameworks
- Python 3.13 (preferred) or 3.10+
- Sphinx for documentation with `sphinx_autodoc_typehints`
- Uv for environment and task management
- Ruff for linting and formatting
- Pyright and Mypy for type checking
- Bandit for security scanning
- Pytest for testing

## General Code Review Standards

### Code Quality Essentials
- Keep functions focused and appropriately sized.
- Use clear, descriptive names.
- Ensure proper error handling throughout.

### Security Standards
- Never hardcode credentials or API keys.
- Validate all user inputs.
- Use parameterized queries to prevent SQL injection.

### Documentation Expectations
- Add doc comments to all public functions.
- Add brief comments for complex algorithms.
- Keep README files up to date.

## Development Quickstart (root)
- Recommended Python: 3.13 (3.10+ also supported). Use `uv run poe setup` to create/refresh `.venv` and install hooks.
- Run full quality gate from root: `uv run poe check` (fmt, lint, pyright, mypy, bandit, tests, markdown lint).
- Monorepo layout: `agents/` (multiple agent packages), `scripts/` (fan-out helpers), `docs/` (unified Sphinx sources/output).
- Run an agent from root: `uv run --package <agent> <agent> ...`; agent checks: `uv run poe -C agents/<agent> check`.
- Docs build (after `uv run poe docs-install`): `uv run poe docs`; per-agent only: `uv run --group docs python scripts/generate_docs.py --agents-only --agents <agent>`.
- See [DEVELOPMENT.md](../DEVELOPMENT.md) for the full dev guide.

## Generated Docs
- `docs/generated` and `agents/*/docs/generated` are produced by the GitHub Actions docs workflow; do not edit or commit them.

## GitHub Actions Workflows
- Regular workflow YAML lives in `.github/workflows/*.yml`. Bash regression tests for workflow logic live in `.github/workflows/tests/`.
- When a workflow contains a guard, allowlist, or regex that the workflow itself only ever exercises against one runtime input (e.g., the semver-shape regex in `monorepo-release.yml`), add a **dedicated regression test workflow** rather than wedging the check into an unrelated existing workflow.
- The dedicated test workflow MUST have an explicit `name:`, a top-of-file header comment explaining **why** it exists and **when/who** can trigger it, and triggers on `pull_request` + `push` to `main` + `workflow_dispatch` with a `paths:` filter scoped to the host workflow, the test script, and the test workflow itself. No `branches:` filter, so it also runs on `copilot/*` branches that the main Python workflows skip.
- See [`.github/instructions/github-actions.instructions.md`](instructions/github-actions.instructions.md) for the full pattern, template, and reference implementation (`monorepo-release-version-regex-test.yml`).
