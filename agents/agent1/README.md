# agent1

Example agent built from the python-agent-template. Use this as a starting point and replace the description/code with your own agent.

## Quickstart
- From the repo root, set up once: `uv run poe setup` (creates/refreshes `.venv`, installs deps, installs pre-commit hooks).
- Full validation (all agents): `uv run poe check`.
- Faster, agent-scoped runs (from repo root):
  - `uv run poe -C agents/agent1 fmt`
  - `uv run poe -C agents/agent1 lint`
  - `uv run poe -C agents/agent1 pyright`
  - `uv run poe -C agents/agent1 mypy`
  - `uv run poe -C agents/agent1 bandit`
  - `uv run poe -C agents/agent1 test`
- To run only on agents changed by your branch: `python scripts/run_tasks_in_changed_agents.py <task>`

## Anatomy
- `src/agent1/agent.py` — agent implementation.
- `tests/` — unit tests; extend with PyTest.
