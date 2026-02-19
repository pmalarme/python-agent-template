# Agent Guide Template

Use this as a blueprint when creating or maintaining any agent in this monorepo. Replace `<agent>` with your agent’s name.

## Principles and conventions
- Isolated per-agent projects under `agents/<agent>` to avoid dependency/release coupling.
- `src/` layout to force imports from the installed package and catch packaging/import issues early.
- Namespace per project: `python_agent_template.agents.<agent>` with namespace packages (no `__init__.py` at the namespace roots) per PyPA guidance: https://packaging.python.org/en/latest/guides/packaging-namespace-packages/
- Wheel-first images: build a wheel and install it in the runtime image for reproducibility and smaller layers.
- Tasks via `uv run` + `poe` for consistent env management.
- Secure-by-default posture: treat secrets as env/secret-store only, validate all inputs, avoid logging sensitive data, and block unsafe shell usage by default.

## Secure helpers (copy/adapt per agent)
- Validate inputs with simple guard clauses (e.g., reject blank/whitespace for required text fields) close to where data enters your agent.
- Prefer these helpers in agent logic and CLI parsing so new contributors follow the safer path by default.

## Secure-by-default checklist (include in each agent README/docs)
- Secrets: load from environment/secret store only; never hardcode tokens/keys.
- Input validation: validate CLI/user input with guard clauses; reject blank/whitespace and unexpected values early.
- Logging/PII: avoid logging secrets or user-provided sensitive data; redact when unsure.
- External calls/commands: favor library calls over shell; if shelling out, build argv lists (no `shell=True`).
- Quality gate: run `uv run poe check` before pushing to catch format/lint/type/security/test issues.
- Tests: include at least one validation test and one test that guards unsafe command construction so contributors see the expected patterns.

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
3) Run the CLI: `uv run <agent> Alice --greeting hello` (or from root with `uv run --package <agent> <agent> ...`).
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
Run with `uv run poe <task>` from `agents/<agent>`, or `uv run poe -C agents/<agent> <task>` from root.

## Running the agent
- From agent dir: `uv run <agent> Alice --greeting hello`
- From root: `uv run --package <agent> <agent> Alice --greeting hello`

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
- From agent dir: `uv run poe publish` (uploads wheel/sdist for this agent), or from root: `uv run poe -C agents/<agent> publish`.

## What lives where
- Agent-level (agents/<agent>): code, tests, Dockerfile, agent-specific tasks/config, LICENSE, README, built artifacts.
- Project-level (root): shared tasks, root pyproject, shared scripts (scripts/), CI, global lint/type/test settings.
- Docs (root): `docs/source/` Sphinx inputs build to `docs/generated` for the unified site.
- Docs (per-agent): `agents/<agent>/docs/source/` Sphinx inputs build to `agents/<agent>/docs/generated`.

### Documentation builds
- Refer to the dedicated docs build guide for commands, outputs, and CI recommendations: [docs/manual/docs-build-guide.md](docs/manual/docs-build-guide.md).

## Troubleshooting
- uv missing: install via `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- Publish auth errors: confirm `UV_PUBLISH_TOKEN` and `UV_PUBLISH_URL` point to your owner.
- Import errors: use `uv run ...` and correct cwd (`agents/<agent>` or `uv run --package <agent> ...` / `uv run poe -C agents/<agent> ...`).
