"""Library of reusable exercise specifications for ML labs."""

from typing import Any, Dict

from components.test_library import TestLibrary


class ExerciseLibrary:
    """Return complete exercise specification dicts for common ML tasks."""

    # ── Data Exploration ──────────────────────────────────────────────────────

    @staticmethod
    def data_exploration(dataset_type: str, difficulty: str) -> Dict[str, Any]:
        instructions = {
            "beginner": (
                "Analyze the dataset and return basic statistics.\n\n"
                "**Requirements:** Return a dict with:\n"
                "- `missing_count`: total number of missing values (int)\n"
                "- `n_rows`: number of rows (int)\n"
                "- `n_features`: number of feature columns (int)\n\n"
                "> Hint: Use `df.isnull().sum().sum()` for missing values."
            ),
            "intermediate": (
                "Perform exploratory data analysis.\n\n"
                "Return a dict with `missing_count`, `n_rows`, `n_features`."
            ),
            "advanced": (
                "Analyze the dataset. Return `missing_count`, `n_rows`, `n_features`."
            ),
        }
        starter = {
            "beginner": (
                "def explore_data(df):\n"
                "    \"\"\"\n"
                "    Analyze dataset statistics.\n"
                "    Returns: dict with missing_count, n_rows, n_features\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    result = {\n"
                "        'missing_count': 0,   # TODO: count total NaN values\n"
                "        'n_rows': 0,          # TODO: number of rows\n"
                "        'n_features': 0,      # TODO: number of feature columns\n"
                "    }\n"
                "    ### END CODE HERE ###\n"
                "    return result"
            ),
            "intermediate": (
                "def explore_data(df):\n"
                "    \"\"\"Returns dict with missing_count, n_rows, n_features.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    result = {}\n"
                "    ### END CODE HERE ###\n"
                "    return result"
            ),
            "advanced": (
                "def explore_data(df):\n"
                "    ### START CODE HERE ###\n"
                "    result = {}\n"
                "    ### END CODE HERE ###\n"
                "    return result"
            ),
        }
        solution = (
            "def explore_data(df):\n"
            "    return {\n"
            "        'missing_count': int(df.isnull().sum().sum()),\n"
            "        'n_rows': len(df),\n"
            "        'n_features': len(df.columns) - 1,\n"
            "    }"
        )
        public_test = (
            "result = func(df)\n"
            "assert isinstance(result, dict), 'Must return a dict'\n"
            "assert 'missing_count' in result\n"
            "assert 'n_rows' in result\n"
            "assert result['n_rows'] == len(df)"
        )
        hidden_test = (
            "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
            "result = func(df)\n"
            "assert result['missing_count'] == int(df.isnull().sum().sum())\n"
            "assert result['n_rows'] == len(df)"
        )
        return {
            "title": "Exercise 1: Data Exploration",
            "function_name": "explore_data",
            "points": 10,
            "instructions": instructions.get(difficulty, instructions["intermediate"]),
            "starter_code": starter.get(difficulty, starter["intermediate"]),
            "solution_code": solution,
            "public_tests": [public_test],
            "hidden_tests": [hidden_test],
            "hints": ["Hint: Use df.isnull().sum().sum() for missing count"],
        }

    # ── Preprocessing ─────────────────────────────────────────────────────────

    @staticmethod
    def preprocessing(task_type: str, difficulty: str) -> Dict[str, Any]:
        hints = {
            "beginner": [
                "Hint: Drop non-numeric columns before splitting",
                "Hint: Use train_test_split(X, y, test_size=0.2, random_state=42)",
                "Hint: Fill missing values with df.fillna(df.median())",
            ],
            "intermediate": ["Hint: Handle NaN values before splitting"],
            "advanced": [],
        }
        starter_beginner = (
            "def preprocess(df):\n"
            "    \"\"\"\n"
            "    Prepare data for training.\n"
            "    Returns: (X_train, X_test, y_train, y_test)\n"
            "    \"\"\"\n"
            "    ### START CODE HERE ###\n"
            "    # Step 1: Separate features and target\n"
            "    # target_col = 'YOUR_TARGET_COLUMN'\n"
            "    # X = df.drop(columns=[target_col, 'id_column'])\n"
            "    # y = df[target_col]\n"
            "    \n"
            "    # Step 2: Keep only numeric columns\n"
            "    # X = X.select_dtypes(include=[np.number])\n"
            "    \n"
            "    # Step 3: Handle missing values\n"
            "    # X = X.fillna(X.median())\n"
            "    \n"
            "    # Step 4: Split\n"
            "    X_train, X_test, y_train, y_test = None, None, None, None\n"
            "    ### END CODE HERE ###\n"
            "    return X_train, X_test, y_train, y_test"
        )
        starter_other = (
            "def preprocess(df):\n"
            "    \"\"\"Returns (X_train, X_test, y_train, y_test). 80/20 split, no NaN.\"\"\"\n"
            "    ### START CODE HERE ###\n"
            "    X_train, X_test, y_train, y_test = None, None, None, None\n"
            "    ### END CODE HERE ###\n"
            "    return X_train, X_test, y_train, y_test"
        )
        solution = (
            "def preprocess(df):\n"
            "    non_numeric = df.select_dtypes(exclude=[np.number]).columns.tolist()\n"
            "    target_col = df.columns[-1]\n"
            "    id_cols = [c for c in non_numeric if 'id' in c.lower()]\n"
            "    X = df.drop(columns=[target_col] + id_cols + [c for c in non_numeric if c != target_col])\n"
            "    X = X.select_dtypes(include=[np.number]).fillna(X.median(numeric_only=True))\n"
            "    y = df[target_col]\n"
            "    return train_test_split(X, y, test_size=0.2, random_state=42)"
        )
        public_test = (
            "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
            "result = func(df)\n"
            "assert len(result) == 4, 'Must return 4 values: X_train, X_test, y_train, y_test'\n"
            "X_train, X_test, y_train, y_test = result\n"
            "assert len(X_train) > 0, 'X_train is empty'\n"
            "assert X_train.isnull().sum().sum() == 0, 'NaN values in X_train'"
        )
        hidden_test = (
            "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
            "X_train, X_test, y_train, y_test = func(df)\n"
            "total = len(X_train) + len(X_test)\n"
            "ratio = len(X_test) / total\n"
            "assert abs(ratio - 0.2) <= 0.05, f'Split ratio {ratio:.2f} != 0.2'\n"
            "assert X_train.isnull().sum().sum() == 0"
        )
        return {
            "title": "Exercise 2: Data Preprocessing",
            "function_name": "preprocess",
            "points": 20,
            "instructions": (
                "Clean and split the dataset for training.\n\n"
                "**Requirements:**\n"
                "- Drop non-numeric and ID columns\n"
                "- Fill or drop missing values\n"
                "- Split into 80% train / 20% test (random_state=42)\n"
                "- Return `(X_train, X_test, y_train, y_test)`"
            ),
            "starter_code": starter_beginner if difficulty == "beginner" else starter_other,
            "solution_code": solution,
            "public_tests": [public_test],
            "hidden_tests": [hidden_test],
            "hints": hints.get(difficulty, []),
        }

    # ── Model Building ────────────────────────────────────────────────────────

    @staticmethod
    def model_building(model_type: str, difficulty: str) -> Dict[str, Any]:
        thresholds = {"beginner": 0.70, "intermediate": 0.80, "advanced": 0.85}
        min_acc = thresholds.get(difficulty, 0.75)
        hints = {
            "beginner": [
                "Hint: Try RandomForestClassifier(n_estimators=100, random_state=42)",
                f"Hint: Target accuracy ≥ {min_acc}",
            ],
            "intermediate": [f"Hint: Target accuracy ≥ {min_acc}"],
            "advanced": [],
        }
        starter = (
            f"def train_{model_type}(X_train, y_train):\n"
            f"    \"\"\"\n"
            f"    Train a {model_type} model.\n"
            f"    Returns: fitted model with .predict() method\n"
            f"    \"\"\"\n"
            f"    ### START CODE HERE ###\n"
            + ("    # Hint: Try RandomForestClassifier or LogisticRegression\n" if difficulty == "beginner" else "")
            + f"    model = None\n"
            f"    ### END CODE HERE ###\n"
            f"    return model"
        )
        solution = (
            f"def train_{model_type}(X_train, y_train):\n"
            f"    from sklearn.ensemble import RandomForestClassifier\n"
            f"    model = RandomForestClassifier(n_estimators=100, random_state=42)\n"
            f"    model.fit(X_train, y_train)\n"
            f"    return model"
        )
        public_test = (
            "assert func is not None, 'Function must not be None'\n"
            "assert callable(func), 'Must be callable'\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "X, y = make_classification(n_samples=200, n_features=5, random_state=42)\n"
            "X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            f"model = func(X_tr, y_tr)\n"
            "assert model is not None, 'train function returned None'\n"
            "assert hasattr(model, 'predict'), 'Model must have predict()'"
        )
        hidden_test = (
            "import warnings\n"
            "from sklearn.metrics import accuracy_score\n"
            "from sklearn.model_selection import train_test_split\n"
            "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
            "X = df.select_dtypes(include=[np.number]).drop(columns=[df.columns[-1]], errors='ignore').fillna(0)\n"
            "y = df.iloc[:, -1]\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "with warnings.catch_warnings():\n"
            "    warnings.simplefilter('ignore')\n"
            f"    model = func(X_train, y_train)\n"
            "preds = model.predict(X_test)\n"
            "acc = accuracy_score(y_test, preds)\n"
            f"assert acc >= {min_acc}, f'Accuracy {{acc:.3f}} < {min_acc}'"
        )
        return {
            "title": "Exercise 3: Build Model",
            "function_name": f"train_{model_type}",
            "points": 30,
            "instructions": (
                f"Train a {model_type} model.\n\n"
                f"**Requirements:**\n"
                f"- Accept `X_train, y_train` as inputs\n"
                f"- Return a fitted scikit-learn model\n"
                f"- Achieve at least {min_acc*100:.0f}% accuracy on the test set"
            ),
            "starter_code": starter,
            "solution_code": solution,
            "public_tests": [public_test],
            "hidden_tests": [hidden_test],
            "hints": hints.get(difficulty, []),
        }

    # ── Model Evaluation ──────────────────────────────────────────────────────

    @staticmethod
    def model_evaluation(task_type: str, difficulty: str) -> Dict[str, Any]:
        if task_type == "regression":
            metrics_list = "rmse, r2, mae"
            solution = (
                "def evaluate_model(model, X_test, y_test):\n"
                "    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error\n"
                "    import numpy as np\n"
                "    preds = model.predict(X_test)\n"
                "    return {\n"
                "        'rmse': float(np.sqrt(mean_squared_error(y_test, preds))),\n"
                "        'r2': float(r2_score(y_test, preds)),\n"
                "        'mae': float(mean_absolute_error(y_test, preds)),\n"
                "    }"
            )
            required_keys = ["rmse", "r2", "mae"]
        else:
            metrics_list = "accuracy, precision, recall, f1"
            solution = (
                "def evaluate_model(model, X_test, y_test):\n"
                "    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score\n"
                "    preds = model.predict(X_test)\n"
                "    return {\n"
                "        'accuracy': float(accuracy_score(y_test, preds)),\n"
                "        'precision': float(precision_score(y_test, preds, average='weighted', zero_division=0)),\n"
                "        'recall': float(recall_score(y_test, preds, average='weighted', zero_division=0)),\n"
                "        'f1': float(f1_score(y_test, preds, average='weighted', zero_division=0)),\n"
                "    }"
            )
            required_keys = ["accuracy", "precision", "recall", "f1"]

        starter = (
            "def evaluate_model(model, X_test, y_test):\n"
            f"    \"\"\"\n"
            f"    Evaluate model performance.\n"
            f"    Returns: dict with {metrics_list}\n"
            f"    \"\"\"\n"
            "    ### START CODE HERE ###\n"
            "    metrics = {}\n"
            "    ### END CODE HERE ###\n"
            "    return metrics"
        )
        keys_repr = repr(required_keys)
        public_test = (
            "from sklearn.dummy import DummyClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "X, y = make_classification(n_samples=100, n_features=5, random_state=42)\n"
            "model = DummyClassifier(strategy='most_frequent')\n"
            "import warnings\n"
            "with warnings.catch_warnings():\n"
            "    warnings.simplefilter('ignore')\n"
            "    model.fit(X, y)\n"
            "result = func(model, X, y)\n"
            f"assert isinstance(result, dict), 'Must return a dict'\n"
            f"missing = set({keys_repr}) - set(result.keys())\n"
            f"assert not missing, f'Missing keys: {{missing}}'"
        )
        return {
            "title": "Exercise 4: Model Evaluation",
            "function_name": "evaluate_model",
            "points": 30,
            "instructions": (
                f"Compute model evaluation metrics.\n\n"
                f"**Requirements:** Return a dict with: `{metrics_list}`"
            ),
            "starter_code": starter,
            "solution_code": solution,
            "public_tests": [public_test],
            "hidden_tests": [public_test],
            "hints": [],
        }

    # ── Hyperparameter Tuning ─────────────────────────────────────────────────

    @staticmethod
    def hyperparameter_tuning(model_type: str, difficulty: str) -> Dict[str, Any]:
        starter = (
            "def tune_hyperparameters(X_train, y_train):\n"
            "    \"\"\"\n"
            "    Tune model hyperparameters using GridSearchCV.\n"
            "    Returns: (best_model, best_params)\n"
            "    \"\"\"\n"
            "    ### START CODE HERE ###\n"
            + ("    # Hint: Use GridSearchCV with param_grid\n" if difficulty == "beginner" else "")
            + "    best_model, best_params = None, {}\n"
            "    ### END CODE HERE ###\n"
            "    return best_model, best_params"
        )
        solution = (
            "def tune_hyperparameters(X_train, y_train):\n"
            "    from sklearn.ensemble import RandomForestClassifier\n"
            "    from sklearn.model_selection import GridSearchCV\n"
            "    param_grid = {'n_estimators': [50, 100], 'max_depth': [None, 5, 10]}\n"
            "    gs = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, n_jobs=-1)\n"
            "    gs.fit(X_train, y_train)\n"
            "    return gs.best_estimator_, gs.best_params_"
        )
        public_test = (
            "assert callable(func), 'Must be callable'\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "X, y = make_classification(n_samples=200, n_features=5, random_state=42)\n"
            "X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "import warnings\n"
            "with warnings.catch_warnings():\n"
            "    warnings.simplefilter('ignore')\n"
            "    result = func(X_tr, y_tr)\n"
            "assert len(result) == 2, 'Must return (best_model, best_params)'\n"
            "best_model, best_params = result\n"
            "assert hasattr(best_model, 'predict'), 'best_model must have predict()'\n"
            "assert isinstance(best_params, dict), 'best_params must be a dict'"
        )
        return {
            "title": "Bonus Exercise: Hyperparameter Tuning",
            "function_name": "tune_hyperparameters",
            "points": 10,
            "instructions": (
                "Improve your model by tuning hyperparameters.\n\n"
                "**Requirements:**\n"
                "- Use `GridSearchCV` or `RandomizedSearchCV`\n"
                "- Return `(best_model, best_params)`"
            ),
            "starter_code": starter,
            "solution_code": solution,
            "public_tests": [public_test],
            "hidden_tests": [public_test],
            "hints": ["Hint: Try tuning n_estimators and max_depth"],
        }
