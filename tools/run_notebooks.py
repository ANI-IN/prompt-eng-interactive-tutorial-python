"""Execute notebooks end to end against the live Claude API and report the results.

Usage (from the project root, with ANTHROPIC_API_KEY in .env or the environment):

    python tools/run_notebooks.py                      # run every solved notebook
    python tools/run_notebooks.py --folder notebooks   # run the exercise notebooks
    python tools/run_notebooks.py 05 10.2              # only notebooks whose name starts with these
    python tools/run_notebooks.py --save               # also write outputs back into the files

For solved notebooks every graded exercise must print "correctly solved: True".
For exercise notebooks the placeholders are expected to grade False; the check
there is only that every cell runs without raising.
"""

import argparse
import re
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parent.parent
GRADE = re.compile(r"This exercise has been correctly solved: (True|False)")
REFUSAL = "WARNING: Claude declined this request"  # printed by lib.helpers.response_text


def cell_text(cell):
    return "".join(
        out.get("text", "") if out.get("output_type") == "stream" else ""
        for out in cell.get("outputs", [])
    )


def run(path: Path, kernel: str, timeout: int, save: bool):
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name=kernel, resources={"metadata": {"path": str(path.parent)}})
    start = time.time()
    error = None
    try:
        client.execute()
    except CellExecutionError as exc:
        error = str(exc).strip().splitlines()[-1][:300]
    code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]
    grades = [m for cell in code_cells for m in GRADE.findall(cell_text(cell))]
    if error is None and any(REFUSAL in cell_text(cell) for cell in code_cells):
        error = "Claude declined a request (stop_reason='refusal'); see the cell output"
    if save and error is None:
        nbformat.write(nb, path)
    return error, grades, time.time() - start


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prefixes", nargs="*", help="only run notebooks whose file name starts with one of these")
    parser.add_argument("--folder", default="notebooks_solved", choices=["notebooks_solved", "notebooks"])
    parser.add_argument("--kernel", default="python3")
    parser.add_argument("--timeout", type=int, default=600, help="per-cell timeout in seconds")
    parser.add_argument("--save", action="store_true", help="write executed outputs back into the notebooks")
    args = parser.parse_args()

    paths = sorted((ROOT / args.folder).glob("*.ipynb"))
    if args.prefixes:
        paths = [p for p in paths if p.name.startswith(tuple(args.prefixes))]

    expect_pass = args.folder == "notebooks_solved"
    failures = 0
    for path in paths:
        error, grades, seconds = run(path, args.kernel, args.timeout, args.save)
        ok = error is None and (not expect_pass or all(g == "True" for g in grades))
        failures += not ok
        summary = f"grades={'/'.join(grades) or '-'}"
        print(f"{'PASS' if ok else 'FAIL'}  {path.name:<52} {summary:<40} {seconds:6.1f}s")
        if error:
            print(f"      error: {error}")
    print(f"\n{len(paths) - failures}/{len(paths)} notebooks OK")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
