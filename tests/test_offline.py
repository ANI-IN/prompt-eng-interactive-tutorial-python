"""Offline checks: no API key or network needed.

Run with:  python -m pytest -q
"""

import ast
import importlib
import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EXERCISE_NBS = sorted((ROOT / "notebooks").glob("*.ipynb"))
SOLVED_NBS = sorted((ROOT / "notebooks_solved").glob("*.ipynb"))
PLACEHOLDER = re.compile(r"\[(Replace|Build your prompt here)")


def cells(path):
    return json.loads(path.read_text(encoding="utf-8"))["cells"]


def source(cell):
    return "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]


# --- grading helpers ---------------------------------------------------------

def test_grading_helpers():
    from lib import grading

    assert grading.includes_all("1, 2 and 3", ["1", "2", "3"])
    assert not grading.includes_all("1 and 2", ["1", "2", "3"])
    assert grading.includes_any("Hola amigo", ["hola", "gracias"])
    assert grading.word_count("  one two\nthree  ") == 3
    assert grading.equals_exact("pytest", "pytest")
    assert not grading.equals_exact("pytest.", "pytest")
    assert grading.line_count("a\n\n b \n") == 2
    assert grading.last_token("Label: Error.") == "error"
    assert grading.last_token("") == ""


def test_placeholder_prompts_skip_the_api(monkeypatch, capsys):
    from lib import helpers

    def fail(**_):
        raise AssertionError("API must not be called for a placeholder prompt")

    monkeypatch.setattr(helpers.client.messages, "create", fail)
    assert helpers.get_completion("[Replace this text]") == ""
    assert helpers.get_completion("question", "[Build your prompt here]") == ""
    assert "Replace the placeholder" in capsys.readouterr().out
    assert not helpers.has_placeholder("a real prompt", "")


# --- notebook structure --------------------------------------------------------

def test_thirteen_chapters_in_both_folders():
    assert len(EXERCISE_NBS) == 13
    assert [p.name for p in EXERCISE_NBS] == [p.name for p in SOLVED_NBS]


@pytest.mark.parametrize("path", EXERCISE_NBS, ids=lambda p: p.stem)
def test_solved_twin_differs_only_in_exercise_cells(path):
    exercise, solved = cells(path), cells(ROOT / "notebooks_solved" / path.name)
    assert len(exercise) == len(solved)
    for a, b in zip(exercise, solved):
        assert a["cell_type"] == b["cell_type"]
        if a["cell_type"] == "markdown" or not PLACEHOLDER.search(source(a)):
            assert source(a) == source(b)


@pytest.mark.parametrize("path", EXERCISE_NBS + SOLVED_NBS, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_code_cells_are_valid_python(path):
    for cell in cells(path):
        if cell["cell_type"] == "code":
            ast.parse(source(cell))


@pytest.mark.parametrize("path", SOLVED_NBS, ids=lambda p: p.stem)
def test_solved_notebooks_have_no_placeholders(path):
    for cell in cells(path):
        if cell["cell_type"] == "code":
            assert not PLACEHOLDER.search(source(cell)), source(cell)[:120]


@pytest.mark.parametrize("path", EXERCISE_NBS, ids=lambda p: p.stem)
def test_exercise_notebooks_ship_without_outputs(path):
    for cell in cells(path):
        if cell["cell_type"] == "code":
            assert cell.get("outputs", []) == []


def test_every_referenced_hint_exists():
    hints = importlib.import_module("hints")
    referenced = set()
    for path in EXERCISE_NBS:
        for cell in cells(path):
            referenced |= set(re.findall(r"from hints import (\w+)", source(cell)))
    assert referenced, "no hint cells found"
    for name in referenced:
        assert isinstance(getattr(hints, name), str)


# --- secrets hygiene -------------------------------------------------------------

def test_no_api_keys_in_tracked_files():
    try:
        files = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.split()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("not a git checkout")
    assert ".env" not in files
    key_pattern = re.compile(r"sk-ant-(?!your-key-here)[A-Za-z0-9_-]{8,}")
    for name in files:
        path = ROOT / name
        if path.is_file():
            assert not key_pattern.search(path.read_text(encoding="utf-8", errors="ignore")), name
