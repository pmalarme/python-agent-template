# python-agent-template

Security-first template for building and shipping multiple Python agents from one monorepo, derived from the Microsoft Agent Framework. It aims to give newcomers a ready-to-run, batteries-included starting point with guardrails (typing, linting, security, CI, releases) that you can adapt to your org’s standards.

> Disclaimer: This template is based on the Microsoft Agent Framework and provided for learning/acceleration. Evaluate and adapt to your organization’s security, compliance, and coding standards before production use.

## What’s inside and why
- **uv + poe**: fast installs and repeatable task runner (fmt/lint/types/tests/bandit).
- **Ruff, Pyright, MyPy, Bandit, PyTest, markdown code fence lint**: code quality and security guardrails.
- **Task fan-out scripts**: run tasks across all agents or only changed agents to keep CI fast.
- **Security automation**: CodeQL scanning and Dependabot for updates; good hygiene baseline.
- **Docs generation**: experimental py2docfx workflow (disabled by default) to emit docfx YAML.
- **Licensing**: each agent can ship its own LICENSE for package publication.

## Prerequisites
- Python 3.10–3.13 installed locally (3.13 default for `poe setup`).
- curl available to install uv, or install uv via your package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- Git for cloning and hooks.

## Getting started (root workspace)
1) Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2) Install dev deps (workspace-wide): `uv run poe setup`
3) Run full quality gate: `uv run poe check`

`poe setup` creates/refreshes `.venv`, installs all dev dependencies with uv, and installs pre-commit hooks so staged changes get checked automatically.

Local setup quickstart: clone the repo, ensure Python 3.10–3.13 is installed, run `uv run poe setup` to create/refresh `.venv` and install hooks, then `uv run poe check` to validate the workspace. For speed, `python scripts/run_tasks_in_changed_agents.py <task>` narrows lint/type/test to modified agents.

## Tasks: check vs pre-commit
- `poe check` (full suite, repo-wide):
	- Ruff format (`fmt`), Ruff lint (`lint`), Pyright, MyPy, Bandit, PyTest, Markdown code fence lint.
	- Runs across all agents. Use for CI and pre-merge confidence; catches issues outside your current diff.
- Pre-commit hooks (fast, staged-only):
	- Ruff format+lint, scoped MyPy, trailing whitespace/EOF fixers, markdown fence checks on staged files.
	- Purpose: keep diffs clean and reduce CI churn. Because it only sees staged files, it is fast but not a substitute for `poe check`.

Why staged-only for pre-commit: speed and focus on what you are changing. Why still run full checks in CI: to catch regressions in untouched files, ensure type/safety coverage repo-wide, and validate tests end-to-end.

### Pre-commit details
- Install once per clone: `uv run poe pre-commit-install` (adds hooks to `.git/hooks`).
- Run manually on all files: `uv run pre-commit run --all-files` (useful before large refactors or in CI if desired).
- Hook set (from `.pre-commit-config.yaml`): Ruff format + Ruff lint, MyPy (scoped), trailing-whitespace/EOF fixers, markdown fenced-code checker.
- If you must skip briefly, prefer `SKIP=hookname pre-commit run` instead of disabling globally.

## Repository layout
- `agents/` — each agent as a package (e.g., `agent1/`).
- `scripts/` — task fan-out and helper scripts (e.g., run tasks across agents, check markdown code blocks).
- `.github/workflows/` — CI (checks, release, CodeQL) and automation.
- `.pre-commit-config.yaml` — local hook definitions.
- `pyproject.toml` — shared config for uv, ruff, mypy, pyright, bandit, poe tasks.
- `docs/` — output/placeholder; doc generation is experimental.

Scripts explained (`scripts/`)
- `run_tasks_in_agents_if_exists.py`: runs a given task (fmt/lint/pyright/mypy/bandit/test) in every agent that defines it, so `poe check` can fan out safely even if some agents lack tasks.
- `run_tasks_in_changed_agents.py`: detects which agents changed relative to the target branch and runs the requested task only there; use for fast local/PR lint/type passes.
- `check_md_code_blocks.py`: validates fenced code blocks in README files; helps keep docs runnable.

Task catalog (root `poe` tasks)
- `poe setup`: create/refresh `.venv`, install deps, install pre-commit hooks (uses `poe venv`, `install`, `pre-commit-install`).
- `poe venv`: `uv venv --clear --python <version>`; default 3.13, override with `-p/--python`.
- `poe install`: `uv sync --all-extras --dev` (docs group excluded by default).
- `poe pre-commit-install`: install and refresh hooks.
- `poe fmt`: Ruff format.
- `poe lint`: Ruff lint.
- `poe pyright`: strict Pyright.
- `poe mypy`: strict MyPy.
- `poe bandit`: Bandit security scan.
- `poe test`: PyTest + coverage.
- `poe markdown-code-lint`: fenced-code checks in READMEs.
- `poe check`: bundle that runs fmt, lint, pyright, mypy, bandit, test, markdown-code-lint.

Bundled task contents (what runs where)
- `poe setup`: (1) create/refresh `.venv`, (2) `uv sync --all-extras --dev`, (3) install pre-commit hooks. Use once per clone or after Python version changes.
- `poe check`: Ruff format → Ruff lint → Pyright → MyPy → Bandit → PyTest + coverage → markdown code fence lint. Use before merge/CI to cover the full workspace.
- Pre-commit hook run (staged files only): Ruff format + Ruff lint, scoped MyPy, trailing-whitespace/EOF fixes, markdown fence checks; install with `uv run poe pre-commit-install`. Fast hygiene, not a replacement for `poe check`.

## Using this template for new agents
1) Copy `agents/agent1` to `agents/<your-agent>`.
2) Update metadata in `agents/<your-agent>/pyproject.toml` (name, description, URLs, deps).
3) Implement your code under `src/<your_agent>/` and extend `tests/`.
4) If you will publish the agent, place a `LICENSE` file in the agent directory and use `license-files = ["LICENSE"]` so wheels/sdists include it.
5) Run `uv run poe check`.

## Virtualenv setup and cleanup
- Create fresh env and install: `uv run poe setup` (runs `poe venv` → `uv sync` → pre-commit install). Default python is 3.13; override with `-p/--python`.
- Manual fallback if needed: `uv venv --python 3.13 && uv sync --all-extras --dev`.
- Clean everything: remove `.venv` and caches with `rm -rf .venv .pytest_cache .ruff_cache .mypy_cache __pycache__ agents/**/{.pytest_cache,.ruff_cache,.mypy_cache,__pycache__}`.

## Documentation (experimental)
- Scripts use py2docfx to emit docfx YAML into `docs/`. The docs tasks are commented out by default; install docs deps with `uv sync --group docs` if you want to experiment. Expect rough edges.

## Tooling reference (what/where/why)

Local + CI (from `pyproject.toml` and `.pre-commit-config.yaml`)

| Tool / service | Where it runs | What it does | Why it matters | Docs |
| --- | --- | --- | --- | --- |
| uv | Local + CI | Fast Python installer/resolver and executor for reproducible envs and tasks. | Keeps dependency installs deterministic and quick, so developers actually run checks. | [uv docs](https://docs.astral.sh/uv/) |
| Poe the Poet | Local + CI | Task runner that fans commands to all agents and provides `poe check`/`poe pre-commit-check`. | One entry point for fmt/lint/types/tests/security, reducing configuration drift. | [Poe docs](https://poethepoet.natn.io/) |
| Ruff (format + lint) | Local, pre-commit, CI | Auto-formats and lints Python/imports/docstrings; flags dead code, unsafe patterns, and some security issues. | Removes style noise from reviews and catches correctness issues early. | [Ruff docs](https://docs.astral.sh/ruff/) |
| Pyright (strict) | Local + CI | Fast static type checker with precise inference. | Prevents type regressions and interface drift; great developer ergonomics. | [Pyright docs](https://microsoft.github.io/pyright/) |
| MyPy (strict) | Local + CI (scoped in pre-commit) | Second static type checker with a different inference engine and plugin support (pydantic). | Adds coverage where Pyright differs; reduces blind spots by double-checking types. | [MyPy docs](https://mypy.readthedocs.io/en/stable/) |
| Bandit | Local, pre-commit, CI | Security static analysis for Python. | Flags risky calls (eval, weak crypto, subprocess misuse) before merge. | [Bandit docs](https://bandit.readthedocs.io/en/latest/) |
| PyTest + pytest-cov | Local + CI | Runs tests with coverage reporting. | Proves behavior still works; coverage highlights untested risk. | [PyTest](https://docs.pytest.org/en/latest/), [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) |
| Markdown code fence lint | Local + CI | Checks fenced code blocks in project READMEs. | Prevents broken snippets and docs drift. | [scripts/check_md_code_blocks.py](scripts/check_md_code_blocks.py) |
| pre-commit framework | Local | Runs the hook set on staged files. | Automates hygiene (format, lint, security) before commits land. | [pre-commit docs](https://pre-commit.com/) |
| pre-commit-hooks bundle | Local | Trims whitespace, fixes EOF, normalizes newlines, validates YAML/TOML/JSON, AST checks, forbids debug statements. | Removes common footguns and keeps config files valid. | [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks) |
| pyupgrade hook | Local | Rewrites Python syntax to modern 3.10+. | Eliminates legacy syntax and aligns with supported versions. | [pyupgrade](https://github.com/asottile/pyupgrade) |
| nbQA hook | Local | Validates notebook cells parse as Python. | Stops broken notebooks from entering the repo. | [nbQA docs](https://nbqa.readthedocs.io/en/latest/) |
| uv-lock hook | Local | Refreshes `uv.lock` when `pyproject.toml` changes. | Ensures lockfile matches manifests, preventing supply-chain drift. | [uv-pre-commit](https://github.com/astral-sh/uv-pre-commit) |
| Poe pre-commit-check hook | Local | Runs diff-aware fmt/lint/pyright/markdown checks via Poe. | Fast, staged-only guardrail that mirrors CI styling and type rules. | [pyproject.toml](pyproject.toml) |

Why both Pyright and MyPy: they use different inference engines and plugin ecosystems, so running both raises signal and lowers the chance of missing type errors.

GitHub-hosted automation (security and updates)

| Service | What it does | Why it matters | Docs |
| --- | --- | --- | --- |
| CodeQL Analysis | Code scanning for Python and GitHub Actions code. | Finds dataflow and security issues beyond linters/typing. | [CodeQL docs](https://docs.github.com/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-codeql-code-scanning) |
| Dependabot | Weekly updates for pip/uv dependencies and GitHub Actions. | Shrinks vulnerability exposure windows and keeps CI runners current. | [Dependabot docs](https://docs.github.com/code-security/dependabot/dependabot-version-updates) |

## Security and automation
- **Dependabot**: keeps pip/uv and GitHub Actions up to date. Alternatives: Renovate, Snyk, Mend. Important to run some updater to shrink vulnerability exposure windows.
- **CodeQL**: SAST/code scanning for Python and GitHub Actions. Alternatives: semgrep, commercial SAST. Important to have at least one scanner in place.
- **Branch protection/rulesets and auto-fix**: enforce required checks, signed commits, and allow trusted bots (e.g., Dependabot) to auto-merge with autofix where policy allows.

## Copyright option
- Ruff copyright enforcement is available but disabled. If your org requires it, enable the `flake8-copyright` block in `pyproject.toml` and add headers. Leave it off to avoid breaking contributions until ready.
