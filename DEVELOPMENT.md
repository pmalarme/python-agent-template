# Development Setup and Guide

<!-- Portions inspired by Microsoft's agent-framework DEV_SETUP.md (MIT): https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md -->

This guide covers:
- How to set up your development environment with Python and uv.
- A guide on how to use this repo, work on agents and run common tasks.

This is a monorepo hosting multiple Python-based agents. Each agent is an isolated package under `agents/<agent>/`, with its own code, tests, docs, and LICENSE. At the root, we defined GitHub Actions workflows, shared scripts, and Poe tasks that run across all agents so the development experience is consistent and efficient.

## Development Setup

For development, we recommend to use [Python 3.13](https://www.python.org/downloads). A complete definitions of the coding standard and conventions are available in [CODING_STANDARDS.md](CODING_STANDARDS.md).

Among the agents and for the project root we are using two main tools:
- [uv](https://github.com/astral-sh/uv) for Python version and virtual environment management, dependency installation, and task running.
- [poethepoet](https://github.com/nat-n/poethepoet) for running repeatable tasks like formatting, linting, testing, and documentation. Main poe tasks are explained at the end of this guide in section [Dev guidelines > Poe tasks](#poe-tasks).

### Development on WSL

If you are using Windows Subsystem for Linux (WSL), follow these additional recommendations:
- Clone the repository in your Linux home (for example `~/workspace`), not `/mnt/c/`, to avoid slow I/O.
- Ensure that the WSL extension for VS Code is installed.

### Install uv

uv allows to easily manage Python versions and virtual environments. Follow the instructions below to install it on your system. Check the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) for complete and up-to-date instructions.

#### Windows (non-WSL)

For Windows, install uv via PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

or via WinGet:

```powershell
winget install --id=astral-sh.uv  -e
```

or via Scoop:

```powershell
scoop install main/uv
```

#### Linux and WSL

Install uv via the shell script (`curl` required):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### MacOS

For MacOS, install uv via the shell script (`curl` required):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or via Homebrew:

```sh
brew install uv
```

or using MacPorts:

```sh
sudo port install uv
```

#### PyPI

Alternatively, you can install with PyPI:

```sh
pipx install uv
```
or
```sh
pip install uv
```

### Setup the Project

To set up the project, run the following command from the repo root:

```sh
uv run poe setup
```

This will create a virtual environment in `.venv/`, install all dependencies, and set up pre-commit hooks. If you want to specify a Python version, use the `-p` flag, for example:

```sh
uv run poe setup --python 3.13
```

The default version for the setup Poe task is Python 3.13 and defined in [pyproject.toml](../pyproject.toml) under `[tool.poe.tasks.setup]`.

### VS Code Setup

Install the following extensions for VS Code:
- [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) by Microsoft who provides rich support for Python development.
- [Pylance extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) by Microsoft which offers performant language support for Python, including type checking.
- [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) by Charlie Marsh which integrates the Ruff linter into VS Code.
- [Code Spell Checker extension](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker) by Street Side Software which helps to catch common spelling errors in code and documentation.

All these extensions are also recommended in the [.vscode/extensions.json](../.vscode/extensions.json) file.

Open the repo in VS Code, run the command "Python: Select Interpreter," and choose the `.venv` interpreter created by uv. This ensures that linting, type checking, and testing use the same environment as defined for the project.

## Development Guide

This guide explains how to work on the repo, run agents, and perform common tasks. It also provides a section to explains how to work with VS Code.

### Monorepo layout

This solution is a monorepo hosting multiple Python-based agents. Each agent is designed to be independent and can be developed, tested, and deployed separately. This is the structure of the monorepo:

```
Repo root
├─ .github/                                    # workflows, instructions, templates
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
├─ docs/
│  ├─ source/                                  # unified Sphinx sources
│  ├─ generated/                               # built HTML (do not edit)
│  └─ manual/                                  # manual guides
├─ scripts/                                    # shared helpers for tasks/CI
│  ├─ check_md_code_blocks.py                  # lint python fences in markdown
│  ├─ generate_docs.py                         # build unified and per-agent docs
│  ├─ run_tasks_in_agents_if_exists.py         # dispatch Poe tasks to all agents
│  ├─ run_tasks_in_changed_agents.py           # dispatch Poe tasks to changed agents
│  └─ utils/
│     └─ task_utils.py                         # task discovery helpers
├─ .pre-commit-config.yaml                     # pre-commit hooks
├─ CODING_STANDARDS.md                         # coding standards
├─ CONTRIBUTING.md                             # contribution guide
├─ DEVELOPMENT.md                              # this guide
├─ LICENSE                                     # root license
├─ pyproject.toml                              # root config, deps, tasks
├─ README.md                                   # project overview
└─ shared_tasks.toml                           # shared Poe tasks
```

### Poe Tasks

This project uses [poethepoet](https://github.com/nat-n/poethepoet) to define and run common tasks. Below is a complete documentation of the tasks available at root level and defined in `pyproject.toml`.

#### Setup and Installations

This first group of Poe tasks are related to setting up the development environment and installing dev dependencies.

##### setup

To set up the development environment, run:

```sh
uv run poe setup
```

This task creates or refreshes the virtual environment in `.venv/`, installs all dependencies, and sets up pre-commit hooks. You can specify a Python version with the `--python` flag.

It is a sequence of the following Poe tasks:

- [venv](#venv)
- [install](#install)
- [pre-commit-install](#pre-commit-install)

##### venv

Create or refresh the virtual environment in `.venv/` using the specified Python version (default is 3.13):

```sh
uv run poe venv
```

To specify a different Python version, use the `--python` flag:

```sh
uv run poe venv --python 3.12
```

This is useful to switch Python versions for the project.

##### install

Install all dependencies including dev dependencies and all extras, upgrade to satisfy constraints, allow prereleases if necessary or explicit, and skip the docs group:

```sh
uv run poe install
```

##### pre-commit-install

Set up pre-commit hooks:

```sh
uv run poe pre-commit-install
```

This installs the pre-commit hooks defined in [.pre-commit-config.yaml](../.pre-commit-config.yaml) to run before each commit. If you have some issues with the pre-commit hooks, you can run them in a terminal using the following command:

```sh
uv run pre-commit run --all-files
```

#### Check and Quality Gates

This second group of Poe tasks are related to code quality, formatting, linting, type checking, security scanning, and testing. They are designed to run against the different agents, `/docs/source` and `/scripts` directories. It also checks code in markdown files.

##### check

Run all quality checks including formatting, linting, type checking, security scanning, and tests:

```sh
uv run poe check
```

It is a sequence of the following Poe tasks:

- [fmt](#fmt-format)
- [lint](#lint)
- [pyright](#pyright)
- [mypy](#mypy)
- [markdown-code-lint](#markdown-code-lint)
- [bandit](#bandit)
- [test](#test)

##### fmt (format)

Format code using Ruff:

```sh
uv run poe fmt
```

##### lint

Lint code using Ruff:

```sh
uv run poe lint
```

##### pyright

Run Pyright for type checking:

```sh
uv run poe pyright
```

##### mypy

Run Mypy for type checking:

```sh
uv run poe mypy
```

##### markdown-code-lint

Lint Python code blocks in markdown files:

```sh
uv run poe markdown-code-lint
```

The markdown-code-lint task uses the `scripts/check_md_code_blocks.py` script to find all Python code blocks in markdown files under `docs/manual/`, `.github/instructions/`, and each agent's `README.md`, and runs Pyright and Ruff on them to ensure code quality and consistency.

##### bandit

Run Bandit for security scanning:

```sh
uv run poe bandit
```

It runs on `scripts/`, `docs/source/`, and all agents' source code.

##### test

Run tests sequentially for each agent using the `test` task of the agent.

```sh
uv run poe test
```

##### pre-commit-check

Run partial checks for pre-commit:

```sh
uv run poe pre-commit-check [--files <file1> <file2> ...]
```

>[!NOTE]
> Use this as the fast path on changed files; during iteration combine with agent-scoped runs (e.g., `uv run poe -C agents/<agent> check`) for the areas you touched.
>
> Before pushing, run the full `uv run poe check` to mirror CI.
>
> If runtimes grow, we can add more diff-scoped tasks or parallelize per-agent runs.

It runs the following Poe tasks:

- [fmt](#fmt-format)
- [lint](#lint)
- [pre-commit-pyright](#pre-commit-pyright) limited to given file arguments
- [pre-commit-markdown-code-lint](#pre-commit-markdown-code-lint) limited to given file arguments

It is designed to be fast and give quick feedback before committing code. It provides an argument to limit the checks to specific files. This argument is used to run pyright and markdown-code-lint only on the files that are staged for commit.

> Both pre-commit-pyright and pre-commit-markdown-code-lint Poe tasks should be used only via this pre-commit-check task.

#### Documentation

This third group of Poe tasks are related to building the documentation using Sphinx.

>[!IMPORTANT]
> This should be used only to fix/improve documentation generation. The documentation should not be pushed to the repository as it is built and published automatically via GitHub Actions.

##### docs-install

Install documentation dependencies:

```sh
uv run poe docs-install
```

##### docs

Build all documentation (unified and per-agent):

```sh
uv run poe docs
```

### Pre-commit Hooks

The setup of the pre-commit hooks is done during the [setup](#setup) or using the [pre-commit-install](#pre-commit-install) Poe task.

The pre-commit hooks are configured in the [.pre-commit-config.yaml](../.pre-commit-config.yaml) file and serve as a first line of defense to catch common issues before code is committed and pushed to the repository.

They run the following checks and formatting before each commit:
- Strips trailing whitespace
- Ensures there is a final newline at the end of files
- Normalizes line ending to LF
- Validates YAML, TOML and JSON
- Parses Python for syntax errors (AST check)
- Checks that debug statements (e.g., pdb.set_trace()) are not present
- Updates code to modern Python 3.10+ syntax automatically
- Runs [pre-commit-check](#pre-commit-check) Poe task
- Runs security check using Bandit with the config defined in the root `pyproject.toml`
- Parses Python code inside Jupyter Notebook to ensure there are no syntax errors (AST check)
- Updates root `uv.lock` if the root `pyproject.toml` changed

### Working in VS Code

In VS Code, it is possible to debug an agent and run Poe tasks using the integrated terminal and task runner.

#### Extensions' Settings

During the setup, several extensions are recommended to enhance the development experience. A configuration of these extensions is available in `/.vscode/settings.json`. It provides auto-formatting using Ruff on save, linting, and type checking using Pylance.

#### Code Debugging

If you need to debug an agent or a script, in `/.vscode/launch.json` there are pre-defined launch configurations for debugging an agent or a script.

You can debug current file using `Python Debugger: Current File`. It launches and runs the current file under debugpy with the current Python interpreter selected in VS Code.

You can also attach an already running process that was started with debugpy listening on `localhost:5678` using `Python Attach`.

#### VS Code Tasks

Most of the [Poe tasks](#poe-tasks) are also available as VS Code tasks defined in `/.vscode/tasks.json`. You can run them using the command palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and searching for `Run Task`.

### Working on an Agent

An agent is an independent package under `agents/<agent>/`. Each agent has its own lifecycle, codebase, tests, and documentation. Here are some guidelines on how to work on an agent.

#### Namespace and Agent Layout

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

The src are in `src/<project-name>/agents/<agent>/` where `<project-name>/agents/<agent>` is the namespace of the agent. It follows [PyPA guidance](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/) for namespace packages. It is composed of 3 parts:

- `<project-name>`: the root namespace for the project (e.g., `python_agent_template`). It is usually the name of the repository and it is also defined in root `pyproject.toml` under `[project]` name.
- `agents`: the sub-namespace for all agents.
- `<agent>`: the specific agent namespace.

#### Agent Development Workflow

When working on an agent, follow these steps:

- Set up the development environment once at the root using `uv run poe setup`.
- Check `agents/<agent>/pyproject.toml` for agent-specific dependencies, tasks, and metadata:
  - Update the metadata (name, description, URLs) if needed.
  - Adjust the `tool.flit.module` to match the agent's namespace.
  - Modify the `tool.poe.tasks` section to customize tasks like bandit target and coverage target.
  - Check Bandit configuration under `[tool.bandit]`.
  - Check MyPy configuration under `[tool.mypy]`.
- Update the code under `agents/<agent>/src/<project-name>/agents/<agent>/`.
- Add or update tests under `agents/<agent>/tests/`.
- Run the checks for that agent using: `uv run poe check` from the agent directory or `uv run poe -C agents/<agent> check` from the root.
- Run the agent using: `uv run <agent> [args]` from the agent directory or `uv run --package <agent> <agent> [args]` from the root.
- Check that the agent is running properly and that the changes are working as expected.
- Commit and push your changes in a feature branch and open a pull request for review.
