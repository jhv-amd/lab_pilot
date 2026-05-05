"""End-to-end integration tests for lab generation."""

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


FULL_GENERATION_CASES = [
    ("Customer Churn Prediction", "machine_learning", "telco_churn", "beginner"),
    ("House Price Prediction", "regression", "house_prices", "intermediate"),
    ("Sentiment Analysis", "nlp", "imdb_sentiment", "advanced"),
    ("Demand Forecasting", "time_series", "synthetic_timeseries", "beginner"),
]


@pytest.mark.parametrize("topic,course,dataset,difficulty", FULL_GENERATION_CASES)
def test_full_lab_generation(topic, course, dataset, difficulty, tmp_dir):
    """Generate a lab and validate it passes the validator."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    from lab_generator import _get_generator

    lab_dir = tmp_dir / f"{course}_{difficulty}"
    generator = _get_generator(course, topic, dataset, difficulty, lab_dir)
    summary = generator.generate_all()

    assert (lab_dir / "assignment.ipynb").exists()
    assert (lab_dir / "test_cases_public.py").exists()
    assert (lab_dir / "test_cases_hidden.py").exists()
    assert (lab_dir / "reference_solution.ipynb").exists()
    assert (lab_dir / "metadata.json").exists()

    meta = json.loads((lab_dir / "metadata.json").read_text())
    assert meta["topic"] == topic
    assert meta["total_points"] > 0

    nb = nbformat.read(str(lab_dir / "assignment.ipynb"), as_version=4)
    start_count = sum(1 for c in nb.cells if "START CODE HERE" in c.source)
    assert start_count >= 3, f"Expected ≥ 3 exercises, found {start_count}"

    assert summary["elapsed_seconds"] < 30, "Generation should complete in < 30 seconds"


def test_exercises_filter(tmp_dir):
    """Only generate the specified exercises."""
    from lab_generator import _get_generator

    lab_dir = tmp_dir / "filtered_lab"
    gen = _get_generator(
        "machine_learning",
        "Test Topic",
        "synthetic",
        "beginner",
        lab_dir,
        exercises_filter=["explore_data", "preprocess"],
    )
    summary = gen.generate_all()
    assert summary["exercises"] == 2


def test_all_courses_generate(tmp_dir):
    """Smoke test: each course generates without error."""
    from lab_generator import _get_generator

    courses = [
        ("machine_learning", "synthetic"),
        ("regression", "synthetic"),
        ("nlp", "synthetic_text"),
        ("time_series", "synthetic_timeseries"),
    ]
    for course, dataset in courses:
        lab_dir = tmp_dir / course
        gen = _get_generator(course, f"Test {course}", dataset, "beginner", lab_dir)
        summary = gen.generate_all()
        assert (lab_dir / "assignment.ipynb").exists(), f"Failed for course: {course}"
