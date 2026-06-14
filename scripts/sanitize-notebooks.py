#!/usr/bin/env python3
"""Clear outputs and reject unsafe public notebook code cells."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import nbformat

PATTERNS = {
    "dynamic evaluation": re.compile(r"e" + r"val\s*\(|new\s+Func" + r"tion"),
    "subprocess execution": re.compile(
        r"child_" + r"process|subprocess|os\.system|sp" + r"awn\s*\("
    ),
    "private absolute path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
    "raw environment access": re.compile(r"process\.env|os\.environ|Deno\.env"),
    "external request": re.compile(r"\b(fetch|requests\.(get|post)|httpx\.(get|post))\s*\("),
}


def notebook_paths(inputs: list[str]):
    for value in inputs:
        path = Path(value)
        if path.is_dir():
            yield from sorted(path.glob("*.ipynb"))
        elif path.suffix == ".ipynb":
            yield path


def sanitize(path: Path, write: bool) -> list[str]:
    notebook = nbformat.read(path, as_version=4)
    errors = []
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type != "code":
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(cell.source):
                errors.append(f"{path}:{index}: {label}")
        cell.outputs = []
        cell.execution_count = None
    nbformat.validate(notebook)
    if write and not errors:
        nbformat.write(notebook, path)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    errors = []
    for path in notebook_paths(args.paths):
        errors.extend(sanitize(path, args.write))
    if errors:
        print("\n".join(errors))
        return 1
    print("Notebook safety checks passed; outputs are clear.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
