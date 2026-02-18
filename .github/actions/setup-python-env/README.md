# Setup Python Environment

Composite GitHub Action that sets up [uv](https://docs.astral.sh/uv/) with a
specific Python version and installs project dependencies via `uv sync`.

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `python-version` | No | `"3.13"` | Python version to install (e.g. `"3.13"`, `"3.10"`). |
| `include-docs` | No | `"false"` | When `"true"`, adds `--group docs` to install Sphinx and related packages. |
| `extra-args` | No | `""` | Additional arguments appended to the `uv sync` command. |

The base command is always `uv sync --all-extras --dev`. The `include-docs` flag
and `extra-args` extend it.

## Usage

### Minimal (defaults to Python 3.13)

```yaml
- uses: ./.github/actions/setup-python-env
```

### With a Python version matrix

```yaml
- uses: ./.github/actions/setup-python-env
  with:
    python-version: ${{ matrix.python-version }}
```

### Including docs dependencies

```yaml
- uses: ./.github/actions/setup-python-env
  with:
    include-docs: "true"
```

### With extra sync arguments

```yaml
- uses: ./.github/actions/setup-python-env
  with:
    include-docs: "true"
    extra-args: "--all-packages -U --prerelease=if-necessary-or-explicit"
```
