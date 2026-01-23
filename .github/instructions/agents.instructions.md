---
applyTo: "agents/**/*"
---

# Copilot Instructions (Agents)

- Use Python 3.13 (preferred) or 3.12 via `uv run` inside the agent dir; from root, run agents with `uv run --package <agent> <agent> [args]`.
- Run the agent: `uv run <agent> [args]` from `agents/<agent>/` (e.g., sample agent: `uv run agent1 Alice --greeting hello`). From root, use `uv run --package <agent> <agent> [args]`.
- Run agent checks: `uv run poe check` (fmt, lint, pyright, mypy, bandit, tests) inside the agent, or `uv run poe -C agents/<agent> check` from root.
- Common tasks: `poe fmt|lint|pyright|mypy|bandit|test`; keep imports and types clean per strict settings.
- Markdown hygiene: keep README/docs code blocks valid; if you add new `.md` files under the agent, ensure `markdown-code-lint` covers them (extend the task glob if needed). Do not commit generated docs; rely on the GitHub Actions docs workflow to produce them.
- Structure reminder: code under `src/python_agent_template/agents/<agent>/`, tests under `tests/`, docs under `docs/source`, generated docs under `docs/generated` (do not edit or commit generated output; they are produced by the GitHub Actions docs workflow).
- Keep agent README and docs updated; add docstrings for public functions and brief comments for non-obvious logic.
- Security: no secrets in code, keep `subprocess` args static, avoid `shell=True`, validate inputs.
- If publishing, ensure agent `pyproject.toml` metadata and LICENSE are set, and wheels are built via the Dockerfile or `uv run poe publish` when configured.
