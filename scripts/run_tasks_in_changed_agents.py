"""Run a Poe task only in agents that have changed files.

How it works:
- Discovers agents via the root uv workspace (tool.uv.workspace.members).
- Determines changed files from argv (if provided) or git diff against base-ref.
- Maps changed files to agents, then runs the task via Poe in each matching agent that defines it.

Usage:
    python scripts/run_tasks_in_changed_agents.py <task> [changed_file ...]
    # When no files are passed, falls back to git diff against --base-ref (default origin/main).

Derived from https://github.com/microsoft/agent-framework/ (MIT) and adapted for agents/*.
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

import argparse
import subprocess  # nosec B404 - use git via fixed arg lists; avoids extra deps like GitPython
import sys
from pathlib import Path

from poethepoet.app import PoeThePoet
from rich import print

from utils.task_utils import discover_projects, extract_poe_tasks

ROOT = Path(__file__).resolve().parent.parent




def git_changed_files(base_ref: str) -> list[str]:
    """Get changed files via git diff, trying a couple of fallbacks.

    Args:
        base_ref: The ref to diff against (e.g., origin/main).

    Returns:
        A list of changed file paths (relative to repo root) or an empty list on failure.
    """

    candidates = [
        ["git", "diff", "--name-only", f"{base_ref}...HEAD", "--"],
        ["git", "diff", "--name-only", "HEAD~1", "--"],
    ]
    for command in candidates:
        try:
            output = subprocess.check_output(command, cwd=ROOT, text=True)  # nosec B603 - fixed args, shell=False, ref-only input
        except subprocess.CalledProcessError:
            continue
        if output.strip():
            return output.strip().splitlines()
    return []


def get_changed_projects(projects: list[Path], changed_files: list[str], workspace_root: Path) -> set[Path]:
    """Determine which agents have changed files by matching paths against project roots.

    Args:
        projects: Candidate project paths from the uv workspace.
        changed_files: Paths (relative or absolute) reported by git or provided by the user.
        workspace_root: Repository root to resolve relative paths.

    Returns:
        A set of project Paths that contain at least one changed file.
    """

    changed_projects: set[Path] = set()

    for file_path in changed_files:
        file_path_str = str(file_path)

        abs_path = Path(file_path_str)
        if not abs_path.is_absolute():
            abs_path = workspace_root / file_path_str

        for project in projects:
            project_abs = workspace_root / project
            try:
                abs_path.relative_to(project_abs)
                changed_projects.add(project)
                break
            except ValueError:
                continue

    return changed_projects


def main() -> None:
    """Parse args, detect changed agents, and run a Poe task where present.

    CLI:
        task (str): Name of the Poe task to run in each changed agent.
        files (list[str], optional): Changed file paths; if omitted, git diff is used.
        --base-ref (str): Base ref for git diff fallback (default: origin/main).
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", help="The task name to run")
    parser.add_argument("files", nargs="*", help="Changed files to determine which agents to run")
    parser.add_argument("--base-ref", default="origin/main", help="Base ref for git diff when no files are provided")
    args = parser.parse_args()

    pyproject_file = ROOT / "pyproject.toml"
    workspace_root = pyproject_file.parent
    projects = discover_projects(pyproject_file)

    changed_files = args.files
    if not changed_files or changed_files == ["."]:
        changed_files = git_changed_files(args.base_ref)

    if not changed_files:
        print(f"[yellow]No changes detected; skipping {args.task}[/yellow]")
        return

    changed_projects = get_changed_projects(projects, changed_files, workspace_root)
    if not changed_projects:
        print(f"[yellow]No agent projects matched the changed files; skipping {args.task}[/yellow]")
        return

    print(f"[cyan]Running {args.task} in agents: {', '.join(str(p) for p in sorted(changed_projects))}[/cyan]")

    for project in sorted(changed_projects):
        tasks = extract_poe_tasks(project / "pyproject.toml")
        if args.task in tasks:
            print(f"Running task {args.task} in {project}")
            app = PoeThePoet(cwd=project)
            result = app(cli_args=[args.task])
            if result:
                sys.exit(result)
        else:
            print(f"Task {args.task} not found in {project}")


if __name__ == "__main__":
    main()
