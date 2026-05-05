"""Reusable test code snippets for public and hidden test files."""


class TestLibrary:
    """Factory for test code strings inserted into generated test modules."""

    @staticmethod
    def test_function_exists(function_name: str) -> str:
        return (
            f"assert {function_name} is not None, 'Function {function_name} must not be None'\n"
            f"assert callable({function_name}), '{function_name} must be callable'"
        )

    @staticmethod
    def test_return_type(function_name: str, expected_type: str) -> str:
        type_map = {
            "dict": "dict",
            "model": "object",
            "dataframe": "pd.DataFrame",
            "ndarray": "np.ndarray",
            "tuple": "tuple",
            "list": "list",
            "float": "float",
            "int": "int",
        }
        python_type = type_map.get(expected_type, "object")
        return f"result = {function_name}()\nassert isinstance(result, {python_type}), f'Expected {expected_type}, got {{type(result)}}'"

    @staticmethod
    def test_model_accuracy(min_accuracy: float, task: str = "classification") -> str:
        if task == "classification":
            return (
                "from sklearn.metrics import accuracy_score\n"
                "preds = func.predict(X_test)\n"
                f"acc = accuracy_score(y_test, preds)\n"
                f"assert acc >= {min_accuracy}, f'Accuracy {{acc:.3f}} < minimum {min_accuracy}'"
            )
        return (
            "from sklearn.metrics import r2_score\n"
            "preds = func.predict(X_test)\n"
            f"r2 = r2_score(y_test, preds)\n"
            f"assert r2 >= {min_accuracy}, f'R² {{r2:.3f}} < minimum {min_accuracy}'"
        )

    @staticmethod
    def test_no_data_leakage() -> str:
        return (
            "# Ensure model is not fitted on test data\n"
            "import inspect\n"
            "src = inspect.getsource(func)\n"
            "assert 'test' not in src.lower().replace('test_', ''), 'Possible test data leakage detected'"
        )

    @staticmethod
    def test_no_overfitting(max_gap: float = 0.10) -> str:
        return (
            "from sklearn.metrics import accuracy_score\n"
            "train_acc = accuracy_score(y_train, func.predict(X_train))\n"
            "test_acc = accuracy_score(y_test, func.predict(X_test))\n"
            f"assert (train_acc - test_acc) <= {max_gap}, "
            f"f'Overfitting detected: train={{train_acc:.3f}}, test={{test_acc:.3f}}'"
        )

    @staticmethod
    def test_dict_has_keys(keys: list) -> str:
        keys_repr = repr(keys)
        return (
            f"missing = set({keys_repr}) - set(result.keys())\n"
            f"assert not missing, f'Result dict missing keys: {{missing}}'"
        )

    @staticmethod
    def test_no_nans_in_output() -> str:
        return (
            "import pandas as pd, numpy as np\n"
            "if isinstance(result, pd.DataFrame):\n"
            "    assert result.isnull().sum().sum() == 0, 'Output contains NaN values'\n"
            "elif isinstance(result, np.ndarray):\n"
            "    assert not np.isnan(result).any(), 'Output contains NaN values'"
        )

    @staticmethod
    def test_split_ratio(test_size: float = 0.2, tolerance: float = 0.05) -> str:
        return (
            "X_train, X_test, y_train, y_test = result\n"
            "total = len(X_train) + len(X_test)\n"
            f"ratio = len(X_test) / total\n"
            f"assert abs(ratio - {test_size}) <= {tolerance}, "
            f"f'Test split {{ratio:.2f}} differs from expected {test_size}'"
        )
