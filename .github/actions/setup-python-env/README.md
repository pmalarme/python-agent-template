# Setup Python Environment

Composite GitHub Action that sets up [uv](https://docs.astral.sh/uv/) with a
specific Python version and installs project dependencies via `uv sync`.

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `python-version` | No | `"3.13"` | Python version to install (e.g. `"3.13"`, `"3.10"`). |
| `include-docs` | No | `"false"` | When `"true"`, adds `--group docs` to install Sphinx and related packages. |
| `extra-args` | No | `""` | Additional arguments appended to the `uv sync` command. Must be a trusted, static flag string — see [Security note](#security-note) below. |

The base command is always `uv sync --all-extras --dev`. The `include-docs` flag
and `extra-args` extend it.

## Security note

`extra-args` is passed to `uv sync` via an environment variable and intentionally
word-split so that callers can supply multiple flags (e.g.
`--all-packages --prerelease=if-necessary-or-explicit`). Because of this word
splitting, **only hardcoded, static strings should be used**. Never pass
dynamic values sourced from issue bodies, PR descriptions, user-controlled
inputs, or any other external source, as those could introduce unexpected `uv
sync` flags and alter environment resolution behaviour.

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
