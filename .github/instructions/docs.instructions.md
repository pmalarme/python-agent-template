---
applyTo: "docs/**/*,agents/*/docs/**/*"
---

# Copilot Instructions (Docs)

- Docs stack: Sphinx with `sphinx_autodoc_typehints`; install docs deps once via `uv run poe docs-install` (uses the `docs` group).
- Build everything: `uv run poe docs` (per-agent + unified). Per-agent only: `uv run --group docs python scripts/generate_docs.py --agents-only --agents <agent>`. Unified only: `uv run --group docs python scripts/generate_docs.py --unified-only`.
- Sources: unified at `docs/source`; per-agent at `agents/<agent>/docs/source`. Generated output: `docs/generated` and `agents/<agent>/docs/generated` — do not edit or commit generated HTML; rely on the GitHub Actions docs workflow to produce/publish generated content.
- PYTHONPATH for builds comes from `scripts/generate_docs.py`; ensure agents exist or the script exits early.
- Keep `_autosummary` directories out of version control (build script cleans them). When adding extensions, note `sphinx_autodoc_typehints` import is intentionally unused.
- Preferred Python: 3.13 (3.12 ok). Run commands via `uv run ...` to ensure the project env is active.
- Update docs/manual guides when changing build steps; align CLI flags with `scripts/generate_docs.py` help.
