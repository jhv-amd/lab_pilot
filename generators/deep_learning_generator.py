"""Generator for deep learning labs."""

from typing import Any, Dict, List

from generators.base_generator import BaseLabGenerator


class DeepLearningGenerator(BaseLabGenerator):

    @property
    def task_type(self) -> str:
        return "deep_learning"

    def get_exercises(self) -> List[Dict[str, Any]]:
        diff = self.difficulty
        return [
            self._data_exploration_exercise(),
            self._preprocessing_exercise(),
            self._model_architecture_exercise(diff),
            self._training_exercise(diff),
            self._evaluation_exercise(),
        ]

    def _data_exploration_exercise(self) -> Dict:
        return {
            "title": "Exercise 1: Data Exploration",
            "function_name": "explore_data",
            "points": 10,
            "instructions": "Explore the dataset shape, class distribution, and sample examples.",
            "starter_code": (
                "def explore_data(X, y):\n"
                "    \"\"\"\n"
                "    Explore the dataset.\n"
                "    Returns: dict with n_samples, n_classes, input_shape\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    result = {}\n"
                "    ### END CODE HERE ###\n"
                "    return result"
            ),
            "solution_code": (
                "def explore_data(X, y):\n"
                "    return {\n"
                "        'n_samples': len(X),\n"
                "        'n_classes': len(np.unique(y)),\n"
                "        'input_shape': X.shape[1:],\n"
                "    }"
            ),
            "public_tests": [
                "assert callable(func)\n"
                "X_dummy = np.zeros((100, 28, 28))\n"
                "y_dummy = np.arange(100) % 10\n"
                "result = func(X_dummy, y_dummy)\n"
                "assert isinstance(result, dict)\n"
                "assert 'n_samples' in result\n"
                "assert result['n_samples'] == 100"
            ],
            "hidden_tests": ["assert result['n_classes'] == len(np.unique(y_dummy))"],
            "hints": ["Hint: Use np.unique(y) to count classes"],
        }

    def _preprocessing_exercise(self) -> Dict:
        return {
            "title": "Exercise 2: Preprocessing",
            "function_name": "preprocess",
            "points": 20,
            "instructions": (
                "Normalize pixel values to [0, 1] and convert labels to one-hot encoding.\n\n"
                "Returns: `(X_train, X_test, y_train, y_test)`"
            ),
            "starter_code": (
                "def preprocess(X, y, n_classes=10):\n"
                "    \"\"\"\n"
                "    Normalize X to [0,1] and one-hot encode y.\n"
                "    Returns (X_train, X_test, y_train_oh, y_test_oh)\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    X_train, X_test, y_train, y_test = None, None, None, None\n"
                "    ### END CODE HERE ###\n"
                "    return X_train, X_test, y_train, y_test"
            ),
            "solution_code": (
                "def preprocess(X, y, n_classes=10):\n"
                "    from sklearn.model_selection import train_test_split\n"
                "    X = X.astype('float32') / 255.0\n"
                "    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
                "    y_train_oh = tf.keras.utils.to_categorical(y_train, n_classes)\n"
                "    y_test_oh = tf.keras.utils.to_categorical(y_test, n_classes)\n"
                "    return X_train, X_test, y_train_oh, y_test_oh"
            ),
            "public_tests": [
                "X_dummy = np.random.randint(0, 255, (200, 28, 28)).astype('uint8')\n"
                "y_dummy = np.arange(200) % 10\n"
                "result = func(X_dummy, y_dummy)\n"
                "assert len(result) == 4\n"
                "X_tr, X_te, y_tr, y_te = result\n"
                "assert X_tr.max() <= 1.0, 'X must be normalized to [0,1]'"
            ],
            "hidden_tests": ["assert X_te.max() <= 1.0\nassert y_tr.shape[1] == 10"],
            "hints": ["Hint: Divide X by 255.0", "Hint: Use tf.keras.utils.to_categorical for one-hot encoding"],
        }

    def _model_architecture_exercise(self, difficulty: str) -> Dict:
        depth_hint = {"beginner": "2-3 Dense layers", "intermediate": "Conv2D + Dense layers", "advanced": ""}
        return {
            "title": "Exercise 3: Model Architecture",
            "function_name": "build_model",
            "points": 30,
            "instructions": (
                "Design a neural network architecture.\n\n"
                "**Requirements:**\n"
                "- Returns a compiled Keras model\n"
                "- Use appropriate output activation and loss"
                + (f"\n- Suggested: {depth_hint[difficulty]}" if depth_hint.get(difficulty) else "")
            ),
            "starter_code": (
                "def build_model(input_shape, n_classes):\n"
                "    \"\"\"\n"
                "    Build and compile a neural network.\n"
                "    Returns: compiled keras model\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    model = None\n"
                "    ### END CODE HERE ###\n"
                "    return model"
            ),
            "solution_code": (
                "def build_model(input_shape, n_classes):\n"
                "    model = keras.Sequential([\n"
                "        layers.Flatten(input_shape=input_shape),\n"
                "        layers.Dense(128, activation='relu'),\n"
                "        layers.Dropout(0.3),\n"
                "        layers.Dense(64, activation='relu'),\n"
                "        layers.Dense(n_classes, activation='softmax'),\n"
                "    ])\n"
                "    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])\n"
                "    return model"
            ),
            "public_tests": [
                "model = func((28, 28), 10)\n"
                "assert model is not None, 'Must return a model'\n"
                "assert hasattr(model, 'predict'), 'Must be a compiled model'\n"
                "assert model.loss is not None, 'Model must be compiled'"
            ],
            "hidden_tests": ["assert model.optimizer is not None\nassert len(model.layers) >= 2"],
            "hints": ["Hint: Use keras.Sequential with Dense layers", "Hint: Use 'softmax' for multiclass output"],
        }

    def _training_exercise(self, difficulty: str) -> Dict:
        min_acc = self.difficulty_cfg.get("min_accuracy_classification", 0.80)
        return {
            "title": "Exercise 4: Model Training",
            "function_name": "train_model",
            "points": 30,
            "instructions": (
                f"Train the model. Target validation accuracy ≥ {min_acc*100:.0f}%.\n\n"
                "**Requirements:** Returns training `history` object."
            ),
            "starter_code": (
                "def train_model(model, X_train, y_train, epochs=10, batch_size=32):\n"
                "    \"\"\"\n"
                "    Train the model and return history.\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    history = None\n"
                "    ### END CODE HERE ###\n"
                "    return history"
            ),
            "solution_code": (
                "def train_model(model, X_train, y_train, epochs=10, batch_size=32):\n"
                "    history = model.fit(\n"
                "        X_train, y_train,\n"
                "        epochs=epochs,\n"
                "        batch_size=batch_size,\n"
                "        validation_split=0.1,\n"
                "        verbose=1,\n"
                "    )\n"
                "    return history"
            ),
            "public_tests": [
                "assert callable(func)\n"
                "assert func is not None"
            ],
            "hidden_tests": [
                "assert history is not None\n"
                "assert 'accuracy' in history.history or 'loss' in history.history"
            ],
            "hints": ["Hint: Use model.fit() and store the result"],
        }

    def _evaluation_exercise(self) -> Dict:
        return {
            "title": "Exercise 5: Evaluation",
            "function_name": "evaluate_model",
            "points": 10,
            "instructions": "Evaluate model on the test set. Return dict with `accuracy` and `loss`.",
            "starter_code": (
                "def evaluate_model(model, X_test, y_test):\n"
                "    \"\"\"Returns dict with accuracy and loss.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    metrics = {}\n"
                "    ### END CODE HERE ###\n"
                "    return metrics"
            ),
            "solution_code": (
                "def evaluate_model(model, X_test, y_test):\n"
                "    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)\n"
                "    return {'loss': float(loss), 'accuracy': float(accuracy)}"
            ),
            "public_tests": ["assert callable(func)"],
            "hidden_tests": ["assert 'accuracy' in result\nassert 0 <= result['accuracy'] <= 1"],
            "hints": ["Hint: Use model.evaluate()"],
        }

    def get_imports(self) -> List[str]:
        return [
            "import numpy as np",
            "import matplotlib.pyplot as plt",
            "import tensorflow as tf",
            "from tensorflow import keras",
            "from tensorflow.keras import layers",
            "from sklearn.model_selection import train_test_split",
            "from sklearn.metrics import classification_report",
            "from utils import plot_training_history",
        ]

    def get_description(self) -> str:
        return (
            f"Build and train a neural network for **{self.topic}**. "
            f"You will design an architecture, train it, and analyze learning curves."
        )

    def get_learning_objectives(self) -> List[str]:
        return [
            "Preprocess image/tabular data for neural networks",
            "Design a feedforward or convolutional neural network",
            "Train with mini-batch gradient descent",
            "Diagnose underfitting and overfitting via learning curves",
            "Evaluate with accuracy and loss metrics",
        ]
