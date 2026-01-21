from __future__ import annotations

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    try:
        import tomli as tomllib  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment]

THIS_FILE = Path(__file__).resolve()


def _find_upwards(start: Path, marker: str = "pyproject.toml") -> Path:
    """Return the first parent containing ``marker``; raise if none is found."""
    for parent in [start, *start.parents]:
        if (parent / marker).is_file():
            return parent
    logger.debug("%s not found starting at %s", marker, start)
    err = FileNotFoundError(marker)
    if hasattr(err, "add_note"):
        err.add_note(f"search start: {start}")
    raise err


AGENT_ROOT = _find_upwards(THIS_FILE)
PROJECT_ROOT = _find_upwards(AGENT_ROOT.parent)
sys.path.insert(0, str(PROJECT_ROOT))
for src_path in PROJECT_ROOT.glob("agents/*/src"):
    sys.path.insert(0, str(src_path))

project = "python-agent-template"
author = "python-agent-template maintainers"


def _get_project_version(default: str = "0.0.0") -> str:
    """Return the project version from this agent's pyproject.toml, or a default."""
    pyproject_path = AGENT_ROOT / "pyproject.toml"
    if tomllib is None or not pyproject_path.is_file():
        return default

    try:
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
    except OSError as exc:
        logger.warning("Failed to read %s; falling back to default version.", pyproject_path, exc_info=exc)
        return default
    except tomllib.TOMLDecodeError as exc:  # type: ignore[union-attr]
        logger.warning("Failed to parse %s; falling back to default version.", pyproject_path, exc_info=exc)
        return default

    version = data.get("project", {}).get("version") or data.get("tool", {}).get("poetry", {}).get("version")
    return version or default


version = _get_project_version()
release = version

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

try:
    if tomllib is not None:
        # Only enable when the TOML parser (and therefore the extension's deps) is available.
        # Import is intentionally unused; it fails fast if the dependency stack is missing.
        import sphinx_autodoc_typehints

        _ = sphinx_autodoc_typehints  # appease static analyzers about usage
        extensions.append("sphinx_autodoc_typehints")
except Exception:
    logger.warning("sphinx_autodoc_typehints not enabled; dependency stack missing.", exc_info=True)

autosummary_generate = True
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False

# set to ["_templates"] when the directory is added
templates_path: list[str] = []
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path: list[str] = []  # set to ["_static"] when the directory is added
