"""Generator for classification labs."""

from typing import Any, Dict, List

from components.exercise_library import ExerciseLibrary
from generators.base_generator import BaseLabGenerator


class ClassificationGenerator(BaseLabGenerator):

    @property
    def task_type(self) -> str:
        return "classification"

    def get_exercises(self) -> List[Dict[str, Any]]:
        diff = self.difficulty
        exercises = [
            ExerciseLibrary.data_exploration("tabular", diff),
            ExerciseLibrary.preprocessing("classification", diff),
            ExerciseLibrary.model_building("classifier", diff),
            ExerciseLibrary.model_evaluation("classification", diff),
        ]
        if self.difficulty_cfg.get("bonus_exercise"):
            exercises.append(ExerciseLibrary.hyperparameter_tuning("classifier", diff))
        return exercises

    def get_imports(self) -> List[str]:
        return [
            "import pandas as pd",
            "import numpy as np",
            "import matplotlib.pyplot as plt",
            "import seaborn as sns",
            "from sklearn.model_selection import train_test_split, GridSearchCV",
            "from sklearn.preprocessing import StandardScaler, LabelEncoder",
            "from sklearn.ensemble import RandomForestClassifier",
            "from sklearn.linear_model import LogisticRegression",
            "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix",
            "from utils import plot_confusion_matrix, plot_feature_importance",
        ]

    def get_description(self) -> str:
        return (
            f"In this lab you will build a classification model for **{self.topic}**. "
            f"You will explore the data, preprocess it, train a classifier, and evaluate its performance."
        )

    def get_learning_objectives(self) -> List[str]:
        return [
            "Perform exploratory data analysis on a real-world dataset",
            "Preprocess tabular data for machine learning",
            "Train and evaluate a classification model",
            "Interpret classification metrics (accuracy, precision, recall, F1)",
            f"Apply machine learning to solve: {self.topic}",
        ]
