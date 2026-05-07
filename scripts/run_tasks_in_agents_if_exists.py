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

import argparse
import sys
from pathlib import Path

from poethepoet.app import PoeThePoet
from rich import print
from utils.task_utils import discover_projects, extract_poe_tasks


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for running Poe tasks across agents."""
    parser = argparse.ArgumentParser(
        description="Run a named Poe task in each agent that defines it.",
    )
    parser.add_argument("task", help="Poe task name to run (e.g. lint, test, build)")
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Extra arguments forwarded to the Poe task",
    )
    return parser.parse_args(argv)


def main() -> None:
    """Run a requested Poe task in each agent that defines it.

    Parses CLI args via argparse: ``task`` (required) and optional extra
    arguments forwarded to the underlying Poe task.
    """
    args = _parse_args()
    pyproject_file = Path(__file__).resolve().parent.parent / "pyproject.toml"
    projects = discover_projects(pyproject_file)

    cli_args = [args.task, *args.extra]
    for project in projects:
        tasks = extract_poe_tasks(project / "pyproject.toml")
        if args.task in tasks:
            print(f"Running task {args.task} in {project}")
            app = PoeThePoet(cwd=project)
            result = app(cli_args=cli_args)
            if result:
                sys.exit(result)
        else:
            print(f"Task {args.task} not found in {project}")


if __name__ == "__main__":
    main()
