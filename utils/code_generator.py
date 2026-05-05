"""Generate Python source strings for tests and utilities."""

from typing import List


class CodeGenerator:
    """Generate Python source code strings for lab components."""

    @staticmethod
    def generate_public_tests_module(exercises: List[dict], dataset_type: str) -> str:
        lines = [
            '"""Public tests — visible to students. Basic sanity checks only."""',
            "",
            "import numpy as np",
            "import pandas as pd",
            "from pathlib import Path",
            "",
            "DATA_DIR = Path(__file__).parent / 'data'",
            "",
        ]
        for ex in exercises:
            fn = ex.get("function_name", "exercise")
            public_tests = ex.get("public_tests", [])
            lines.append(f"def test_{fn}(func):")
            if public_tests:
                for test_body in public_tests:
                    # indent each line of the test body
                    for line in test_body.strip().splitlines():
                        lines.append(f"    {line}")
            else:
                lines.append(f"    assert func is not None, '{fn} must not be None'")
                lines.append(f"    assert callable(func), '{fn} must be callable'")
            lines.append(f"    print('  ✓ test_{fn} passed')")
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def generate_hidden_tests_module(exercises: List[dict], difficulty_cfg: dict) -> str:
        lines = [
            '"""Hidden grading tests — not distributed to students."""',
            "",
            "import warnings",
            "import numpy as np",
            "import pandas as pd",
            "from pathlib import Path",
            "from typing import Dict",
            "",
            "DATA_DIR = Path(__file__).parent / 'data'",
            "",
        ]
        for ex in exercises:
            fn = ex.get("function_name", "exercise")
            max_pts = ex.get("points", 10)
            hidden_tests = ex.get("hidden_tests", [])

            lines += [
                f"def test_{fn}_comprehensive(func) -> Dict:",
                f"    try:",
            ]
            if hidden_tests:
                for test_body in hidden_tests:
                    for line in test_body.strip().splitlines():
                        lines.append(f"        {line}")
            else:
                lines.append(f"        assert func is not None, 'Function must not be None'")

            lines += [
                f"        return {{'passed': True, 'score': {max_pts}, 'max_score': {max_pts}, 'feedback': 'All checks passed'}}",
                f"    except AssertionError as e:",
                f"        return {{'passed': False, 'score': 0, 'max_score': {max_pts}, 'feedback': str(e)}}",
                f"    except Exception as e:",
                f"        return {{'passed': False, 'score': 0, 'max_score': {max_pts}, 'feedback': f'Error: {{e}}'}}",
                "",
                f"test_{fn}_comprehensive.max_score = {max_pts}",
                "",
            ]
        return "\n".join(lines)

    @staticmethod
    def generate_utils_module(topic: str, task_type: str) -> str:
        lines = [
            f'"""Utility functions for the {topic} lab."""',
            "",
            "import matplotlib.pyplot as plt",
            "import numpy as np",
            "import seaborn as sns",
            "",
        ]
        if task_type == "classification":
            lines += [
                "from sklearn.metrics import confusion_matrix",
                "",
                "def plot_confusion_matrix(y_true, y_pred, labels=None, title='Confusion Matrix'):",
                "    cm = confusion_matrix(y_true, y_pred)",
                "    fig, ax = plt.subplots(figsize=(6, 5))",
                "    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',",
                "                xticklabels=labels or ['Class 0', 'Class 1'],",
                "                yticklabels=labels or ['Class 0', 'Class 1'], ax=ax)",
                "    ax.set_xlabel('Predicted'); ax.set_ylabel('Actual'); ax.set_title(title)",
                "    plt.tight_layout(); plt.show(); return fig",
                "",
                "def plot_feature_importance(names, importances, top_n=10):",
                "    idx = np.argsort(importances)[::-1][:top_n]",
                "    fig, ax = plt.subplots(figsize=(8, 4))",
                "    ax.barh([names[i] for i in idx[::-1]], importances[idx[::-1]], color='#2563eb')",
                "    ax.set_title(f'Top {top_n} Feature Importances')",
                "    plt.tight_layout(); plt.show(); return fig",
            ]
        elif task_type == "regression":
            lines += [
                "def plot_predictions(y_true, y_pred, title='Predicted vs Actual'):",
                "    fig, ax = plt.subplots(figsize=(7, 6))",
                "    ax.scatter(y_true, y_pred, alpha=0.4, color='#2563eb', edgecolors='none')",
                "    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]",
                "    ax.plot(lims, lims, 'r--', linewidth=1.5)",
                "    ax.set_xlabel('Actual'); ax.set_ylabel('Predicted'); ax.set_title(title)",
                "    plt.tight_layout(); plt.show(); return fig",
                "",
                "def plot_residuals(y_true, y_pred):",
                "    residuals = y_pred - y_true",
                "    fig, axes = plt.subplots(1, 2, figsize=(12, 4))",
                "    axes[0].scatter(y_pred, residuals, alpha=0.4, color='#2563eb', edgecolors='none')",
                "    axes[0].axhline(0, color='red', linestyle='--')",
                "    axes[0].set_title('Residuals vs Predicted')",
                "    axes[1].hist(residuals, bins=30, color='#2563eb', edgecolor='white')",
                "    axes[1].set_title('Residual Distribution')",
                "    plt.tight_layout(); plt.show(); return fig",
            ]
        else:
            lines += [
                "def plot_training_history(history):",
                "    fig, axes = plt.subplots(1, 2, figsize=(12, 4))",
                "    axes[0].plot(history.history['loss'], label='Train Loss')",
                "    if 'val_loss' in history.history:",
                "        axes[0].plot(history.history['val_loss'], label='Val Loss')",
                "    axes[0].set_title('Loss'); axes[0].legend()",
                "    if 'accuracy' in history.history:",
                "        axes[1].plot(history.history['accuracy'], label='Train Acc')",
                "        if 'val_accuracy' in history.history:",
                "            axes[1].plot(history.history['val_accuracy'], label='Val Acc')",
                "        axes[1].set_title('Accuracy'); axes[1].legend()",
                "    plt.tight_layout(); plt.show(); return fig",
            ]
        return "\n".join(lines)
