# Coding Standards

This document describes the coding standards and conventions for developing agents within this monorepo. Adhering to these standards ensures code quality, maintainability, and consistency across different agents.

<!-- Portions inspired by Microsoft's agent-framework CODING_STANDARD.md (MIT): https://github.com/microsoft/agent-framework/blob/main/python/CODING_STANDARD.md -->

## General Naming Conventions

**Prefer explicit and meaningful names.**

Favor meaningful, spelled‑out names for variables, functions, methods, classes, packages, and modules. Avoid abbreviations so intent is obvious without extra context.

For example, instead of `usr_id` or `fmt_msg()`, prefer more descriptive names such as `user_identifier` and `format_message_for_logging()`.

When values represent quantities, include units or domain qualifiers in the name to prevent ambiguity.

_For example, prefer `timeout_seconds`, `max_retries`, or `file_size_bytes` over generic names like `timeout`, `max`, or `size`._

**Mark internal APIs explicitly.**

Use a leading underscore (`_`) for internal helpers that are not part of the public API, and avoid relying on internal names from other modules.

**Use predicate naming for booleans and checks.**

Use clear predicate naming for booleans and checks so conditions read naturally.

_For example, `is_valid`, `has_token`, `can_retry`, `should_refresh`, etc._

**Make directionality explicit for external integrations.**

For methods implementing integration with external services, use descriptive prefixes to clarify directionality:
- `_prepare_<object>_for_<purpose>` for shaping payloads before sending.
- `_parse_<object>_from_<source>` for normalizing/decoding incoming responses.

## General Coding Conventions

**Prioritize simplicity and readability.**

Always respect the [KISS principle](https://en.wikipedia.org/wiki/KISS_principle). Write code that is easy to read and understand. Avoid clever tricks or complex constructs that may confuse future maintainers.

**Document intent, not mechanics.**

Document non-obvious or surprising behavior with comments and docstrings. Explain the "why" behind decisions, not just the "what". Always update public-facing docs when behavior, configuration, or defaults change.

**Design for failure and clarity.**

When implementing features, consider edge cases and failure modes. Validate inputs and fail fast with clear error messages. Avoid silent failures or ambiguous states.

**Treat configuration as a public contract.**

Treat configuration as part of the public contract: validate it, document defaults, and fail fast on invalid values.

**Handle configuration and secrets safely.**

Never hardcode secrets, tokens, credentials, or service endpoints in source code.
Load them from environment variables, secret stores, or configuration objects instead.

Document all required configuration keys and environment variables in README files or public documentation. Provide defaults only when they are safe and explicitly documented.

When logging, never emit secrets or sensitive data. Mask or strip confidential fields, and avoid logging full request or response payloads if they may contain secrets or personally identifiable information (PII).

**Follow the Clean Code Essentials.**

Code should follow the [Clean Code Essentials](#clean-code-essentials) defined below, favoring clarity, single responsibility, and explicit behavior over compactness or cleverness.

**Validate behavior with tests.**

Use a test-driven approach. First, write tests that cover happy paths, edge cases, and error conditions. Ensure tests are isolated, deterministic, and fast. Tests must follow the [Testing Conventions](#testing-conventions) defined below. Then implement the feature to make the tests pass.

## Clean Code Essentials

**Keep functions and methods single-purpose.**

Keep functions and methods focused on a single responsibility. A function/method should do one thing well; if it begins to branch into multiple concerns (validation, transformation, persistence, logging), extract helpers with clear names so each unit remains easy to read and test.

**Prefer guard clauses over nesting.**

Prefer guard clauses to keep control flow flat and readable. Return early for invalid inputs or trivial cases instead of nesting conditions deeply.
For example, prefer:

```python
def create_user(email: str) -> User:
    if not email:
        raise ValueError("email must be provided")
    if "@" not in email:
        raise ValueError("email must be a valid address")
    return User(email=email)
```

over deeply nested `if/else` blocks that obscure the happy path.

**Avoid boolean mode flags.**

Avoid boolean mode flags in APIs because they make call sites ambiguous and encourage feature creep. Feature creep is the gradual, unchecked addition of new capabilities or options to a function, method, or API, often without a clear need or cohesive design, increasing complexity and reducing clarity over time.

When behavior changes meaningfully, prefer separate functions, explicit parameters, or a strategy/enum-like approach so intent is obvious at the call site.

For example, prefer `parse_strict()` and `parse_lenient()` (or distinct strategies) rather than `parse(data, strict=True)` when the behavior diverges significantly.

**Minimize side effects and mutability.**

Minimize hidden side effects and mutability. Avoid mutable defaults, limit in-place mutation, and return new data when practical. If a function intentionally mutates inputs or relies on shared state, document it explicitly to prevent surprising behavior.
For example, avoid:

```python
def add_tag(tag: str, tags: list[str] = []):
    tags.append(tag)
    return tags
```

and instead use:

```python
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    tags = tags or []
    return [*tags, tag]
```

**Make errors actionable and safe.**

Make error messages actionable and safe. Errors should explain what failed, include relevant identifiers, and suggest how to fix the issue. Never include secrets (tokens, passwords, connection strings) in exceptions or logs. Prefer raising precise exception types with clear messages so failures are diagnosable without debugging.

For example, prefer `ValueError("unsupported region 'eu-west-9'; expected one of: ...")` over generic messages like "invalid input".

## Testing Conventions

**Test behavior, not implementation.**

Write tests that validate observable outcomes: return values, state changes, emitted events, and externally visible side effects. Avoid asserting on internal call sequences or private helpers unless the behavior is otherwise unobservable. Tests should act as executable documentation of the contract, not a mirror of the implementation.

**Keep tests isolated, deterministic, and fast.**

Tests must run in any order and on any machine with consistent results. Avoid shared global state, reliance on real time, randomness, network access, or external services in unit tests. When I/O or time is involved, isolate it behind boundaries and substitute controlled inputs so failures are reproducible.

**Organize tests by intent and scope.**

Structure the suite so fast unit tests are the default and slower tests are clearly separated. Keep unit tests focused on pure logic and boundary conditions, and reserve integration tests for validating wiring with real dependencies (databases, filesystems, queues, HTTP services). Use clear categorization (folder structure and/or markers) so different scopes can be executed independently in CI.

**Prefer clear setup via fixtures and builders.**

Use shared setup only when it improves readability and reduces duplication. Prefer small, composable fixtures and explicit test data builders over large, implicit “do-everything” fixtures. Keep the test’s core intent visible at the call site: arrange only what is needed for that behavior.

**Cover happy paths, edge cases, and failure modes.**

For each behavior, include representative success cases, boundary conditions, and error paths. Validate input handling and failure semantics (exception type, message where appropriate, fallback behavior). Prefer parametrized tests when validating the same behavior across multiple inputs to reduce duplication and improve coverage.

**Mock boundaries, not internals.**

Mock external dependencies at the edges of the system (network, database drivers, file I/O, clocks, environment) rather than mocking internal functions. Favor dependency injection and clear interfaces so tests can substitute boundaries without coupling to implementation details.

**Use consistent naming and structure.**

Name test modules `test_*.py`, test functions `test_<behavior>()`, and test classes `Test<ClassOrBehavior>` (without `__init__`) only when grouping improves readability. Use descriptive, behavior-driven names that read naturally and make failures self-explanatory (e.g., `test_rejects_expired_token`, `test_returns_404_when_user_missing`).

**Maintain test suite quality.**

Keep tests readable and focused: avoid complex logic inside tests, prefer direct assertions, and ensure failures provide clear signals. Treat flaky tests as defects: fix, quarantine, or remove them promptly. Run the full test suite regularly in CI and enforce consistent execution across environments.

**Keep test data explicit and close to the test.**

Define test data at the point of use whenever possible. Avoid hiding important behavior or assumptions inside fixtures; fixtures should assemble context, not encode test logic.

**Keep unit tests pure.**

Unit tests must not perform real network calls, database access, or filesystem writes. Such interactions belong to integration tests and must be clearly separated.

## Code Style and Formatting

We use [Ruff](https://github.com/astral-sh/ruff) for both linting and formatting.

>[!NOTE]
> As `fix = true` and `fixable = ["ALL"]` in `[tool.ruff.lint]` section of `pyproject.toml`, running Ruff will automatically fix all fixable issues, so any rule listed below that support an auto-fix will rewrite the code when linting runs.

- **Line length:** 120 characters
- **Target Python version:** 3.10+
- **Google-style docstrings:** All public functions, classes, and modules should have docstrings following Google conventions
<details>
<summary><strong>Ruff rules used for linting</strong></summary>

**Rules enforced:**

- See: [pyproject.toml](./pyproject.toml) `[tool.ruff.lint]`
- [Naming (N)](https://docs.astral.sh/ruff/rules/#pep8-naming-n) — all names follows [PEP8](https://www.python.org/dev/peps/pep-0008/) naming conventions (snake_case functions/vars, CapWords classes, UPPER_SNAKE constants).
- Imports:
    - [I (isort)](https://docs.astral.sh/ruff/rules/#isort-i) — imports are sorted/grouped.
    - [ICN (import conventions)](https://docs.astral.sh/ruff/rules/#flake8-import-conventions-icn) — prefer consistent relative vs absolute imports and avoid pointless aliases.
    - [INP (implicit namespace)](https://docs.astral.sh/ruff/rules/#flake8-no-pep420-inp) — implicit packages should have `__init__.py` file.
- [Docstrings (D)](https://docs.astral.sh/ruff/rules/#pydocstyle-d) — public modules, classes, methods,functions, packages, etc. need docstrings.
- [Quotes (Q)](https://docs.astral.sh/ruff/rules/#flake8-quotes-q) — ensures consistency by using always single or double quote. In our case double quote.
- [Comprehensions (C4)](https://docs.astral.sh/ruff/rules/#flake8-commas-com) — flags unnecessary list/set/dict comprehensions; prefer simpler expressions so the code is more readable.
- [Async (ASYNC)](https://docs.astral.sh/ruff/rules/#flake8-async-async) — flags bad async/await patterns.
- [Returns (RET)](https://docs.astral.sh/ruff/rules/#flake8-return-ret) — ensures consistent return statements.
- [Exceptions (TRY)](https://docs.astral.sh/ruff/rules/#tryceratops-try) — checks consistency in exception handling.
- [Raise parentheses (RSE)](https://docs.astral.sh/ruff/rules/#flake8-raise-rse) — checks for unnecessary parentheses on raised exceptions.
- [Simplifications (SIM)](https://docs.astral.sh/ruff/rules/#flake8-simplify-sim) — keeps code simple for boolean/logical expressions, if statements, for loops, return statements.
- [Modernizations (UP)](https://docs.astral.sh/ruff/rules/#pyupgrade-up) — upgrades syntax to modern Python.
- [Formatting basics (E, W)](https://docs.astral.sh/ruff/rules/#pycodestyle-e-w) — checks some [PEP8](https://www.python.org/dev/peps/pep-0008/) conventions mainly on whitespace/spacing/line break.
- [Pyflakes (F)](https://docs.astral.sh/ruff/rules/#pyflakes-f) — [Pyflakes](https://github.com/PyCQA/pyflakes) checks like unused imports/vars, undefined names, etc.
- [Pylint-style (PLC/PLE/PLR/PLW)](https://docs.astral.sh/ruff/rules/#pylint-pl) — [Pylint](https://pylint.pycqa.org/) checks for code smell, complexity, bad builtins, etc.
- [Bug risks (B)](https://docs.astral.sh/ruff/rules/#flake8-bugbear-b) — checks common bug patterns and potential design issues with bug bear.
<!-- - [Copyright (CPY)](https://docs.astral.sh/ruff/rules/#flake8-copyright-cpy) — enforces copyright headers. -->
- [Datetime TZ (DTZ)](https://docs.astral.sh/ruff/rules/#flake8-datetimez-dtz) — datetime should always used with timezone.
- [Implicit string concat (ISC)](https://docs.astral.sh/ruff/rules/#flake8-implicit-str-concat-isc) — checks implicit explicit string concatenation issues.
- [pygrep-hooks (PGH)](https://docs.astral.sh/ruff/rules/#pygrep-hooks-pgh) — checks `noqa` and `type: ignore` annotations. Checks also invalid mock access.
- [Pytest style (PT)](https://docs.astral.sh/ruff/rules/#flake8-pytest-style-pt) — checks commom issues and inconsistencies in pytest-based tests.
- [Security (S)](https://docs.astral.sh/ruff/rules/#flake8-bandit-s) — use [Bandit](https://bandit.readthedocs.io/en/latest/) to find some security issues.
- [TODO/FIXME hygiene (TD)](https://docs.astral.sh/ruff/rules/#td-flake8-todos) — ensures TODO are properly formatted and linked to an issue.
- [FIX](https://docs.astral.sh/ruff/rules/#flake8-fixme-fix) — flags FIX/FIXME/XXX/TODO comment patterns.
- [Debugger (T10)](https://docs.astral.sh/ruff/rules/#flake8-debugger-t10) — check for the presence of debugger call and import statements.
- [Print (T20)](https://docs.astral.sh/ruff/rules/#flake8-print-t20) — flags `print` and `pprint` statements so they can be replaced with logging.
- [Ruff-specific (RUF)](https://docs.astral.sh/ruff/rules/#ruff-specific-rules-ruf) — check Ruff specific rules.
- [Eradicate commented-out code (ERA)](https://docs.astral.sh/ruff/rules/#eradicate-era) — removes dead/commented code.

**Rules ignored globally:**

- See: [pyproject.toml](./pyproject.toml) `[tool.ruff.lint]`
- [D100](https://docs.astral.sh/ruff/rules/d100/) — allows missing docstring in public modules.
- [D104](https://docs.astral.sh/ruff/rules/d104/) — allows missing docstring in public packages.
- [D418](https://docs.astral.sh/ruff/rules/d418/) — allows overload functions to have a docstring.
- [TD003](https://docs.astral.sh/ruff/rules/td003/) — allows TODOs with missing issue's link.
- [FIX002](https://docs.astral.sh/ruff/rules/fix002/) — allows TODO markers, i.e. allows only TODO markers.
- [B027](https://docs.astral.sh/ruff/rules/b027/) — allows empty non-abstract methods in abstract base classes.  We sometimes keep optional hooks in [ABCs](https://docs.python.org/3/library/abc.html) as concrete no-ops so subclasses can override them when needed without being forced to.
    ```python
    from abc import ABC, abstractmethod

    class PipelineStep(ABC):
        @abstractmethod
        def run(self, payload: dict) -> dict:
            """Required: transform payload."""

        def before_run(self, payload: dict) -> dict:
            """Optional hook: tweak input before run."""
            return payload  # default no-op

        def after_run(self, payload: dict) -> dict:
            """Optional hook: tweak output after run."""
            return payload  # default no-op
    ```

**Rules ignored per-file:**

- See: [pyproject.toml](./pyproject.toml) `[tool.ruff.lint.per-file-ignores]`
- Tests (`**/tests/**`):
    - [S101](https://docs.astral.sh/ruff/rules/s101/) — allows plain `assert` in tests (blocked elsewhere because `-O` strips them at runtime).
    - [PLR2004](https://docs.astral.sh/ruff/rules/plr2004/) — allows magic numbers in tests to keep fixtures/expectations concise.
- Notebooks (`*.ipynb`):
    - [CPY](https://docs.astral.sh/ruff/rules/cpy001/) — skips copyright headers in notebooks.
    - [E501](https://docs.astral.sh/ruff/rules/e501/) — relaxes line-length in notebooks to avoid breaking rendered cells.
</details>


## Function Parameter Guidelines

To make the code easier to use and maintain, follow these parameter guidelines:

- **Positional parameters:** Only use positional parameters for up to three fully expected parameters. Beyond that, the ordering becomes non-obvious and error-prone.
- **Keyword parameters:** Use keyword-only parameters for all other parameters, especially when there are multiple required parameters without obvious ordering.
- **Avoid additional imports:** Do not require users to import additional modules just to use your function. This matters even for packaged agents as configuration may come from env vars as strings; accept strings plus the enum and normalize once at the boundary. For instance, instead of forcing callers to import an enum:

    ```python
    def create_agent(name: str, api_provider: ApiProvider, model: str, kwargs: dict[str, object]) -> Agent:
        # Implementation here
    ```

    Do this instead:

    ```python
    def create_agent(
        name: str,
        *,
        api_provider: Literal["azure-openai", "openai"] | ApiProvider,
        model: str,
        client_kwargs: dict[str, object],   # api client options
        tool_kwargs: dict[str, object],     # tool registry/config options
        trace_kwargs: dict[str, object],    # tracing/telemetry options
    ) -> Agent:
        """Create an agent, normalizing provider strings/env into enums and separating kwargs buckets."""
        if isinstance(api_provider, str):
            api_provider = ApiProvider(api_provider)
        # Implementation here
    ```

- **Document kwargs:** Always document how `kwargs` are used, either by referencing external documentation or explaining their purpose.
- **Separate kwargs:** When combining kwargs for multiple purposes, use specific parameters like `client_kwargs: dict[str, Any]` instead of mixing everything into `**kwargs` (cf. example above).

## Imports and Module Layout

Keep imports sorted by Ruff, which groups them as standard library, third-party, and first-party imports. Avoid deep relative imports that cross agent boundaries—instead, rely on the namespace package `python_agent_template.agents.<agent>` for clarity and maintainability.

Re-export public symbols in each agent's `__init__.py` to provide a clean public API, and keep internal modules private. Watch out for circular imports; when they occur, move shared types or utilities into dedicated modules to break the cycle.

## Package Structure and Public API

See [DEVELOPMENT.md](DEVELOPMENT.md) for the full monorepo layout and development guide.

The agents follow a specific layout to ensure consistency and ease of development. Each agent is located under `agents/<agent>/` and has the following structure:

```
Repo root
(...)
├─ agents/
│  └─ <agent>/
│     ├─ src/<project-name>/agents/<agent>/    # agent code (entrypoint, core logic)
│     ├─ tests/                                # agent tests
│     ├─ docs/
│     │  ├─ source/                            # Sphinx sources
│     │  └─ generated/                         # built HTML (do not edit)
│     ├─ Dockerfile                            # build agent container image
│     ├─ pyproject.toml                        # agent-specific deps/tasks/metadata
│     └─ LICENSE                               # agent-specific license
(...)
```

Each agent lives under the `agents/<agent>/` directory and is fully self-contained. The agent’s code is located in `src/python_agent_template/agents/<agent>/` and is accompanied by its own tests, documentation, Dockerfile, `pyproject.toml`, and license file. This structure ensures that each agent can be developed, tested, packaged, and released independently.

Shared documentation is maintained centrally using Sphinx. Common documentation sources live under `docs/source/`, while generated documentation is written to `docs/generated/`. Generated documentation is read-only and must never be edited manually.

The repository uses namespace packages, meaning no `__init__.py` files are present at shared root levels. Each agent exports its own public API exclusively from its dedicated package, without relying on implicit package initialization.

Agent code is namespaced under `python_agent_template.agents.<agent>`, following PyPA namespace package guidance. This namespace is composed of the project root namespace, the `agents` sub-namespace, and the agent name. To ensure imports, packaging, and tooling behave correctly, agent code must be placed under `src/python_agent_template/agents/<agent>/` to match this namespace exactly.

Each agent’s public surface must remain minimal and intentional. Internal helpers, wiring code, and implementation details should not be exposed as part of the public API. When appropriate, prefer factories or builder functions over exposing raw implementation classes, so the external contract remains stable even as internal structure evolves.

## Asynchronous Programming

Prefer asynchronous implementations because agents are mostly I/O-bound (network calls, streaming, tool invocations). Implementing synchronously limits scalability and responsiveness and leads to blocking behavior.

You should always assume everything is asynchronous by default. Use the function signature with either `async def` or `def` to understand if something is asynchronous or not.

Default to `async def` for I/O-bound code paths. If you need to provide synchronous versions, create thin sync shims that delegate to the async implementations rather than duplicating logic.

Never block the event loop with CPU-bound work or blocking I/O. Offload such work to executors, or use async-native clients when available. Propagate cancellation promptly—do not swallow `CancelledError` unless you re-raise it.

Prefer `asyncio.TaskGroup` or `gather` with `return_exceptions=False` unless you have a clear strategy for error aggregation.

## Subprocesses and External Calls

When calling subprocesses, avoid `shell=True` to prevent shell injection vulnerabilities. Instead, pass argument lists directly to `subprocess` functions:

```python
# ✅ Preferred
subprocess.run(["git", "status"], check=True)

# ❌ Avoid
subprocess.run("git status", shell=True)
```

Validate any untrusted inputs (user-provided data, config/env values, webhooks, queue messages, tool or model outputs) that influence subprocess arguments or external API requests. Set timeouts on network and subprocess calls where feasible to avoid unbounded waits that can hang your application.

## Performance Considerations

### Cache Expensive Computations

Think about caching where appropriate. Cache the results of expensive operations that are called repeatedly with the same inputs:

```python
# ✅ Preferred - cache expensive computations
class AIFunction:
    def __init__(self, ...):
        self._cached_parameters: dict[str, Any] | None = None

    def parameters(self) -> dict[str, Any]:
        """Return the JSON schema for the function's parameters.

        The result is cached after the first call for performance.
        """
        if self._cached_parameters is None:
            self._cached_parameters = self.input_model.model_json_schema()
        return self._cached_parameters

# ❌ Avoid - recalculating every time
def parameters(self) -> dict[str, Any]:
    return self.input_model.model_json_schema()
```

### Prefer Attribute Access Over isinstance()

When checking types in hot paths, prefer checking a `type` attribute (fast string comparison) over `isinstance()` (slower due to method resolution order traversal):

```python
# ✅ Preferred - type attribute comparison
if content.type == "function_call":
    # handle function call

# ❌ Avoid in hot paths - isinstance() is slower
if isinstance(content, FunctionCallContent):
    # handle function call
```

### Avoid Redundant Serialization

When the same data needs to be used in multiple places, compute it once and reuse it:

```python
# ✅ Preferred - reuse computed representation
payload = message.to_dict()
logger.info("sending", extra={"payload": payload})
queue.put(payload)

# ❌ Avoid - computing the same thing twice
logger.info(message.to_dict())
queue.put(message.to_dict())
```

Move work that does not change outside loops so it runs once. Reuse clients and other heavy objects instead of creating them for every call. Avoid copying large payloads when you can safely pass references or iterators. Keep optional instrumentation behind a quick check so skipping it is cheap.

## Documentation

We follow the [Google Docstring](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#383-functions-and-methods) style guide for functions and methods. Docstrings are required for all public APIs but can be omitted for private functions when they're self-evident.

Docstrings should contain (always include #1; include other sections only when applicable):

1. **Single-line summary:** A concise explanation of what the function does, ending with a period. Always include this. Add a blank line after the summary before any extended description.
2. **Extended description:** Explain non-obvious behavior, guarantees, or edge cases (not implementation mechanics). Add this only when it clarifies intent.
3. **Args section:** Specify arguments after an `Args:` header, with each argument in the format:
   - `arg_name`: Explanation of the argument.
   - Longer explanations can continue on the next line, indented by 4 spaces.
    - Do not restate type hints. Mention a default only when it is important to the contract (and keep it in sync when the default changes).
4. **Keyword-only arguments section:** Similar format to `Args:` but for keyword-only parameters (those after `*`).
5. **Returns/Yields section:** Explain what the function returns or yields.
6. **Raises section:** Include only when it adds value (project-specific exceptions or non-obvious cases). Skip obvious exceptions like `ValueError` or `TypeError` unless the context is non-obvious.
7. **Examples section:** Provide usage examples using `.. code-block:: python`.

At minimum, a docstring looks like this:

```python
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same."""
    ...
```

A complete version includes more detail:

```python
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same.

    Here is extra explanation of the logic involved.

    Args:
        arg1: The first string to compare.
        arg2: The second string to compare.

    Returns:
        True if the strings are the same, False otherwise.
    """
    return arg1 == arg2
```

A more complete example with keyword arguments and code samples:

```python
def create_client(
    model_id: str | None = None,
    *,
    timeout: float | None = None,
    env_file_path: str | None = None,
    **kwargs: Any,
) -> Client:
    """Create a new client with the specified configuration.

    Args:
        model_id: The model ID to use. If not provided,
            it will be loaded from settings.

    Keyword Args:
        timeout: Optional timeout for requests.
        env_file_path: If provided, settings are read from this file.
        kwargs: Additional keyword arguments passed to the underlying client.

    Returns:
        A configured client instance.

    Raises:
        ValueError: If the model_id is invalid.

    Examples:
        .. code-block:: python

            # Create a client with default settings:
            client = create_client(model_id="gpt-4o")

            # Or load from environment:
            client = create_client(env_file_path=".env")
    """
    ...
```

Keep READMEs, quickstarts, and Sphinx sources aligned with actual behavior. Do not edit generated docs under `docs/generated` or `agents/*/docs/generated`—these are built automatically by the documentation workflow.

Code samples in documentation should be runnable and, where practical, pass Ruff and Pyright checks. Docstrings should explain intent and nuances rather than simply restating type hints.

## Pull Requests and Reviews

Keep pull request diffs focused and cohesive. Update tests and documentation alongside code changes so reviewers can see the complete picture. Call out breaking changes explicitly in the PR description.

Before requesting review, run the full project quality gate to ensure formatting, linting, type checking, security scanning, and tests all pass locally (see DEVELOPMENT.md for the current command).

Prefer small, reviewable commits that tell a clear story. Avoid mixing refactors with functional changes unless they're tightly coupled—it makes reviews easier and safer.
