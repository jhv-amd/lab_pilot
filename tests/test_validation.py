"""Tests for LabValidator."""

import json
import shutil
import tempfile
from pathlib import Path

import nbformat
import pytest

from utils.validation import LabValidator


@pytest.fixture
def tmp_dir():
    d = tempfile.mkdtemp()
    yield Path(d)
    shutil.rmtree(d)


def make_valid_lab(lab_dir: Path):
    """Create a minimal valid lab in lab_dir."""
    # assignment.ipynb
    nb = nbformat.v4.new_notebook()
    nb.cells = [
        nbformat.v4.new_markdown_cell("# Test Lab"),
        nbformat.v4.new_code_cell(
            "def explore(df):\n    ### START CODE HERE ###\n    pass\n    ### END CODE HERE ###"
        ),
    ]
    with open(lab_dir / "assignment.ipynb", "w") as f:
        nbformat.write(nb, f)

    # reference_solution.ipynb
    nb2 = nbformat.v4.new_notebook()
    nb2.cells = [nbformat.v4.new_code_cell("# solution")]
    with open(lab_dir / "reference_solution.ipynb", "w") as f:
        nbformat.write(nb2, f)

    (lab_dir / "test_cases_public.py").write_text("def test_explore(func):\n    pass\n")
    (lab_dir / "test_cases_hidden.py").write_text("def test_explore_comprehensive(func):\n    pass\n")
    (lab_dir / "utils.py").write_text("# utils\n")
    (lab_dir / "README.md").write_text("# Lab\n")

    meta = {
        "assignment_id": "test_lab",
        "topic": "Test",
        "difficulty": "beginner",
        "total_points": 100,
    }
    (lab_dir / "metadata.json").write_text(json.dumps(meta))

    data_dir = lab_dir / "data"
    data_dir.mkdir()
    (data_dir / "train.csv").write_text("a,b\n1,2\n3,4\n")
    (data_dir / "test.csv").write_text("a,b\n5,6\n")


class TestLabValidator:
    def test_valid_lab_passes(self, tmp_dir):
        make_valid_lab(tmp_dir)
        validator = LabValidator(tmp_dir)
        result = validator.validate_lab()
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_missing_file_is_error(self, tmp_dir):
        make_valid_lab(tmp_dir)
        (tmp_dir / "assignment.ipynb").unlink()
        validator = LabValidator(tmp_dir)
        result = validator.validate_lab()
        assert not result["valid"]
        assert any("assignment.ipynb" in e for e in result["errors"])

    def test_invalid_notebook_is_error(self, tmp_dir):
        make_valid_lab(tmp_dir)
        (tmp_dir / "assignment.ipynb").write_text("not valid json {{")
        validator = LabValidator(tmp_dir)
        result = validator.validate_lab()
        assert not result["valid"]

    def test_syntax_error_in_py_is_error(self, tmp_dir):
        make_valid_lab(tmp_dir)
        (tmp_dir / "test_cases_public.py").write_text("def broken(:\n    pass\n")
        validator = LabValidator(tmp_dir)
        result = validator.validate_lab()
        assert not result["valid"]
        assert any("test_cases_public" in e for e in result["errors"])

    def test_missing_data_files_is_warning(self, tmp_dir):
        make_valid_lab(tmp_dir)
        (tmp_dir / "data" / "train.csv").unlink()
        validator = LabValidator(tmp_dir)
        result = validator.validate_lab()
        assert any("train.csv" in w for w in result["warnings"])

    def test_invalid_metadata_json_is_error(self, tmp_dir):
        make_valid_lab(tmp_dir)
        (tmp_dir / "metadata.json").write_text("not json <<<")
        validator = LabValidator(tmp_dir)
        result = validator.validate_lab()
        assert not result["valid"]

    def test_no_markers_is_warning(self, tmp_dir):
        make_valid_lab(tmp_dir)
        nb = nbformat.v4.new_notebook()
        nb.cells = [nbformat.v4.new_code_cell("x = 1")]
        with open(tmp_dir / "assignment.ipynb", "w") as f:
            nbformat.write(nb, f)
        validator = LabValidator(tmp_dir)
        result = validator.validate_lab()
        assert any("START CODE HERE" in w for w in result["warnings"])
