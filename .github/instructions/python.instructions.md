---
applyTo: "**/*.{py,ipynb}"
---

# Python Instructions

- All Python code—including notebooks—must follow the repository standards in [CODING_STANDARDS.md](../../CODING_STANDARDS.md).
- For workflows, quality gates, and environment setup, refer to [DEVELOPMENT.md](../../DEVELOPMENT.md).

## Naming Conventions

- Use meaningful, spelled-out names for variables, functions, classes, and modules; avoid abbreviations.
- Use a leading underscore (`_`) for internal helpers that are not part of the public API.
- Use `is_`, `has_`, `can_`, `should_` prefixes for boolean variables and predicate functions.
- Include units or domain qualifiers in names that represent quantities (e.g., `timeout_seconds`, `file_size_bytes`).

## Code Style

- Line length: 120 characters (enforced by Ruff).
- Use double quotes for strings (enforced by Ruff).
- All public functions, classes, and modules must have Google-style docstrings.
- Imports must be sorted by Ruff: standard library → third-party → first-party.
- Prefer `async def` for I/O-bound code paths; never block the event loop with synchronous I/O or CPU-bound work.
- Avoid `shell=True` in subprocess calls; pass argument lists directly.
- Never hardcode secrets, tokens, credentials, or service endpoints in source code.

## Testing

- Name test modules `test_*.py`, test functions `test_<behavior>()`.
- Unit tests must not perform real network calls, database access, or filesystem writes.
- Use `pytest` fixtures for setup; prefer small, composable fixtures over large, implicit ones.
- Cover happy paths, edge cases, and error conditions; use parametrize for the same behavior across multiple inputs.

## Quality Gate

- Run `uv run poe check` (fmt, lint, pyright, mypy, bandit, tests, markdown-code-lint) before committing.
- Run agent-scoped checks with `uv run poe -C agents/<agent> check` when working inside an agent.
