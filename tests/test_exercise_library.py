"""Tests for ExerciseLibrary."""

import pytest
from components.exercise_library import ExerciseLibrary


class TestDataExploration:
    def test_returns_dict(self):
        ex = ExerciseLibrary.data_exploration("tabular", "intermediate")
        assert isinstance(ex, dict)

    def test_has_required_keys(self):
        ex = ExerciseLibrary.data_exploration("tabular", "intermediate")
        for key in ("title", "function_name", "points", "starter_code", "solution_code",
                    "public_tests", "hidden_tests"):
            assert key in ex, f"Missing key: {key}"

    def test_function_name_is_explore_data(self):
        ex = ExerciseLibrary.data_exploration("tabular", "advanced")
        assert ex["function_name"] == "explore_data"

    def test_starter_code_has_markers(self):
        ex = ExerciseLibrary.data_exploration("tabular", "beginner")
        assert "### START CODE HERE ###" in ex["starter_code"]
        assert "### END CODE HERE ###" in ex["starter_code"]

    def test_beginner_has_hints(self):
        ex = ExerciseLibrary.data_exploration("tabular", "beginner")
        assert len(ex["hints"]) > 0

    def test_advanced_has_no_hints(self):
        ex = ExerciseLibrary.data_exploration("tabular", "advanced")
        assert len(ex["hints"]) == 0

    def test_points_is_positive(self):
        ex = ExerciseLibrary.data_exploration("tabular", "intermediate")
        assert ex["points"] > 0


class TestPreprocessing:
    def test_returns_dict(self):
        ex = ExerciseLibrary.preprocessing("classification", "intermediate")
        assert isinstance(ex, dict)

    def test_function_name(self):
        ex = ExerciseLibrary.preprocessing("classification", "beginner")
        assert ex["function_name"] == "preprocess"

    def test_beginner_starter_has_steps(self):
        ex = ExerciseLibrary.preprocessing("classification", "beginner")
        assert "Step 1" in ex["starter_code"]


class TestModelBuilding:
    def test_returns_dict(self):
        ex = ExerciseLibrary.model_building("classifier", "intermediate")
        assert isinstance(ex, dict)

    def test_points_is_30(self):
        ex = ExerciseLibrary.model_building("classifier", "intermediate")
        assert ex["points"] == 30

    def test_solution_trains_model(self):
        ex = ExerciseLibrary.model_building("classifier", "advanced")
        assert "fit" in ex["solution_code"]


class TestHyperparameterTuning:
    def test_returns_dict(self):
        ex = ExerciseLibrary.hyperparameter_tuning("classifier", "intermediate")
        assert isinstance(ex, dict)

    def test_function_name(self):
        ex = ExerciseLibrary.hyperparameter_tuning("classifier", "intermediate")
        assert ex["function_name"] == "tune_hyperparameters"

    def test_solution_uses_gridsearch(self):
        ex = ExerciseLibrary.hyperparameter_tuning("classifier", "intermediate")
        assert "GridSearchCV" in ex["solution_code"]
