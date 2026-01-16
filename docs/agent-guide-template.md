# Agent Guide Template

Use this as a blueprint when creating or maintaining any agent in this monorepo. Replace `<agent>` with your agent’s name.

## Principles and conventions
- Isolated per-agent projects under `agents/<agent>` to avoid dependency/release coupling.
- `src/` layout to force imports from the installed package and catch packaging/import issues early.
- Namespace per project: `python_agent_template.agents.<agent>` with namespace packages (no `__init__.py` at the namespace roots) per PyPA guidance: https://packaging.python.org/en/latest/guides/packaging-namespace-packages/
- Wheel-first images: build a wheel and install it in the runtime image for reproducibility and smaller layers.
- Tasks via `uv run` + `poe` for consistent env management.

## Structure (replace `<agent>`)
```
agents/<agent>/
├─ Dockerfile                # wheel-based image build
├─ LICENSE                   # agent-specific license (included in wheel/sdist)
├─ README.md                 # quickstart and usage
├─ pyproject.toml            # agent metadata, tasks, tooling config, script entrypoint
├─ src/
│  └─ python_agent_template/
│     └─ agents/
│        └─ <agent>/
│           ├─ __init__.py   # exports
│           ├─ __main__.py   # CLI entrypoint
│           └─ agent.py      # core logic
└─ tests/
   └─ test_agent.py          # unit tests for agent logic
```

## Creating a new agent (recipe)
1) Copy `agents/agent1` to `agents/<agent>`.
2) Rename package path under `src/python_agent_template/agents/<agent>`; update imports.
3) Update `pyproject.toml`: project name/description/URLs, script entrypoint, `tool.flit.module = "python_agent_template.agents.<agent>"`, bandit target, coverage target.
4) Adjust Dockerfile tags/paths if needed.
5) Update README for the new agent with run/build/publish instructions.
6) Run `uv run poe check` inside `agents/<agent>`; optionally run `uv run poe check` from root.

## Daily workflow
1) Setup once (root): `uv run poe setup`.
2) Work inside the agent: `cd agents/<agent>`.
3) Run the CLI: `uv run <agent> Alice --greeting hello` (or from root with `uv run -C agents/<agent> ...`).
4) Run agent checks: `uv run poe check`.
5) Before publishing or merging, optionally run repo-wide checks from root: `uv run poe check`.

## Tasks (agent-scoped)
- `poe fmt` — ruff format
- `poe lint` — ruff lint
- `poe pyright` — strict pyright
- `poe mypy` — strict mypy
- `poe bandit` — security scan on agent code
- `poe test` — pytest with coverage
- `poe check` — bundle of the above
Run with `uv run poe <task>` from `agents/<agent>`, or `uv run -C agents/<agent> poe <task>` from root.

## Running the agent
- From agent dir: `uv run <agent> Alice --greeting hello`
- From root: `uv run -C agents/<agent> <agent> Alice --greeting hello`

## Testing and coverage
- Unit tests: `uv run poe test`
- The CLI guard `if __name__ == "__main__":` is often marked `# pragma: no cover` because it only runs as a script; add a CLI test and drop the pragma if you want it counted.

## Lint, types, security
- Format then lint: `uv run poe fmt` and `uv run poe lint`
- Types: `uv run poe pyright` and `uv run poe mypy`
- Security: `uv run poe bandit`

## Build the container (wheel-based)
- Build: `docker build -t <agent>:latest .`
- Run: `docker run --rm <agent>:latest <agent> Bob`
- Rationale: builder stage creates a wheel; runtime installs the wheel for reproducibility and a smaller attack surface.

## Publish to GitHub Packages
- Set:
  - `export UV_PUBLISH_URL=https://pypi.pkg.github.com/<owner>`
  - `export UV_PUBLISH_TOKEN=<token_with_package_write>`
- From agent dir: `uv run poe publish` (uploads wheel/sdist for this agent), or from root: `uv run -C agents/<agent> poe publish`.

## What lives where
- Agent-level (agents/<agent>): code, tests, Dockerfile, agent-specific tasks/config, LICENSE, README, built artifacts.
- Project-level (root): shared tasks, root `pyproject.toml`, shared scripts (`scripts/`), CI, global lint/type/test settings.

## Troubleshooting
- uv missing: install via `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- Publish auth errors: confirm `UV_PUBLISH_TOKEN` and `UV_PUBLISH_URL` point to your owner.
- Import errors: use `uv run ...` and correct cwd (`agents/<agent>` or `-C agents/<agent>`).
