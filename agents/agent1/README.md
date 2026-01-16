# agent1

Example agent built from the python-agent-template. Use this as a starting point and replace the description/code with your own agent. For a fuller walkthrough template, see [docs/agent-guide-template.md](../../docs/agent-guide-template.md).

## Quickstart (typical flow)
- Setup (repo root): `uv run poe setup` (creates/refreshes `.venv`, installs deps, hooks).
- Change into the agent: `cd agents/agent1`.
- Run the agent: `uv run agent1 Alice --greeting hello`.
- Run full checks for this agent: `uv run poe check` (from `agents/agent1`).
- Optional: switch back to root for repo-wide checks: `cd .. && cd .. && uv run poe check`.

## Common dev tasks (agent-scoped)
- Format: `uv run poe fmt`
- Lint: `uv run poe lint`
- Type check: `uv run poe pyright` / `uv run poe mypy`
- Security scan: `uv run poe bandit`
- Tests: `uv run poe test`

## Run from repo root (alternative)
 Run the agent without `cd`: `uv run -C agents/agent1 agent1 Alice --greeting hello`.
 Agent checks from root: `uv run -C agents/agent1 poe check`.
 Repo-wide checks: `uv run poe check`.

## Build the image (wheel-based)
- Build the container (from `agents/agent1`): `docker build -t agent1:latest .`.
- Run the container: `docker run --rm agent1:latest agent1 Bob` (override args as needed).
 Configure env vars for publishing:
  - `export UV_PUBLISH_URL=https://pypi.pkg.github.com/<owner>`
  - `export UV_PUBLISH_TOKEN=<ghp_or_fine_grained_token_with_package_write>`
 Publish from repo root: `uv run poe publish` (uploads the built wheel/sdist to GitHub Packages). Replace `<owner>` with your GitHub user or org.

## Publish the package to GitHub Packages
- Configure env vars for publishing:
 The package is published under the namespace `python_agent_template.agents.agent1`, following the PyPA namespace packaging guidance: https://packaging.python.org/en/latest/guides/packaging-namespace-packages/
 The namespace root `python_agent_template` (and its `agents` sub-namespace) have no `__init__.py`, allowing multiple agents to coexist; `agent1` is a regular package inside it.
- Publish from repo root: `uv run poe publish` (uploads the built wheel/sdist to GitHub Packages). Replace `<owner>` with your GitHub user or org.

 `src/python_agent_template/agents/agent1/agent.py` — agent implementation.
 `tests/` — unit tests; extend with PyTest.
- The `agents` namespace has no `__init__.py` so multiple agents can coexist without collisions; `agent1` is a regular package inside it.

## Anatomy
- `src/python_agent_template/agents/agent1/agent.py` — agent implementation.
- `tests/` — unit tests; extend with PyTest.
