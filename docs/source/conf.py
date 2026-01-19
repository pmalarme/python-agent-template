from __future__ import annotations

import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    try:
        import tomli as tomllib  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
for src_path in PROJECT_ROOT.glob("agents/*/src"):
    sys.path.insert(0, str(src_path))

project = "python-agent-template"
author = "python-agent-template maintainers"


def _get_project_version(default: str = "0.0.0") -> str:
    """Return the project version from pyproject.toml, or a default."""

    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    if tomllib is None or not pyproject_path.is_file():
        return default

    try:
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
    except Exception:
        return default

    version = (
        data.get("project", {}).get("version")
        or data.get("tool", {}).get("poetry", {}).get("version")
    )
    return version or default


version = _get_project_version()
release = version

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

autosummary_generate = True
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path = ["_static"]
