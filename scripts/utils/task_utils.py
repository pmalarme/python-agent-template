"""Shared utilities for discovering uv workspace members and Poe tasks.

Usage:
- Call ``discover_projects(root / "pyproject.toml")`` to expand uv workspace members (and excludes).
- Call ``extract_poe_tasks(project / "pyproject.toml")`` to enumerate a project's Poe tasks,
  following any ``tool.poe.include`` file if present.

Both helpers return plain Python collections and perform no IO beyond reading pyproject files.

Derived from https://github.com/microsoft/agent-framework/ (MIT license) and adapted for agents/*.
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

import glob
from pathlib import Path

import tomli


def discover_projects(workspace_pyproject_file: Path) -> list[Path]:
    """Expand uv workspace members (and excludes) into concrete project paths.

    Expects a pyproject that defines ``tool.uv.workspace.members``; returns each member as a Path,
    expanding globs and removing any entries listed under ``exclude``.

    Args:
        workspace_pyproject_file: Path to the root pyproject that defines the uv workspace.

    Returns:
        A list of Paths to each discovered project directory.
    """

    with workspace_pyproject_file.open("rb") as f:
        data = tomli.load(f)

    projects = data["tool"]["uv"]["workspace"]["members"]
    exclude = data["tool"]["uv"]["workspace"].get("exclude", [])

    all_projects: list[Path] = []
    for project in projects:
        if "*" in project:
            globbed = glob.glob(str(project), root_dir=workspace_pyproject_file.parent)
            globbed_paths = [Path(p) for p in globbed]
            all_projects.extend(globbed_paths)
        else:
            all_projects.append(Path(project))

    for project in exclude:
        if "*" in project:
            globbed = glob.glob(str(project), root_dir=workspace_pyproject_file.parent)
            globbed_paths = [Path(p) for p in globbed]
            all_projects = [p for p in all_projects if p not in globbed_paths]
        else:
            all_projects = [p for p in all_projects if p != Path(project)]

    return all_projects


def extract_poe_tasks(file: Path) -> set[str]:
    """Collect Poe task names from a pyproject (including an included file if present).

    Reads ``tool.poe.tasks`` and, if ``tool.poe.include`` points to a file, merges tasks from there too.

    Args:
        file: Path to a pyproject.toml to inspect.

    Returns:
        A set of Poe task names defined across the file (and any included file).
    """

    with file.open("rb") as f:
        data = tomli.load(f)

    tasks = set(data.get("tool", {}).get("poe", {}).get("tasks", {}).keys())

    include: str | None = data.get("tool", {}).get("poe", {}).get("include", None)
    if include:
        include_file = file.parent / include
        if include_file.exists():
            tasks = tasks.union(extract_poe_tasks(include_file))

    return tasks
