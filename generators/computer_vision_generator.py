"""Generator for computer vision labs."""

from typing import Any, Dict, List

from generators.base_generator import BaseLabGenerator


class ComputerVisionGenerator(BaseLabGenerator):

    @property
    def task_type(self) -> str:
        return "deep_learning"

    def get_exercises(self) -> List[Dict[str, Any]]:
        return [
            self._data_exploration_exercise(),
            self._preprocessing_exercise(),
            self._cnn_architecture_exercise(),
            self._training_exercise(),
            self._evaluation_exercise(),
        ]

    def _data_exploration_exercise(self) -> Dict:
        return {
            "title": "Exercise 1: Image Data Exploration",
            "function_name": "explore_images",
            "points": 10,
            "instructions": (
                "Explore the image dataset.\n\n"
                "**Returns:** dict with `n_samples`, `image_shape`, `n_classes`"
            ),
            "starter_code": (
                "def explore_images(X, y):\n"
                "    \"\"\"Returns dict with n_samples, image_shape, n_classes.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    result = {}\n"
                "    ### END CODE HERE ###\n"
                "    return result"
            ),
            "solution_code": (
                "def explore_images(X, y):\n"
                "    return {'n_samples': len(X), 'image_shape': X.shape[1:], 'n_classes': len(np.unique(y))}"
            ),
            "public_tests": [
                "X_d = np.zeros((100, 32, 32, 3))\n"
                "y_d = np.arange(100) % 10\n"
                "result = func(X_d, y_d)\n"
                "assert result['n_samples'] == 100\n"
                "assert result['n_classes'] == 10"
            ],
            "hidden_tests": ["assert result['image_shape'] == (32, 32, 3)"],
            "hints": ["Hint: Use X.shape[1:] for image shape"],
        }

    def _preprocessing_exercise(self) -> Dict:
        return {
            "title": "Exercise 2: Image Preprocessing",
            "function_name": "preprocess_images",
            "points": 20,
            "instructions": (
                "Normalize images to [0, 1] and prepare train/test splits.\n\n"
                "**Returns:** `(X_train, X_test, y_train, y_test)` — X normalized, y as integers"
            ),
            "starter_code": (
                "def preprocess_images(X, y):\n"
                "    \"\"\"Normalize to [0,1] and split 80/20. Returns (X_train, X_test, y_train, y_test).\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    X_train, X_test, y_train, y_test = None, None, None, None\n"
                "    ### END CODE HERE ###\n"
                "    return X_train, X_test, y_train, y_test"
            ),
            "solution_code": (
                "def preprocess_images(X, y):\n"
                "    from sklearn.model_selection import train_test_split\n"
                "    X = X.astype('float32') / 255.0\n"
                "    return train_test_split(X, y, test_size=0.2, random_state=42)"
            ),
            "public_tests": [
                "X_d = np.random.randint(0, 255, (200, 32, 32, 3), dtype='uint8')\n"
                "y_d = np.arange(200) % 10\n"
                "X_tr, X_te, y_tr, y_te = func(X_d, y_d)\n"
                "assert X_tr.max() <= 1.0, 'Images must be normalized to [0,1]'\n"
                "assert len(X_tr) + len(X_te) == 200"
            ],
            "hidden_tests": ["assert abs(len(X_te) / 200 - 0.2) < 0.05"],
            "hints": ["Hint: Divide by 255.0 for normalization"],
        }

    def _cnn_architecture_exercise(self) -> Dict:
        min_acc = self.difficulty_cfg.get("min_accuracy_classification", 0.75)
        return {
            "title": "Exercise 3: CNN Architecture",
            "function_name": "build_cnn",
            "points": 30,
            "instructions": (
                "Design a Convolutional Neural Network.\n\n"
                "**Requirements:**\n"
                "- Include at least one Conv2D + MaxPooling2D block\n"
                "- Flatten and add Dense layers\n"
                "- Compile with optimizer, loss, and metrics\n"
                f"- Target validation accuracy ≥ {min_acc*100:.0f}%"
            ),
            "starter_code": (
                "def build_cnn(input_shape, n_classes):\n"
                "    \"\"\"\n"
                "    Build and compile a CNN.\n"
                "    Returns: compiled keras model\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    model = None\n"
                "    ### END CODE HERE ###\n"
                "    return model"
            ),
            "solution_code": (
                "def build_cnn(input_shape, n_classes):\n"
                "    model = keras.Sequential([\n"
                "        layers.Conv2D(32, (3,3), activation='relu', input_shape=input_shape),\n"
                "        layers.MaxPooling2D(2, 2),\n"
                "        layers.Conv2D(64, (3,3), activation='relu'),\n"
                "        layers.MaxPooling2D(2, 2),\n"
                "        layers.Flatten(),\n"
                "        layers.Dense(128, activation='relu'),\n"
                "        layers.Dropout(0.3),\n"
                "        layers.Dense(n_classes, activation='softmax'),\n"
                "    ])\n"
                "    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])\n"
                "    return model"
            ),
            "public_tests": [
                "model = func((32, 32, 3), 10)\n"
                "assert model is not None\n"
                "conv_layers = [l for l in model.layers if 'conv' in l.name]\n"
                "assert len(conv_layers) >= 1, 'Must include at least one Conv2D layer'"
            ],
            "hidden_tests": ["assert model.optimizer is not None\nassert len(model.layers) >= 4"],
            "hints": ["Hint: Use keras.Sequential with Conv2D and MaxPooling2D"],
        }

    def _training_exercise(self) -> Dict:
        return {
            "title": "Exercise 4: Model Training",
            "function_name": "train_cnn",
            "points": 30,
            "instructions": "Train the CNN model. Return the training history.",
            "starter_code": (
                "def train_cnn(model, X_train, y_train, epochs=10, batch_size=32):\n"
                "    \"\"\"Train the CNN. Returns history object.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    history = None\n"
                "    ### END CODE HERE ###\n"
                "    return history"
            ),
            "solution_code": (
                "def train_cnn(model, X_train, y_train, epochs=10, batch_size=32):\n"
                "    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,\n"
                "                        validation_split=0.1, verbose=1)\n"
                "    return history"
            ),
            "public_tests": ["assert callable(func)"],
            "hidden_tests": ["assert history is not None\nassert 'accuracy' in history.history"],
            "hints": ["Hint: Use model.fit() with validation_split=0.1"],
        }

    def _evaluation_exercise(self) -> Dict:
        return {
            "title": "Exercise 5: Evaluation & Visualization",
            "function_name": "evaluate_cnn",
            "points": 10,
            "instructions": "Evaluate the CNN on test data. Return dict with `accuracy` and `loss`.",
            "starter_code": (
                "def evaluate_cnn(model, X_test, y_test):\n"
                "    \"\"\"Returns dict with accuracy and loss.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    metrics = {}\n"
                "    ### END CODE HERE ###\n"
                "    return metrics"
            ),
            "solution_code": (
                "def evaluate_cnn(model, X_test, y_test):\n"
                "    loss, acc = model.evaluate(X_test, y_test, verbose=0)\n"
                "    return {'accuracy': float(acc), 'loss': float(loss)}"
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
            "from utils import plot_training_history",
        ]

    def get_description(self) -> str:
        return (
            f"Build a Convolutional Neural Network for **{self.topic}**. "
            f"You will design a CNN architecture, train it on image data, and evaluate performance."
        )

    def get_learning_objectives(self) -> List[str]:
        return [
            "Understand image data representation (height, width, channels)",
            "Apply image normalization and preprocessing",
            "Design a CNN with convolutional and pooling layers",
            "Train with early stopping and batch normalization",
            "Visualize learning curves and class activation maps",
        ]
