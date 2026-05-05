"""Tests for topic-specific generators."""

import json
import shutil
import tempfile
from pathlib import Path

import nbformat
import pytest


@pytest.fixture
def tmp_dir():
    d = tempfile.mkdtemp()
    yield Path(d)
    shutil.rmtree(d)


class TestClassificationGenerator:
    def test_get_exercises_returns_list(self):
        from generators.classification_generator import ClassificationGenerator
        gen = ClassificationGenerator("Churn", "telco_churn", "intermediate", "/tmp/test_cl")
        exercises = gen.get_exercises()
        assert isinstance(exercises, list)
        assert len(exercises) >= 4

    def test_exercise_has_required_keys(self):
        from generators.classification_generator import ClassificationGenerator
        gen = ClassificationGenerator("Churn", "telco_churn", "beginner", "/tmp/test_cl")
        for ex in gen.get_exercises():
            assert "title" in ex
            assert "function_name" in ex
            assert "points" in ex
            assert "starter_code" in ex
            assert "solution_code" in ex

    def test_beginner_has_no_bonus(self):
        from generators.classification_generator import ClassificationGenerator
        gen = ClassificationGenerator("Churn", "telco_churn", "beginner", "/tmp/test_cl")
        exercises = gen.get_exercises()
        fn_names = [e["function_name"] for e in exercises]
        assert "tune_hyperparameters" not in fn_names

    def test_intermediate_has_bonus(self):
        from generators.classification_generator import ClassificationGenerator
        gen = ClassificationGenerator("Churn", "telco_churn", "intermediate", "/tmp/test_cl")
        exercises = gen.get_exercises()
        fn_names = [e["function_name"] for e in exercises]
        assert "tune_hyperparameters" in fn_names

    def test_get_imports_returns_strings(self):
        from generators.classification_generator import ClassificationGenerator
        gen = ClassificationGenerator("Churn", "telco_churn", "intermediate", "/tmp/test_cl")
        imports = gen.get_imports()
        assert all(isinstance(i, str) for i in imports)
        assert any("pandas" in i for i in imports)

    def test_generate_all_creates_files(self, tmp_dir):
        from generators.classification_generator import ClassificationGenerator
        gen = ClassificationGenerator("Churn", "telco_churn", "beginner", tmp_dir)
        summary = gen.generate_all()
        assert (tmp_dir / "assignment.ipynb").exists()
        assert (tmp_dir / "test_cases_public.py").exists()
        assert (tmp_dir / "test_cases_hidden.py").exists()
        assert (tmp_dir / "reference_solution.ipynb").exists()
        assert (tmp_dir / "metadata.json").exists()
        assert (tmp_dir / "README.md").exists()

    def test_metadata_has_correct_fields(self, tmp_dir):
        from generators.classification_generator import ClassificationGenerator
        gen = ClassificationGenerator("Test Topic", "synthetic", "beginner", tmp_dir)
        gen.generate_all()
        meta = json.loads((tmp_dir / "metadata.json").read_text())
        assert meta["topic"] == "Test Topic"
        assert meta["difficulty"] == "beginner"
        assert meta["total_points"] > 0
        assert len(meta["exercises"]) >= 4


class TestRegressionGenerator:
    def test_task_type_is_regression(self):
        from generators.regression_generator import RegressionGenerator
        gen = RegressionGenerator("House Prices", "house_prices", "intermediate", "/tmp/test_reg")
        assert gen.task_type == "regression"

    def test_generates_regression_exercises(self):
        from generators.regression_generator import RegressionGenerator
        gen = RegressionGenerator("House Prices", "house_prices", "intermediate", "/tmp/test_reg")
        exercises = gen.get_exercises()
        fn_names = [e["function_name"] for e in exercises]
        assert "train_regressor" in fn_names
        assert "evaluate_model" in fn_names

    def test_generate_all_creates_files(self, tmp_dir):
        from generators.regression_generator import RegressionGenerator
        gen = RegressionGenerator("House Prices", "synthetic", "beginner", tmp_dir)
        gen.generate_all()
        assert (tmp_dir / "assignment.ipynb").exists()
        assert (tmp_dir / "utils.py").exists()


class TestNLPGenerator:
    def test_has_text_exercises(self):
        from generators.nlp_generator import NLPGenerator
        gen = NLPGenerator("Sentiment", "imdb_sentiment", "intermediate", "/tmp/test_nlp")
        exercises = gen.get_exercises()
        fn_names = [e["function_name"] for e in exercises]
        assert "explore_text" in fn_names
        assert "clean_text" in fn_names
        assert "extract_features" in fn_names

    def test_generate_all_nlp(self, tmp_dir):
        from generators.nlp_generator import NLPGenerator
        gen = NLPGenerator("Sentiment Analysis", "imdb_sentiment", "beginner", tmp_dir)
        gen.generate_all()
        assert (tmp_dir / "assignment.ipynb").exists()


class TestTimeSeriesGenerator:
    def test_has_time_series_exercises(self):
        from generators.time_series_generator import TimeSeriesGenerator
        gen = TimeSeriesGenerator("Demand Forecast", "synthetic_timeseries", "intermediate", "/tmp/test_ts")
        exercises = gen.get_exercises()
        fn_names = [e["function_name"] for e in exercises]
        assert "explore_series" in fn_names
        assert "preprocess_series" in fn_names
        assert "add_time_features" in fn_names
