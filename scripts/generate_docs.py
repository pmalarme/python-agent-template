"""Generate HTML docs for all agents using Sphinx (autodoc + napoleon).

How the paths are used:
- ``root``: repository root override (default: this repo root).
- ``agent-source``: agent-local Sphinx source (relative to each agent dir) or absolute.
- ``agent-output``: agent-local build output (relative to each agent dir) or absolute.
- ``unified-source``: shared Sphinx source for the combined site (default ``docs/source``).
- ``unified-output``: shared build output for the combined site (default ``docs/generated``).

Flags:
- ``--agents-only`` / ``--unified-only`` toggle which sites are built (default: build both).
- ``--agents`` limits per-agent builds to the named agent directories.
"""

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT License. See:
#   https://github.com/microsoft/agent-framework/blob/main/LICENSE
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import annotations

import argparse
import os
import shutil
import subprocess  # nosec B404 - subprocess used to invoke sphinx-build with controlled args
import sys
import logging
from pathlib import Path

import tomli
from utils.task_utils import discover_projects

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logger = logging.getLogger(__name__)
SPHINX_MISSING_MSG = "sphinx-build not found on PATH; install docs dependencies (uv sync --group docs)."


def clean_autosummary(source_dir: Path) -> None:
    """Remove sphinx-autosummary cache so nav stays in sync."""

    autosummary_dir = source_dir / "_autosummary"
    if autosummary_dir.exists():
        shutil.rmtree(autosummary_dir)


def load_module_name(agent_dir: Path) -> str:
    """Return the importable module name for an agent.

    Prefers the ``name`` field in the ``[tool.flit.module]`` table (used in this
    repo) and falls back to ``project.name`` if not set.
    """

    pyproject = agent_dir / "pyproject.toml"
    if not pyproject.is_file():
        return agent_dir.name

    try:
        text = pyproject.read_text(encoding="utf-8")
        data = tomli.loads(text)
    except tomli.TOMLDecodeError:
        logger.warning(
            "Failed to parse pyproject.toml in %s; falling back to directory name.",
            agent_dir,
            exc_info=True,
        )
        return agent_dir.name
    except OSError:
        logger.warning(
            "Failed to read pyproject.toml in %s; falling back to directory name.",
            agent_dir,
            exc_info=True,
        )
        return agent_dir.name

    module = data.get("tool", {}).get("flit", {}).get("module", {}).get("name")
    if module:
        return module
    return data.get("project", {}).get("name", agent_dir.name)


def ensure_sphinx_available() -> None:
    """Raise a helpful error if sphinx-build is not on PATH."""

    if shutil.which("sphinx-build") is None:
        raise FileNotFoundError(SPHINX_MISSING_MSG)


def build_agent_docs(
    root: Path,
    agents: list[Path],
    source: Path,
    output: Path,
    env: dict[str, str],
) -> None:
    """Build docs for each agent into its own output directory."""
    if logger.isEnabledFor(logging.INFO):
        modules = [load_module_name(agent_dir) for agent_dir in agents]

        logger.info("Discovered agents:")
        for agent_dir, module in zip(agents, modules):
            logger.info("- %s (module: %s)", agent_dir.name, module)

    for agent_dir in agents:
        source_dir = source if source.is_absolute() else agent_dir / source
        if not source_dir.exists():
            logger.warning("Skipping %s: no docs source at %s", agent_dir.name, source_dir)
            continue

        clean_autosummary(source_dir)

        output_dir = output if output.is_absolute() else agent_dir / output
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "sphinx-build",
            "-b",
            "html",
            str(source_dir),
            str(output_dir),
        ]

        try:
            # Inherit stdout/stderr so Sphinx warnings/errors stream to the console for visibility.
            # Only catch a missing sphinx-build binary; Sphinx build failures propagate so users see the raw error.
            subprocess.run(
                cmd,
                check=True,
                cwd=root,
                env=env,
                stdout=None,
                stderr=None,
            )  # nosec B603 - command args are static and trusted
        except FileNotFoundError as exc:
            raise FileNotFoundError(SPHINX_MISSING_MSG) from exc


def build_unified_docs(
    root: Path,
    source: Path,
    output: Path,
    env: dict[str, str],
) -> None:
    """Build the shared unified doc site."""

    source_dir = source if source.is_absolute() else root / source
    if not source_dir.exists():
        logger.warning("Skipping unified docs: no source at %s", source_dir)
        return

    clean_autosummary(source_dir)

    output_dir = output if output.is_absolute() else root / output
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "sphinx-build",
        "-b",
        "html",
        str(source_dir),
        str(output_dir),
    ]

    try:
        # Inherit stdout/stderr so Sphinx warnings/errors stream to the console for visibility.
        # Only catch a missing sphinx-build binary; Sphinx build failures propagate so users see the raw error.
        subprocess.run(
            cmd,
            check=True,
            cwd=root,
            env=env,
            stdout=None,
            stderr=None,
        )  # nosec B603 - command args are static and trusted
    except FileNotFoundError as exc:
        raise FileNotFoundError(SPHINX_MISSING_MSG) from exc


def validate_build_paths(
    build_agents: bool,
    build_unified: bool,
    agent_source: Path | None,
    agent_output: Path | None,
    unified_source: Path | None,
    unified_output: Path | None,
) -> None:
    """Ensure required paths are present before triggering builds."""

    if build_agents and (agent_source is None or agent_output is None):
        raise SystemExit("Per-agent build requires both agent_source and agent_output paths.")

    if build_unified and (unified_source is None or unified_output is None):
        raise SystemExit("Unified build requires both unified_source and unified_output paths.")


def build_parser() -> argparse.ArgumentParser:
    """Return the CLI argument parser for docs generation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=ROOT,
        type=Path,
        help="Repository root to search for agents and resolve unified docs paths (default: repo root).",
    )
    parser.add_argument(
        "--agent-source",
        default=Path("docs/source"),
        type=Path,
        help=(
            "Per-agent docs source directory. "
            "If relative, it is interpreted relative to each agent directory "
            "(default: docs/source)."
        ),
    )
    parser.add_argument(
        "--agent-output",
        default=Path("docs/generated"),
        type=Path,
        help=(
            "Per-agent docs build output directory. "
            "If relative, it is interpreted relative to each agent directory "
            "(default: docs/generated)."
        ),
    )
    parser.add_argument(
        "--unified-source",
        default=ROOT / "docs/source",
        type=Path,
        help=(
            "Unified docs source directory, resolved from the repository root "
            f"(default: {ROOT / 'docs/source'})."
        ),
    )
    parser.add_argument(
        "--unified-output",
        default=ROOT / "docs/generated",
        type=Path,
        help=(
            "Unified docs build output directory, resolved from the repository root "
            f"(default: {ROOT / 'docs/generated'})."
        ),
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--agents-only", action="store_true", help="Build only per-agent docs")
    group.add_argument("--unified-only", action="store_true", help="Build only unified docs")
    parser.add_argument("--agents", nargs="*", help="Limit doc build to specific agent directory names")
    return parser


def generate_docs(
    root: Path,
    source: Path,
    output: Path,
    unified_source: Path,
    unified_output: Path,
    build_agents: bool = True,
    build_unified: bool = True,
    agent_filter: list[str] | None = None,
) -> None:
    """Dispatch builds for per-agent sites and the unified site."""

    filter_set = set(agent_filter) if agent_filter else None

    agent_dirs: list[Path] = []
    for project in discover_projects(root / "pyproject.toml"):
        candidate = project if project.is_absolute() else root / project
        if not (candidate / "pyproject.toml").exists():
            continue
        if filter_set and candidate.name not in filter_set:
            continue
        agent_dirs.append(candidate)

    if not agent_dirs:
        if filter_set:
            logger.warning("No agents matched filter %s; skipping per-agent build.", sorted(filter_set))
            raise SystemExit("No agents matched the provided filter; nothing to build.")
        else:
            logger.warning("No agent projects found; skipping per-agent build.")
            raise SystemExit("No agent projects found; nothing to build.")

    # agent_dirs is guaranteed non-empty here (early return above).
    extra_paths = [str(root)] + [str(agent_dir / "src") for agent_dir in agent_dirs]
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    if existing_pythonpath:
        extra_paths.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(extra_paths)

    if build_agents:
        build_agent_docs(root, agent_dirs, source, output, env)

    if build_unified:
        build_unified_docs(root, unified_source, unified_output, env)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logger.info("Current path: %s", args.root)

    build_agents = not args.unified_only
    build_unified = not args.agents_only

    validate_build_paths(
        build_agents,
        build_unified,
        args.agent_source,
        args.agent_output,
        args.unified_source,
        args.unified_output,
    )

    try:
        ensure_sphinx_available()
        generate_docs(
            args.root,
            args.agent_source,
            args.agent_output,
            unified_source=args.unified_source,
            unified_output=args.unified_output,
            build_agents=build_agents,
            build_unified=build_unified,
            agent_filter=args.agents,
        )
    except Exception as exc:  # pragma: no cover - logging only
        logger.error("Error generating documentation: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
