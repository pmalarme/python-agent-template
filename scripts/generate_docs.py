"""Generate HTML docs for all agents using Sphinx (autodoc + napoleon).

How the paths are used:
- ``root``: repo root override (default: this repo root).
- ``source``: agent-local Sphinx source (relative to each agent dir) or absolute.
- ``output``: agent-local build output (relative to each agent dir) or absolute.
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


def clean_autosummary(source_dir: Path) -> None:
    """Remove sphinx-autosummary cache so nav stays in sync."""

    autosummary_dir = source_dir / "_autosummary"
    if autosummary_dir.exists():
        shutil.rmtree(autosummary_dir)


def load_module_name(agent_dir: Path) -> str:
    """Return the importable module name for an agent.

    Prefers ``tool.flit.module.name`` (used in this repo) and falls back to
    ``project.name`` if not set.
    """

    pyproject = agent_dir / "pyproject.toml"
    data = tomli.loads(pyproject.read_text(encoding="utf-8"))
    module = data.get("tool", {}).get("flit", {}).get("module", {}).get("name")
    if module:
        return module
    return data.get("project", {}).get("name", agent_dir.name)


def build_agent_docs(
    root: Path,
    agents: list[Path],
    source: Path,
    output: Path,
    env: dict[str, str],
) -> None:
    """Build docs for each agent into its own output directory."""

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

        subprocess.run(cmd, check=True, cwd=root, env=env)  # nosec B603 - command args are static and trusted


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

    subprocess.run(cmd, check=True, cwd=root, env=env)  # nosec B603 - command args are static and trusted


def generate_docs(
    root: Path,
    source: Path,
    output: Path,
    unified_source: Path | None = None,
    unified_output: Path | None = None,
    build_agents: bool = True,
    build_unified: bool = True,
    agent_filter: list[str] | None = None,
) -> None:
    """Dispatch builds for per-agent sites and the unified site."""

    agent_dirs: list[Path] = []
    for project in discover_projects(root / "pyproject.toml"):
        candidate = project if project.is_absolute() else root / project
        if (candidate / "pyproject.toml").exists():
            agent_dirs.append(candidate)

    if agent_filter:
        agent_dirs = [agent_dir for agent_dir in agent_dirs if agent_dir.name in set(agent_filter)]

    extra_paths = [str(root)] + [str(agent_dir / "src") for agent_dir in agent_dirs]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(extra_paths + [env.get("PYTHONPATH", "")])

    if build_agents:
        build_agent_docs(root, agent_dirs, source, output, env)

    if build_unified and unified_source and unified_output:
        build_unified_docs(root, unified_source, unified_output, env)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--source", default=Path("docs/source"), type=Path)
    parser.add_argument("--output", default=Path("docs/generated"), type=Path)
    parser.add_argument("--unified-source", default=ROOT / "docs/source", type=Path)
    parser.add_argument("--unified-output", default=ROOT / "docs/generated", type=Path)
    parser.add_argument("--agents-only", action="store_true", help="Build only per-agent docs")
    parser.add_argument("--unified-only", action="store_true", help="Build only unified docs")
    parser.add_argument("--agents", nargs="*", help="Limit doc build to specific agent directory names")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logger.info("Current path: %s", args.root)

    if args.agents_only and args.unified_only:
        raise SystemExit("Cannot set both --agents-only and --unified-only")

    build_agents = not args.unified_only
    build_unified = not args.agents_only

    try:
        generate_docs(
            args.root,
            args.source,
            args.output,
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
