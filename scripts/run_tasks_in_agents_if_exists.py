"""Run a named Poe task in each agent that defines it.

How it works:
- Discovers agents via the root uv workspace (tool.uv.workspace.members).
- For each agent, reads its pyproject (and optional tool.poe.include) to see if the task exists.
- If present, runs the task with Poe in that agent's directory; otherwise logs that it was skipped.

Usage:
    python scripts/run_tasks_in_agents_if_exists.py <task> [agent ...]

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

import sys
from pathlib import Path

from poethepoet.app import PoeThePoet
from rich import print

from utils.task_utils import discover_projects, extract_poe_tasks


def main() -> None:
    """Run a requested Poe task in each agent that defines it.

    If agent names are provided, only those under agents/ are considered; otherwise all workspace members.

    Args:
        None. Parses CLI args: ``task`` (required).
    """
    pyproject_file = Path(__file__).resolve().parent.parent / "pyproject.toml"
    projects = discover_projects(pyproject_file)

    if len(sys.argv) < 2:
        print("Please provide a task name")
        sys.exit(1)

    task_name = sys.argv[1]
    for project in projects:
        tasks = extract_poe_tasks(project / "pyproject.toml")
        if task_name in tasks:
            print(f"Running task {task_name} in {project}")
            app = PoeThePoet(cwd=project)
            result = app(cli_args=sys.argv[1:])
            if result:
                sys.exit(result)
        else:
            print(f"Task {task_name} not found in {project}")


if __name__ == "__main__":
    main()
