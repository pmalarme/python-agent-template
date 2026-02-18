---
applyTo: ".github/agents/*.agent.md"
---

# Copilot Instructions (Copilot Custom Agents)

Copilot custom agents are Markdown prompt files in `.github/agents/` that customize AI engine behavior for specific tasks. They can be used directly in GitHub Copilot Chat (via `/agent`) or imported into [GitHub Agentic Workflows](https://github.github.com/gh-aw/).

## File Format

- Each agent is a Markdown file in `.github/agents/` using the `*.agent.md` naming convention, with YAML frontmatter between `---` markers followed by a Markdown body containing the agent prompt.
- The frontmatter defines agent metadata. The Markdown body contains the system-level instructions that shape the AI's behavior.

## Frontmatter Fields

- `name:` — Human-readable agent name (e.g., `Security Reviewer Agent`).
- `description:` — Brief description of the agent's purpose and scope.
- `tools:` — Tool configurations available to the agent (merged into importing workflows).
- `mcp-servers:` — MCP server configurations (merged into importing workflows).
- `disable-model-invocation:` — Set `true` for dispatcher/routing agents that only organize other agents without invoking the model themselves.

Do **not** add fields that belong in workflows (e.g., `on:`, `permissions:`, `engine:`, `safe-outputs:`). These are set by the importing workflow, not the agent.

## Markdown Body (Prompt)

- Start with a clear role statement: who the agent is and what it does.
- Be specific about the task scope, methodology, and expected output format.
- Use headings and checklists to organize categories of work.
- Include concrete examples of good and bad patterns when helpful.
- Reference project conventions (e.g., `CODING_STANDARDS.md`) for context.
- Keep prompts actionable — every instruction should translate to observable AI behavior.

## Agent Design Guidelines

- **Single responsibility**: Each agent should focus on one well-defined task (e.g., security review, code review, documentation review). Compose agents via separate workflows rather than making one agent do everything.
- **Be thorough but bounded**: List all categories/checks the agent should evaluate, but keep each check concise. Use checklists (`- [ ]`) for systematic coverage.
- **Specify output format**: Define how findings should be reported (e.g., severity levels, file/line references, structured tables). This ensures consistent, actionable output.
- **Severity classification**: When the agent identifies issues, define a severity scale (e.g., critical, high, medium, low, informational) and explain how each level maps to actions.
- **Minimize false positives**: Include guidance like "only flag issues you are confident about" and "state uncertainty as informational."
- **Project context**: Reference the project's tech stack, conventions, and standards so the agent's recommendations are relevant (e.g., "This is a Python monorepo using Ruff, Pyright strict, Bandit").

## Importing into Agentic Workflows

- Import via the `imports:` field in a workflow's frontmatter. Paths are relative to the importing file (e.g., `../agents/my-agent.agent.md` from `.github/workflows/`).
- Only **one agent** can be imported per workflow.
- Agent `tools:` and `mcp-servers:` are merged into the workflow. All other frontmatter fields (`name`, `description`) are metadata only.
- Agents can also be imported from remote repositories: `owner/repo/.github/agents/agent.agent.md@v1.0.0`.

## Using in Copilot Chat

- In GitHub Copilot Chat, type `/agent` and select the agent by name.
- The agent prompt is injected as system-level context, shaping how Copilot responds.
- Dispatcher agents (with `disable-model-invocation: true`) route requests to specialized prompts or workflows.

## Naming Conventions

- All agent files must use the `*.agent.md` suffix: `security-reviewer.agent.md`, `code-reviewer.agent.md`, `docs-checker.agent.md`.
- Use kebab-case for the base name.
- The `name:` field in frontmatter should be a human-readable title (e.g., `Security Reviewer Agent`).
- The `agentic-workflows.agent.md` file is reserved for the gh-aw dispatcher agent created by `gh aw init`.

## Security

- Never include secrets, tokens, or credentials in agent prompts.
- Do not instruct agents to bypass security controls, disable TLS verification, or ignore errors.
- Agent prompts should reinforce project security standards (e.g., referencing `CODING_STANDARDS.md` security section).
