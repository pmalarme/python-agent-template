"""Generate docs using py2docfx for all agents in this workspace.

EXPERIMENTAL: py2docfx outputs docfx YAML, not markdown; this pipeline is not finalized and
may change or be replaced.

Path-based variant derived from the Agent Framework script:
- Collect uv workspace members under ``agents/*``
- Build a py2docfx package manifest with ``install_type=path`` per agent
- Emit docfx-ready YAML into ``docs/``
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
import asyncio
import json
import os
from pathlib import Path
from typing import Any

import tomli
from py2docfx.__main__ import main as py2docfx_main  # type: ignore[reportMissingImports]

from utils.task_utils import discover_projects


def load_package_name(agent_dir: Path) -> str:
    pyproject = agent_dir / "pyproject.toml"
    data = tomli.loads(pyproject.read_text(encoding="utf-8"))
    return data.get("project", {}).get("name", agent_dir.name)


def build_manifest(agent_dirs: list[Path]) -> dict[str, Any]:
    """Build py2docfx package manifest using path installs for each agent."""

    packages: list[dict[str, Any]] = []
    for agent_dir in agent_dirs:
        name = load_package_name(agent_dir)
        packages.append(
            {
                "package_info": {
                    "name": name,
                    "install_type": "source_code",
                    "folder": str(agent_dir.resolve()),
                },
                "output_path": f"agents/{agent_dir.name}",
            }
        )

    return {
        "packages": packages,
        "required_packages": [],
    }


async def generate_docs(root: Path, output: Path) -> None:
    """Run py2docfx with the generated manifest."""

    agent_dirs: list[Path] = []
    for project in discover_projects(root / "pyproject.toml"):
        candidate = project if project.is_absolute() else root / project
        if (candidate / "pyproject.toml").exists():
            agent_dirs.append(candidate)

    extra_paths = [str(root)] + [str(agent_dir) for agent_dir in agent_dirs]
    os.environ["PYTHONPATH"] = ":".join(extra_paths + [os.environ.get("PYTHONPATH", "")])
    manifest = build_manifest(agent_dirs)

    print("Discovered agents:")
    for agent_dir in agent_dirs:
        print(f"- {agent_dir.name}")

    output_root = output if output.is_absolute() else root / output
    output_root.mkdir(parents=True, exist_ok=True)

    # py2docfx defines the output option as "-o--output-root-folder" (concatenated), so we must use that literal.
    args = [
        "-o--output-root-folder",
        str(output_root),
        "-j",
        json.dumps(manifest),
        "--verbose",
    ]
    try:
        await py2docfx_main(args)
    except Exception as exc:  # pragma: no cover - logging only
        print(f"Error generating documentation: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--output", default=Path("docs"), type=Path)
    args = parser.parse_args()

    print(f"Current path: {args.root}")

    asyncio.run(generate_docs(args.root, args.output))


if __name__ == "__main__":
    main()
