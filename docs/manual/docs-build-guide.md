# Documentation Build Guide

How to build API docs for the template and each agent.

## What gets built
- Per-agent site: Sphinx sources in `agents/<agent>/docs/source` → HTML in `agents/<agent>/docs/generated`.
- Unified site: Sphinx sources in `docs/source` → HTML in `docs/generated`.
- Manual docs: hand-written content lives in `docs/manual`.

## Commands
- Default (build per-agent + unified):
  - `uv run --group docs python scripts/generate_docs.py`
- Per-agent only:
  - `uv run --group docs python scripts/generate_docs.py --agents-only [--agents agent1 agent2]`
- Unified only:
  - `uv run --group docs python scripts/generate_docs.py --unified-only`
- Via poe (root):
  - `uv run poe docs` (same as default)
  - Optional setup: `uv run poe docs-install` to sync the docs group once

## Outputs
- Per-agent HTML: `agents/<agent>/docs/generated`
- Unified HTML: `docs/generated`

## Path overrides (rarely needed)
- `--root`: repo root override
- `--source` / `--output`: agent-local source/output (relative to each agent unless absolute)
- `--unified-source` / `--unified-output`: unified source/output (relative to repo unless absolute)

## Best practices
- Do not commit generated HTML; build in CI and publish artifacts or Pages instead.
- Keep `docs/source/_autosummary` out of git (already ignored); the build script clears it.
- Use `uv run poe docs` locally before releasing if you need to verify the output.

## CI recommendation
- Add a GitHub Actions job that installs the docs group (`uv sync --group docs`) and runs `uv run poe docs`.
- Fail the job on Sphinx warnings/errors; optionally upload `docs/generated` as an artifact.

## Per-agent tasks
- Agents may expose `poe docs` locally; agent1 example runs `uv run python ../../scripts/generate_docs.py --agents-only --agents agent1`.
