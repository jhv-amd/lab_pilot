"""Tests for NotebookBuilder."""

import shutil
import tempfile
from pathlib import Path

import nbformat
import pytest

from utils.notebook_builder import NotebookBuilder


@pytest.fixture
def tmp_dir():
    d = tempfile.mkdtemp()
    yield Path(d)
    shutil.rmtree(d)


SAMPLE_EXERCISES = [
    {
        "title": "Exercise 1: Test",
        "function_name": "test_fn",
        "points": 10,
        "instructions": "Do something.",
        "starter_code": "def test_fn(x):\n    ### START CODE HERE ###\n    pass\n    ### END CODE HERE ###",
        "solution_code": "def test_fn(x):\n    return x + 1",
        "hints": ["Hint: add 1"],
    }
]


class TestNotebookBuilder:
    def test_add_title_returns_self(self):
        builder = NotebookBuilder()
        result = builder.add_title("Title", "Description", SAMPLE_EXERCISES, 10)
        assert result is builder

    def test_build_creates_file(self, tmp_dir):
        builder = NotebookBuilder()
        builder.add_title("Test Lab", "A test lab.", SAMPLE_EXERCISES, 10)
        builder.add_setup_cell(["import numpy as np"], "data = None")
        builder.add_exercise(SAMPLE_EXERCISES[0], 1, "beginner")
        builder.add_submission_cell("test_lab")
        out = tmp_dir / "notebook.ipynb"
        builder.build(out)
        assert out.exists()

    def test_built_notebook_is_valid(self, tmp_dir):
        builder = NotebookBuilder()
        builder.add_title("Test", "Desc", SAMPLE_EXERCISES, 10)
        builder.add_setup_cell(["import pandas as pd"], "pass")
        out = tmp_dir / "nb.ipynb"
        builder.build(out)
        nb = nbformat.read(str(out), as_version=4)
        assert len(nb.cells) > 0

    def test_exercise_creates_three_cells(self, tmp_dir):
        builder = NotebookBuilder()
        initial_count = len(builder.cells)
        builder.add_exercise(SAMPLE_EXERCISES[0], 1, "intermediate")
        # Should add: markdown header, code cell, test cell
        assert len(builder.cells) == initial_count + 3

    def test_submission_cell_contains_assignment_id(self, tmp_dir):
        builder = NotebookBuilder()
        builder.add_submission_cell("my_test_lab")
        last_cell = builder.cells[-1]
        assert "my_test_lab" in last_cell.source

    def test_build_solution_creates_file(self, tmp_dir):
        builder = NotebookBuilder()
        builder.add_title("Test", "Desc", SAMPLE_EXERCISES, 10)
        builder.add_setup_cell(["import numpy as np"], "pass")
        out = tmp_dir / "solution.ipynb"
        builder.build_solution(out, SAMPLE_EXERCISES)
        assert out.exists()

    def test_hints_appear_for_beginner(self):
        builder = NotebookBuilder()
        ex = {**SAMPLE_EXERCISES[0], "hints": ["Hint: try this"]}
        builder.add_exercise(ex, 1, "beginner")
        md_cell = builder.cells[0]
        assert "Hint: try this" in md_cell.source

    def test_hints_hidden_for_advanced(self):
        builder = NotebookBuilder()
        ex = {**SAMPLE_EXERCISES[0], "hints": ["Hint: try this"]}
        builder.add_exercise(ex, 1, "advanced")
        md_cell = builder.cells[0]
        assert "Hint: try this" not in md_cell.source
