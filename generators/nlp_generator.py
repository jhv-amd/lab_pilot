"""Generator for NLP labs."""

from typing import Any, Dict, List

from generators.base_generator import BaseLabGenerator


class NLPGenerator(BaseLabGenerator):

    @property
    def task_type(self) -> str:
        return "classification"

    def get_exercises(self) -> List[Dict[str, Any]]:
        diff = self.difficulty
        return [
            self._text_exploration_exercise(),
            self._tokenization_exercise(diff),
            self._feature_extraction_exercise(diff),
            self._model_training_exercise(diff),
            self._evaluation_exercise(),
        ]

    def _text_exploration_exercise(self) -> Dict:
        return {
            "title": "Exercise 1: Text Exploration",
            "function_name": "explore_text",
            "points": 10,
            "instructions": (
                "Analyze the text dataset.\n\n"
                "**Returns:** dict with `n_samples`, `avg_length`, `class_distribution` (dict of label→count)"
            ),
            "starter_code": (
                "def explore_text(df):\n"
                "    \"\"\"Analyze text dataset. Returns: dict with n_samples, avg_length, class_distribution.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    result = {}\n"
                "    ### END CODE HERE ###\n"
                "    return result"
            ),
            "solution_code": (
                "def explore_text(df):\n"
                "    text_col = df.select_dtypes(include='object').columns[0]\n"
                "    label_col = df.columns[-1]\n"
                "    return {\n"
                "        'n_samples': len(df),\n"
                "        'avg_length': float(df[text_col].str.split().str.len().mean()),\n"
                "        'class_distribution': df[label_col].value_counts().to_dict(),\n"
                "    }"
            ),
            "public_tests": [
                "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
                "result = func(df)\n"
                "assert isinstance(result, dict)\n"
                "assert 'n_samples' in result\n"
                "assert result['n_samples'] == len(df)"
            ],
            "hidden_tests": [
                "assert 'avg_length' in result\n"
                "assert 'class_distribution' in result\n"
                "assert sum(result['class_distribution'].values()) == len(df)"
            ],
            "hints": ["Hint: Use df['text'].str.split().str.len().mean() for average length"],
        }

    def _tokenization_exercise(self, difficulty: str) -> Dict:
        hints = {
            "beginner": ["Hint: Use re.sub to remove special characters", "Hint: Use .lower() to lowercase"],
            "intermediate": ["Hint: Remove punctuation and lowercase"],
            "advanced": [],
        }
        return {
            "title": "Exercise 2: Text Cleaning & Tokenization",
            "function_name": "clean_text",
            "points": 20,
            "instructions": (
                "Clean and tokenize text data.\n\n"
                "**Requirements:**\n"
                "- Lowercase all text\n"
                "- Remove punctuation and special characters\n"
                "- Return a list of cleaned text strings"
            ),
            "starter_code": (
                "def clean_text(texts):\n"
                "    \"\"\"\n"
                "    Clean a list of text strings.\n"
                "    Returns: list of cleaned strings\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    cleaned = []\n"
                "    ### END CODE HERE ###\n"
                "    return cleaned"
            ),
            "solution_code": (
                "def clean_text(texts):\n"
                "    cleaned = []\n"
                "    for text in texts:\n"
                "        text = str(text).lower()\n"
                "        text = re.sub(r'[^a-z0-9\\s]', '', text)\n"
                "        text = ' '.join(text.split())\n"
                "        cleaned.append(text)\n"
                "    return cleaned"
            ),
            "public_tests": [
                "samples = ['Hello, World!', 'Test 123!!', '   spaces   ']\n"
                "result = func(samples)\n"
                "assert len(result) == 3\n"
                "assert all(c == c.lower() for c in result), 'Text must be lowercased'\n"
                "assert ',' not in result[0], 'Punctuation must be removed'"
            ],
            "hidden_tests": [
                "assert '!' not in result[1]\n"
                "assert result[2].strip() == result[2], 'Leading/trailing spaces removed'"
            ],
            "hints": hints.get(difficulty, []),
        }

    def _feature_extraction_exercise(self, difficulty: str) -> Dict:
        return {
            "title": "Exercise 3: Feature Extraction",
            "function_name": "extract_features",
            "points": 20,
            "instructions": (
                "Convert cleaned text to numerical features using TF-IDF.\n\n"
                "**Returns:** `(X_train, X_test, y_train, y_test)` where X is a TF-IDF matrix"
            ),
            "starter_code": (
                "def extract_features(train_df, test_size=0.2):\n"
                "    \"\"\"\n"
                "    Extract TF-IDF features.\n"
                "    Returns: (X_train, X_test, y_train, y_test)\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                + ("    # Hint: Use TfidfVectorizer\n" if difficulty == "beginner" else "")
                + "    X_train, X_test, y_train, y_test = None, None, None, None\n"
                "    ### END CODE HERE ###\n"
                "    return X_train, X_test, y_train, y_test"
            ),
            "solution_code": (
                "def extract_features(train_df, test_size=0.2):\n"
                "    from sklearn.feature_extraction.text import TfidfVectorizer\n"
                "    text_col = train_df.select_dtypes(include='object').columns[0]\n"
                "    label_col = train_df.columns[-1]\n"
                "    texts = clean_text(train_df[text_col].tolist())\n"
                "    labels = train_df[label_col].values\n"
                "    X_tr_raw, X_te_raw, y_train, y_test = train_test_split(\n"
                "        texts, labels, test_size=test_size, random_state=42)\n"
                "    vec = TfidfVectorizer(max_features=5000)\n"
                "    X_train = vec.fit_transform(X_tr_raw)\n"
                "    X_test = vec.transform(X_te_raw)\n"
                "    return X_train, X_test, y_train, y_test"
            ),
            "public_tests": [
                "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
                "result = func(df)\n"
                "assert len(result) == 4\n"
                "X_train, X_test, y_train, y_test = result\n"
                "assert X_train.shape[0] > 0\n"
                "assert X_train.shape[1] == X_test.shape[1], 'Train/test must have same features'"
            ],
            "hidden_tests": ["assert len(y_train) == X_train.shape[0]"],
            "hints": ["Hint: Fit TfidfVectorizer on train only, then transform test"],
        }

    def _model_training_exercise(self, difficulty: str) -> Dict:
        min_acc = self.difficulty_cfg.get("min_accuracy_classification", 0.80)
        return {
            "title": "Exercise 4: Model Training",
            "function_name": "train_classifier",
            "points": 30,
            "instructions": (
                f"Train a text classification model. Target accuracy ≥ {min_acc*100:.0f}%.\n\n"
                "**Returns:** fitted scikit-learn classifier"
            ),
            "starter_code": (
                "def train_classifier(X_train, y_train):\n"
                "    \"\"\"Train a text classifier. Returns fitted model.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                + ("    # Hint: Try LogisticRegression or MultinomialNB\n" if difficulty == "beginner" else "")
                + "    model = None\n"
                "    ### END CODE HERE ###\n"
                "    return model"
            ),
            "solution_code": (
                "def train_classifier(X_train, y_train):\n"
                "    from sklearn.linear_model import LogisticRegression\n"
                "    model = LogisticRegression(max_iter=1000, random_state=42)\n"
                "    model.fit(X_train, y_train)\n"
                "    return model"
            ),
            "public_tests": [
                "assert callable(func)\n"
                "from sklearn.datasets import make_classification\n"
                "X, y = make_classification(n_samples=200, n_features=20, random_state=42)\n"
                "model = func(X, y)\n"
                "assert model is not None\n"
                "assert hasattr(model, 'predict')"
            ],
            "hidden_tests": [
                f"from sklearn.metrics import accuracy_score\n"
                "preds = model.predict(X_test)\n"
                f"acc = accuracy_score(y_test, preds)\n"
                f"assert acc >= {min_acc}, f'Accuracy {{acc:.3f}} < {min_acc}'"
            ],
            "hints": ["Hint: Try LogisticRegression(max_iter=1000)"],
        }

    def _evaluation_exercise(self) -> Dict:
        return {
            "title": "Exercise 5: Evaluation",
            "function_name": "evaluate_classifier",
            "points": 20,
            "instructions": "Compute classification metrics. Return dict with `accuracy`, `precision`, `recall`, `f1`.",
            "starter_code": (
                "def evaluate_classifier(model, X_test, y_test):\n"
                "    \"\"\"Returns dict with accuracy, precision, recall, f1.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    metrics = {}\n"
                "    ### END CODE HERE ###\n"
                "    return metrics"
            ),
            "solution_code": (
                "def evaluate_classifier(model, X_test, y_test):\n"
                "    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score\n"
                "    preds = model.predict(X_test)\n"
                "    return {\n"
                "        'accuracy': float(accuracy_score(y_test, preds)),\n"
                "        'precision': float(precision_score(y_test, preds, average='weighted', zero_division=0)),\n"
                "        'recall': float(recall_score(y_test, preds, average='weighted', zero_division=0)),\n"
                "        'f1': float(f1_score(y_test, preds, average='weighted', zero_division=0)),\n"
                "    }"
            ),
            "public_tests": [
                "from sklearn.dummy import DummyClassifier\n"
                "from sklearn.datasets import make_classification\n"
                "X, y = make_classification(100, 5, random_state=42)\n"
                "m = DummyClassifier().fit(X, y)\n"
                "result = func(m, X, y)\n"
                "assert isinstance(result, dict)\n"
                "assert set(result.keys()) >= {'accuracy', 'f1'}"
            ],
            "hidden_tests": ["assert 0 <= result['accuracy'] <= 1\nassert 0 <= result['f1'] <= 1"],
            "hints": [],
        }

    def get_imports(self) -> List[str]:
        return [
            "import pandas as pd",
            "import numpy as np",
            "import re",
            "import string",
            "import matplotlib.pyplot as plt",
            "from sklearn.model_selection import train_test_split",
            "from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer",
            "from sklearn.linear_model import LogisticRegression",
            "from sklearn.naive_bayes import MultinomialNB",
            "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report",
        ]

    def get_description(self) -> str:
        return (
            f"Build a natural language processing pipeline for **{self.topic}**. "
            f"You will clean text, extract TF-IDF features, and train a text classifier."
        )

    def get_learning_objectives(self) -> List[str]:
        return [
            "Explore and visualize text datasets",
            "Apply text cleaning and tokenization",
            "Extract TF-IDF features",
            "Train and evaluate a text classifier",
            "Interpret precision, recall, and F1 for NLP tasks",
        ]
