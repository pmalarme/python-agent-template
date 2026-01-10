"""Check code blocks in Markdown files for syntax errors.

What it does:
- Expands glob patterns (unless --no-glob) to find Markdown files.
- Extracts ```python fences and runs pyright on each block via uv; highlights failures with pygments.
- Supports --exclude patterns to skip paths and --no-glob to treat inputs literally.

Derived from https://github.com/microsoft/agent-framework/ (MIT).
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
from enum import Enum
import glob
import logging
import os
import tempfile
import subprocess  # nosec
from typing import Any, cast

from pygments import highlight  # type: ignore
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer  # type: ignore[reportUnknownVariableType]


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class Colors(str, Enum):
    CEND = "\33[0m"
    CRED = "\33[31m"
    CREDBG = "\33[41m"
    CGREEN = "\33[32m"
    CGREENBG = "\33[42m"
    CVIOLET = "\33[35m"
    CGREY = "\33[90m"


def with_color(text: str, color: Colors) -> str:
    """Render text with ANSI color codes."""

    return f"{color.value}{text}{Colors.CEND.value}"


def expand_file_patterns(patterns: list[str], skip_glob: bool = False) -> list[str]:
    """Expand glob patterns to actual file paths, preserving literal paths when requested.

    Args:
        patterns: Glob patterns or literal paths, depending on ``skip_glob``.
        skip_glob: When True, treats patterns as literal paths and filters for .md.

    Returns:
        A sorted list of unique markdown file paths.
    """

    all_files: list[str] = []
    for pattern in patterns:
        if skip_glob:
            if pattern.endswith(".md"):
                matches = glob.glob(pattern, recursive=False)
                all_files.extend(matches)
        else:
            matches = glob.glob(pattern, recursive=True)
            all_files.extend(matches)
    return sorted(set(all_files))


def extract_python_code_blocks(markdown_file_path: str) -> list[tuple[str, int]]:
    """Extract Python code blocks from a Markdown file, returning code and starting line numbers.

    Args:
        markdown_file_path: Path to a markdown file.

    Returns:
        A list of tuples ``(code_block, starting_line_number)``.
    """

    with open(markdown_file_path, encoding="utf-8") as file:
        lines = file.readlines()

    code_blocks: list[tuple[str, int]] = []
    in_code_block = False
    current_block: list[str] = []

    for i, line in enumerate(lines):
        if line.strip().startswith("```python"):
            in_code_block = True
            current_block = []
        elif line.strip().startswith("```"):
            in_code_block = False
            code_blocks.append(("\n".join(current_block), i - len(current_block) + 1))
        elif in_code_block:
            current_block.append(line)

    return code_blocks


def check_code_blocks(
    markdown_file_paths: list[str],
    exclude_patterns: list[str] | None = None,
) -> None:
    """Check Python code blocks in Markdown files by running pyright on each block.

    Args:
        markdown_file_paths: Markdown files to inspect.
        exclude_patterns: Optional substrings; any path containing one is skipped.

    Raises:
        RuntimeError: If any checked file contains a failing Python block.
    """

    files_with_errors: list[str] = []
    exclude_patterns = exclude_patterns or []

    for markdown_file_path in markdown_file_paths:
        if any(pattern in markdown_file_path for pattern in exclude_patterns):
            logger.info("Skipping %s (matches exclude pattern)", markdown_file_path)
            continue

        code_blocks = extract_python_code_blocks(markdown_file_path)
        had_errors = False

        for code_block, line_no in code_blocks:
            markdown_file_path_with_line_no = f"{markdown_file_path}:{line_no}"
            logger.info("Checking a code block in %s...", markdown_file_path_with_line_no)

            tmp_path = ""
            try:
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                    temp_file.write(code_block.encode("utf-8"))
                    temp_file.flush()
                    tmp_path = temp_file.name

                result = subprocess.run(
                    ["uv", "run", "pyright", tmp_path],
                    capture_output=True,
                    text=True,
                    cwd=".",
                )  # nosec

                if result.returncode != 0:
                    lexer = cast(Any, PythonLexer())
                    formatter = cast(Any, TerminalFormatter())
                    highlighted_code: str = highlight(code_block, lexer, formatter)
                    logger.info(
                        " %s\n%s\n%s\n%s\n%s\n\n%s\n%s%s\n",
                        with_color("FAIL", Colors.CREDBG),
                        with_color("========================================================", Colors.CGREY),
                        with_color(
                            f"Error: Pyright found issues in {with_color(markdown_file_path_with_line_no, Colors.CVIOLET)}",
                            Colors.CRED,
                        ),
                        with_color("--------------------------------------------------------", Colors.CGREY),
                        highlighted_code,
                        with_color("pyright output:", Colors.CVIOLET),
                        with_color(result.stdout, Colors.CRED),
                        with_color("========================================================", Colors.CGREY),
                    )
                    had_errors = True
                else:
                    logger.info(" %s", with_color("OK", Colors.CGREENBG))
            finally:
                if tmp_path:
                    try:
                        os.unlink(tmp_path)
                    except FileNotFoundError:
                        pass

        if had_errors:
            files_with_errors.append(markdown_file_path)

    if files_with_errors:
        raise RuntimeError("Syntax errors found in the following files:\n" + "\n".join(files_with_errors))


def main() -> None:
    """Parse CLI arguments and run pyright checks on python fences in markdown files.

    CLI:
        markdown_files (list[str]): Markdown files or glob patterns.
        --exclude (str, repeatable): Skip files whose path contains this substring.
        --no-glob (flag): Treat inputs as literal paths (no glob expansion).
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown_files", nargs="+", help="Markdown files to check (supports glob patterns).")
    parser.add_argument("--exclude", action="append", help="Exclude files containing this pattern.")
    parser.add_argument("--no-glob", action="store_true", help="Treat file arguments as literal paths (no glob expansion).")
    args = parser.parse_args()

    expanded_files = expand_file_patterns(args.markdown_files, skip_glob=args.no_glob)
    check_code_blocks(expanded_files, args.exclude)


if __name__ == "__main__":
    main()
