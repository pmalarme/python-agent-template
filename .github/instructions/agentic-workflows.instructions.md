---
applyTo: ".github/workflows/*.md"
---

# Copilot Instructions (Agentic Workflows)

Agentic workflow files are [GitHub Agentic Workflows](https://github.github.com/gh-aw/) markdown files compiled to GitHub Actions `.lock.yml` files via `gh aw compile`.

## File Format

- Each workflow is a Markdown file in `.github/workflows/` with YAML frontmatter between `---` markers followed by a Markdown body.
- The frontmatter defines triggers, permissions, tools, safe-outputs, imports, and other configuration. The Markdown body contains the natural-language prompt executed by the AI engine at runtime.
- Only frontmatter changes require recompilation (`gh aw compile`). Edits to the Markdown body take effect at runtime without recompiling.

## Frontmatter Reference

- `on:` — Standard GitHub Actions trigger syntax (e.g., `pull_request`, `issues`, `schedule`). Extended with `reaction:`, `stop-after:`, `manual-approval:`, `forks:`, `skip-roles:`, `skip-bots:`.
- `description:` — Human-readable workflow description rendered as a comment in the lock file.
- `engine:` — AI engine (`copilot`, `claude`, `codex`, `custom`). Defaults to `copilot` if omitted.
- `imports:` — List of shared workflow components or agent files. Paths are **relative to the importing file** (e.g., `../agents/my-agent.md`). Only one agent file (from `.github/agents/`) can be imported per workflow.
- `permissions:` — Standard GitHub Actions permissions. When using safe-outputs for write actions (comments, reviews), the workflow itself typically only needs `read` permissions; the safe-output sandbox handles writes.
- `tools:` — Tool configurations: `bash`, `edit`, `github`, `web-fetch`, `web-search`, `playwright`, `cache-memory`, and MCP servers.
- `safe-outputs:` — Constrained write operations the AI can perform (e.g., `create-pull-request-review-comment`, `submit-pull-request-review`, `add-reviewer`, `create-issue-comment`). Each has a `max:` limit.
- `safe-inputs:` — Custom MCP tools defined inline using JavaScript or shell scripts.
- `network:` — Network access controls with domain allowlists and ecosystem identifiers (e.g., `python`, `node`, `defaults`).
- `strict:` — Enables enhanced security validation (default: `true`). Set `false` only for development/testing.
- `roles:` — Repository permission levels allowed to trigger the workflow. Defaults to `[admin, maintainer, write]`.
- `runs-on:` — Runner label (default: `ubuntu-latest`).
- `timeout-minutes:` — Workflow timeout (default: `20`). Use hyphen, not underscore.
- `concurrency:` — Concurrency policy for the agent job.
- `steps:` — Custom steps that run **before** agentic execution (outside the firewall sandbox; use only for deterministic preparation).
- `post-steps:` — Custom steps that run **after** agentic execution (outside the sandbox; use for cleanup/artifacts).
- `jobs:` — Custom jobs that run before the agentic job (outside the sandbox).
- `env:` — Workflow-level environment variables.
- `secrets:` — Secret values passed to the workflow (always use `${{ secrets.NAME }}`).
- `runtimes:` — Override default runtime versions (e.g., `node`, `python`, `uv`).
- `cache:` — Cache configuration using `actions/cache` syntax.

## Markdown Body

- The Markdown body is the prompt sent to the AI engine. Write clear, specific instructions.
- Use `${{ github.event.* }}` expressions to reference trigger context (e.g., PR number, issue body).
- Use `${{ needs.job-name.outputs.* }}` to reference outputs from custom `jobs:`.
- Structure the prompt with headings, numbered steps, and bullet points for clarity.
- Be explicit about expected behavior: what to review, what actions to take, and how to format output.

## Imports

- **Relative paths**: Import paths are resolved relative to the importing file. From `.github/workflows/`, use `../agents/my-agent.md` for agent files.
- **Remote imports**: Use `owner/repo/path@ref` format (e.g., `acme/shared-workflows/tools.md@v1.0.0`).
- **One agent per workflow**: Only one `.github/agents/` file can be imported per workflow.
- **Shared components**: Files without an `on:` field are shared components — validated but not compiled into Actions.
- **Frontmatter merging**: Imported `tools:`, `mcp-servers:`, `safe-outputs:`, `network:`, `runtimes:`, `services:`, and `steps:` are merged into the main workflow. `permissions:` are validated but not merged — the main workflow must declare all required permissions.

## Compilation

- Compile all workflows: `gh aw compile`.
- Compile a specific workflow: `gh aw compile <name>` (the basename without `.md`).
- Both the `.md` source and the generated `.lock.yml` must be committed.
- Use `gh aw compile --strict` to enforce action pinning, network config, and safe-output requirements.
- Use `gh aw compile --validate` for schema and action SHA validation.

## Security Best Practices

- Prefer `safe-outputs:` over `permissions: pull-requests: write` — let the sandbox handle writes.
- Set `max:` limits on all safe-outputs to bound AI behavior.
- Use `network:` allowlists with ecosystem identifiers (`python`, `node`, `defaults`) rather than individual domains.
- Keep `strict: true` (default) for production workflows.
- Never put secrets in the Markdown body; use `${{ secrets.NAME }}` in frontmatter `env:` or `secrets:`.
- Custom `steps:`, `post-steps:`, and `jobs:` run outside the firewall sandbox — use only for deterministic work.
