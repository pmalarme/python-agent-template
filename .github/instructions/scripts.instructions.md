---
applyTo: "scripts/**/*"
---

# Copilot Instructions (Scripts)

- Scripts are shared utilities that run across agents; keep them general-purpose and free of agent-specific logic.
- Always pass argument lists to `subprocess` instead of using `shell=True` to prevent shell injection vulnerabilities.
- Use `# noqa: S603  # nosec B603` inline when calling subprocess with a statically known argument list to suppress false-positive security warnings from Ruff and Bandit.
- Validate any user-supplied or environment-sourced inputs before passing them to subprocesses or external calls.
- Add a module-level docstring and Google-style docstrings on all public functions.
- Keep scripts idempotent and safe to re-run; write to temporary paths first and move atomically when producing output files.
- Do not import from `agents/` packages; scripts must remain runnable from the repo root without agent dependencies.
