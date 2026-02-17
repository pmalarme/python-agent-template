# agent1

Example agent built from the python-agent-template. Use this as a starting point and replace the description/code with your own agent. For a fuller walkthrough template, see [docs/agent-guide-template.md](../../docs/agent-guide-template.md).

## Quickstart (typical flow)
- Setup (repo root): `uv run poe setup` (creates/refreshes `.venv`, installs deps, hooks).
- Change into the agent: `cd agents/agent1`.
- Run the agent: `uv run agent1 Alice --greeting hello`.
- Run full checks for this agent: `uv run poe check` (from `agents/agent1`).
- Optional: switch back to root for repo-wide checks: `cd ../.. && uv run poe check`.

## Common dev tasks (agent-scoped)
- Format: `uv run poe fmt`
- Lint: `uv run poe lint`
- Type check: `uv run poe pyright` / `uv run poe mypy`
- Security scan: `uv run poe bandit`
- Tests: `uv run poe test`

## Run from repo root (alternative)
- Run the agent without `cd`: `uv run --package agent1 agent1 Alice --greeting hello`.
- Agent checks from root: `uv run poe -C agents/agent1 check`.
- Repo-wide checks: `uv run poe check`.

## Build the image (wheel-based)
- Build the container (from `agents/agent1`): `docker build -t agent1:latest .`.
- Run the container: `docker run --rm agent1:latest agent1 Bob` (override args as needed).

## Publish the package to GitHub Packages
- Configure env vars for publishing:
  - `export UV_PUBLISH_URL=https://pypi.pkg.github.com/<owner>`
  - `export UV_PUBLISH_TOKEN=<ghp_or_fine_grained_token_with_package_write>`
- Publish from the agent dir (`agents/agent1`): `uv run poe publish` (uploads the built wheel/sdist). From repo root use `uv run poe -C agents/agent1 publish`.
- Package namespace: `python_agent_template.agents.agent1` uses a namespace root without `__init__.py` so multiple agents can coexist (PyPA guidance: https://packaging.python.org/en/latest/guides/packaging-namespace-packages/).

## Anatomy
- `src/python_agent_template/agents/agent1/agent.py` — agent implementation.
- `tests/` — unit tests; extend with PyTest.
