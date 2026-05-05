"""Download and prepare datasets for generated labs."""

import csv
import random
import string
from pathlib import Path
from typing import Dict, Any

import numpy as np
import yaml


DATASETS_DIR = Path(__file__).parent.parent / "datasets"


def _load_dataset_config(dataset_name: str) -> Dict[str, Any]:
    for yaml_file in DATASETS_DIR.glob("*.yaml"):
        with open(yaml_file) as f:
            cfg = yaml.safe_load(f) or {}
        if dataset_name in cfg:
            return cfg[dataset_name]
    return {}


class DatasetManager:
    """Generate or download datasets for lab kits."""

    @staticmethod
    def prepare_dataset(dataset_name: str, output_dir: str | Path) -> Dict[str, Any]:
        """
        Prepare the dataset and write train.csv / test.csv to output_dir/data/.
        Returns metadata dict describing the dataset.
        """
        output_dir = Path(output_dir)
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        cfg = _load_dataset_config(dataset_name)
        if not cfg:
            cfg = {"name": dataset_name, "type": "tabular", "n_samples": 500, "source": "synthetic"}

        source = cfg.get("source", "synthetic")
        ds_type = cfg.get("type", "tabular")

        if source == "sklearn" and dataset_name == "iris":
            return DatasetManager._prepare_iris(data_dir, cfg)
        elif source == "sklearn" and dataset_name == "diabetes":
            return DatasetManager._prepare_diabetes(data_dir, cfg)
        elif ds_type == "tabular":
            return DatasetManager._prepare_tabular_synthetic(dataset_name, cfg, data_dir)
        elif ds_type == "text":
            return DatasetManager._prepare_text_synthetic(dataset_name, cfg, data_dir)
        elif ds_type == "timeseries":
            return DatasetManager._prepare_timeseries_synthetic(dataset_name, cfg, data_dir)
        else:
            return DatasetManager._prepare_tabular_synthetic(dataset_name, cfg, data_dir)

    @staticmethod
    def _prepare_iris(data_dir: Path, cfg: dict) -> dict:
        from sklearn.datasets import load_iris
        from sklearn.model_selection import train_test_split
        import pandas as pd

        data = load_iris(as_frame=True)
        df = data.frame
        df["species"] = data.target_names[df["target"]]
        df = df.drop(columns=["target"])
        train, test = train_test_split(df, test_size=0.2, random_state=42)
        train.to_csv(data_dir / "train.csv", index=False)
        test.to_csv(data_dir / "test.csv", index=False)
        (data_dir / "README.md").write_text(
            "# Iris Dataset\n\nClassic multiclass classification dataset.\nTarget: `species`\n"
        )
        return {"train_path": "data/train.csv", "test_path": "data/test.csv",
                "description": cfg.get("description", "Iris"), "target": "species"}

    @staticmethod
    def _prepare_diabetes(data_dir: Path, cfg: dict) -> dict:
        from sklearn.datasets import load_diabetes
        from sklearn.model_selection import train_test_split
        import pandas as pd

        data = load_diabetes(as_frame=True)
        df = data.frame
        df["outcome"] = (df["target"] > df["target"].median()).astype(int)
        df = df.drop(columns=["target"])
        train, test = train_test_split(df, test_size=0.2, random_state=42)
        train.to_csv(data_dir / "train.csv", index=False)
        test.to_csv(data_dir / "test.csv", index=False)
        (data_dir / "README.md").write_text("# Diabetes Dataset\nTarget: `outcome`\n")
        return {"train_path": "data/train.csv", "test_path": "data/test.csv",
                "description": cfg.get("description", "Diabetes"), "target": "outcome"}

    @staticmethod
    def _prepare_tabular_synthetic(dataset_name: str, cfg: dict, data_dir: Path) -> dict:
        rng = np.random.default_rng(42)
        n = cfg.get("n_samples", 800)
        features = cfg.get("features", [])
        target = cfg.get("target", "label")
        id_col = cfg.get("id_column", None)
        task = cfg.get("task", "classification")
        missing_rate = cfg.get("missing_rate", 0.0)

        rows = []
        for i in range(n):
            row = {}
            if id_col:
                row[id_col] = f"ID{i:04d}"
            for feat in features:
                fname = feat["name"]
                ftype = feat.get("type", "float")
                if ftype == "categorical":
                    row[fname] = rng.choice(feat.get("values", ["a", "b", "c"]))
                elif ftype == "int":
                    lo, hi = feat.get("range", [0, 100])
                    row[fname] = int(rng.integers(lo, hi))
                else:
                    lo, hi = feat.get("range", [0.0, 1.0])
                    row[fname] = round(float(rng.uniform(lo, hi)), 3)
            if task == "classification":
                numeric_vals = [v for k, v in row.items() if isinstance(v, (int, float)) and k != id_col]
                logit = -1.0 + sum(0.2 * (v - np.mean(numeric_vals)) / (np.std(numeric_vals) + 1e-9) for v in numeric_vals[:3])
                prob = 1 / (1 + np.exp(-logit))
                row[target] = int(rng.uniform() < prob)
            else:
                numeric_vals = [v for k, v in row.items() if isinstance(v, (int, float)) and k != id_col]
                row[target] = round(float(sum(100 * v for v in numeric_vals[:3]) + rng.normal(0, 500)), 2)
            rows.append(row)

        # Inject missing values
        if missing_rate > 0:
            numeric_keys = [k for k, v in rows[0].items() if isinstance(v, float)]
            for row in rows:
                for k in numeric_keys:
                    if rng.uniform() < missing_rate:
                        row[k] = None

        # Split and write
        split = int(0.8 * n)
        fieldnames = list(rows[0].keys())
        for fname, subset in [("train.csv", rows[:split]), ("test.csv", rows[split:])]:
            with open(data_dir / fname, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(subset)

        readme = f"# {cfg.get('name', dataset_name)}\n\n{cfg.get('description', '')}\n\nTarget: `{target}`\n"
        (data_dir / "README.md").write_text(readme)

        return {"train_path": "data/train.csv", "test_path": "data/test.csv",
                "description": cfg.get("description", ""), "target": target}

    @staticmethod
    def _prepare_text_synthetic(dataset_name: str, cfg: dict, data_dir: Path) -> dict:
        import csv as csv_mod
        rng = np.random.default_rng(42)
        n = cfg.get("n_samples", 600)
        classes = cfg.get("classes", ["positive", "negative"])
        target = cfg.get("target", "label")

        positive_words = ["great", "excellent", "wonderful", "amazing", "good", "love", "best", "fantastic"]
        negative_words = ["terrible", "awful", "bad", "worst", "hate", "poor", "disappointing", "boring"]
        neutral_words = ["the", "a", "is", "this", "very", "quite", "just", "really", "movie", "product"]

        rows = []
        for i in range(n):
            label = classes[i % len(classes)]
            if "positive" in label or "ham" in label or label == classes[0]:
                words = rng.choice(positive_words, 5).tolist() + rng.choice(neutral_words, 8).tolist()
            else:
                words = rng.choice(negative_words, 5).tolist() + rng.choice(neutral_words, 8).tolist()
            rng.shuffle(words)
            rows.append({"text": " ".join(words), target: label})

        split = int(0.8 * n)
        for fname, subset in [("train.csv", rows[:split]), ("test.csv", rows[split:])]:
            with open(data_dir / fname, "w", newline="", encoding="utf-8") as f:
                writer = csv_mod.DictWriter(f, fieldnames=["text", target])
                writer.writeheader()
                writer.writerows(subset)

        (data_dir / "README.md").write_text(f"# {dataset_name}\nText classification dataset.\nTarget: `{target}`\n")
        return {"train_path": "data/train.csv", "test_path": "data/test.csv", "target": target}

    @staticmethod
    def _prepare_timeseries_synthetic(dataset_name: str, cfg: dict, data_dir: Path) -> dict:
        import csv as csv_mod
        from datetime import date, timedelta
        rng = np.random.default_rng(42)
        n = cfg.get("n_points", 1000)
        target = cfg.get("target", "value")

        start = date(2020, 1, 1)
        rows = []
        for i in range(n):
            trend = 0.05 * i
            seasonality = 10 * np.sin(2 * np.pi * i / 7)
            noise = float(rng.normal(0, 2))
            value = round(50 + trend + seasonality + noise, 3)
            rows.append({"date": (start + timedelta(days=i)).isoformat(), target: value})

        split = int(0.8 * n)
        for fname, subset in [("train.csv", rows[:split]), ("test.csv", rows[split:])]:
            with open(data_dir / fname, "w", newline="") as f:
                writer = csv_mod.DictWriter(f, fieldnames=["date", target])
                writer.writeheader()
                writer.writerows(subset)

        (data_dir / "README.md").write_text(f"# {dataset_name}\nTime series dataset.\nTarget: `{target}`\n")
        return {"train_path": "data/train.csv", "test_path": "data/test.csv", "target": target}

    @staticmethod
    def generate_data_loading_code(dataset_name: str) -> str:
        cfg = _load_dataset_config(dataset_name)
        ds_type = cfg.get("type", "tabular")
        target = cfg.get("target", "label")

        if ds_type in ("tabular",):
            return (
                "train_df = pd.read_csv('data/train.csv')\n"
                f"print(f'Dataset loaded: {{train_df.shape[0]}} rows, {{train_df.shape[1]}} columns')\n"
                f"print(f'Target: {target}')\n"
                "train_df.head()"
            )
        elif ds_type == "text":
            return (
                "train_df = pd.read_csv('data/train.csv')\n"
                f"print(f'Text dataset: {{train_df.shape[0]}} samples')\n"
                f"print(f'Classes: {{train_df[\"{target}\"].unique()}}')\n"
                "train_df.head()"
            )
        elif ds_type == "timeseries":
            return (
                "train_df = pd.read_csv('data/train.csv', parse_dates=['date'])\n"
                f"print(f'Time series: {{len(train_df)}} time steps')\n"
                "train_df.head()"
            )
        return "# Load your data here\ndata = pd.read_csv('data/train.csv')"
