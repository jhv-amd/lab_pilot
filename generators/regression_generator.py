"""Generator for regression labs."""

from typing import Any, Dict, List

from components.exercise_library import ExerciseLibrary
from generators.base_generator import BaseLabGenerator


class RegressionGenerator(BaseLabGenerator):

    @property
    def task_type(self) -> str:
        return "regression"

    def get_exercises(self) -> List[Dict[str, Any]]:
        diff = self.difficulty
        exercises = [
            ExerciseLibrary.data_exploration("tabular", diff),
            ExerciseLibrary.preprocessing("regression", diff),
            self._train_regressor_exercise(),
            ExerciseLibrary.model_evaluation("regression", diff),
        ]
        if self.difficulty_cfg.get("bonus_exercise"):
            exercises.append(self._feature_engineering_exercise())
        return exercises

    def _train_regressor_exercise(self) -> Dict[str, Any]:
        min_r2 = self.difficulty_cfg.get("min_accuracy_regression_r2", 0.75)
        hints = {
            "beginner": [f"Hint: Try LinearRegression or RandomForestRegressor", f"Hint: Target R² ≥ {min_r2}"],
            "intermediate": [f"Hint: Target R² ≥ {min_r2}"],
            "advanced": [],
        }
        starter = (
            "def train_regressor(X_train, y_train):\n"
            "    \"\"\"\n"
            "    Train a regression model.\n"
            "    Returns: fitted model with .predict() method\n"
            "    \"\"\"\n"
            "    ### START CODE HERE ###\n"
            + ("    # Hint: Try LinearRegression() or RandomForestRegressor()\n" if self.difficulty == "beginner" else "")
            + "    model = None\n"
            "    ### END CODE HERE ###\n"
            "    return model"
        )
        solution = (
            "def train_regressor(X_train, y_train):\n"
            "    from sklearn.ensemble import GradientBoostingRegressor\n"
            f"    model = GradientBoostingRegressor(n_estimators=100, random_state=42)\n"
            "    model.fit(X_train, y_train)\n"
            "    return model"
        )
        public_test = (
            "from sklearn.datasets import make_regression\n"
            "from sklearn.model_selection import train_test_split\n"
            "X, y = make_regression(n_samples=200, n_features=5, random_state=42)\n"
            "X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "model = func(X_tr, y_tr)\n"
            "assert model is not None, 'Must return a model'\n"
            "assert hasattr(model, 'predict'), 'Model must have predict()'"
        )
        hidden_test = (
            "from sklearn.metrics import r2_score\n"
            "from sklearn.model_selection import train_test_split\n"
            "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
            "X = df.select_dtypes(include=[np.number]).drop(columns=[df.columns[-1]], errors='ignore').fillna(0)\n"
            "y = df.iloc[:, -1]\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "model = func(X_train, y_train)\n"
            "preds = model.predict(X_test)\n"
            "r2 = r2_score(y_test, preds)\n"
            f"assert r2 >= {min_r2}, f'R² {{r2:.3f}} < {min_r2}'"
        )
        return {
            "title": "Exercise 3: Train Regression Model",
            "function_name": "train_regressor",
            "points": 30,
            "instructions": (
                f"Train a regression model for **{self.topic}**.\n\n"
                f"**Requirements:** Return a fitted model with `.predict()`. Target R² ≥ {min_r2}."
            ),
            "starter_code": starter,
            "solution_code": solution,
            "public_tests": [public_test],
            "hidden_tests": [hidden_test],
            "hints": hints.get(self.difficulty, []),
        }

    def _feature_engineering_exercise(self) -> Dict[str, Any]:
        return {
            "title": "Bonus: Feature Engineering",
            "function_name": "engineer_features",
            "points": 10,
            "instructions": (
                "Create new features to improve model performance.\n\n"
                "**Requirements:** Return an augmented DataFrame with at least 2 new features."
            ),
            "starter_code": (
                "def engineer_features(df):\n"
                "    \"\"\"Add new features to improve predictions.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    df_new = df.copy()\n"
                "    # TODO: Add new features\n"
                "    ### END CODE HERE ###\n"
                "    return df_new"
            ),
            "solution_code": (
                "def engineer_features(df):\n"
                "    df_new = df.copy()\n"
                "    numeric_cols = df_new.select_dtypes(include=[np.number]).columns[:3]\n"
                "    df_new['feature_ratio'] = df_new[numeric_cols[0]] / (df_new[numeric_cols[1]] + 1e-9)\n"
                "    df_new['feature_product'] = df_new[numeric_cols[0]] * df_new[numeric_cols[2]]\n"
                "    return df_new"
            ),
            "public_tests": [
                "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
                "result = func(df)\n"
                "assert isinstance(result, pd.DataFrame), 'Must return a DataFrame'\n"
                "assert len(result.columns) > len(df.columns), 'Must add new columns'"
            ],
            "hidden_tests": ["assert len(result.columns) >= len(df.columns) + 2, 'Must add at least 2 features'"],
            "hints": ["Hint: Try ratio features, polynomial features, or interaction terms"],
        }

    def get_imports(self) -> List[str]:
        return [
            "import pandas as pd",
            "import numpy as np",
            "import matplotlib.pyplot as plt",
            "import seaborn as sns",
            "from sklearn.model_selection import train_test_split",
            "from sklearn.preprocessing import StandardScaler",
            "from sklearn.linear_model import LinearRegression, Ridge",
            "from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor",
            "from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score",
            "from utils import plot_predictions, plot_residuals",
        ]

    def get_description(self) -> str:
        return (
            f"In this lab you will build a regression model for **{self.topic}**. "
            f"You will explore the data, engineer features, train a regressor, and evaluate with RMSE and R²."
        )

    def get_learning_objectives(self) -> List[str]:
        return [
            "Perform exploratory data analysis for regression tasks",
            "Preprocess and engineer features",
            "Train and compare regression models",
            "Evaluate with RMSE, MAE, and R² metrics",
            "Diagnose overfitting using residual analysis",
        ]
