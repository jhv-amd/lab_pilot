"""Generator for time series labs."""

from typing import Any, Dict, List

from generators.base_generator import BaseLabGenerator


class TimeSeriesGenerator(BaseLabGenerator):

    @property
    def task_type(self) -> str:
        return "regression"

    def get_exercises(self) -> List[Dict[str, Any]]:
        return [
            self._exploration_exercise(),
            self._preprocessing_exercise(),
            self._feature_engineering_exercise(),
            self._model_training_exercise(),
            self._forecasting_evaluation_exercise(),
        ]

    def _exploration_exercise(self) -> Dict:
        return {
            "title": "Exercise 1: Time Series Exploration",
            "function_name": "explore_series",
            "points": 10,
            "instructions": (
                "Analyze the time series.\n\n"
                "**Returns:** dict with `n_points`, `mean`, `std`, `trend` ('up'/'down'/'flat')"
            ),
            "starter_code": (
                "def explore_series(df, value_col='value'):\n"
                "    \"\"\"Analyze time series. Returns dict with n_points, mean, std, trend.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    result = {}\n"
                "    ### END CODE HERE ###\n"
                "    return result"
            ),
            "solution_code": (
                "def explore_series(df, value_col='value'):\n"
                "    series = df[value_col]\n"
                "    slope = np.polyfit(range(len(series)), series, 1)[0]\n"
                "    trend = 'up' if slope > 0.01 else ('down' if slope < -0.01 else 'flat')\n"
                "    return {'n_points': len(series), 'mean': float(series.mean()),\n"
                "            'std': float(series.std()), 'trend': trend}"
            ),
            "public_tests": [
                "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
                "result = func(df)\n"
                "assert isinstance(result, dict)\n"
                "assert result['n_points'] == len(df)\n"
                "assert result['trend'] in ('up', 'down', 'flat')"
            ],
            "hidden_tests": ["assert abs(result['mean'] - df[df.columns[-1]].mean()) < 1"],
            "hints": ["Hint: Use np.polyfit to detect trend direction"],
        }

    def _preprocessing_exercise(self) -> Dict:
        return {
            "title": "Exercise 2: Time Series Preprocessing",
            "function_name": "preprocess_series",
            "points": 20,
            "instructions": (
                "Prepare the time series for supervised learning.\n\n"
                "**Requirements:**\n"
                "- Scale values to [0, 1] using MinMaxScaler\n"
                "- Create sliding window sequences of length `window_size`\n"
                "- Return `(X, y)` where each X[i] is a window and y[i] is the next value"
            ),
            "starter_code": (
                "def preprocess_series(series, window_size=10):\n"
                "    \"\"\"\n"
                "    Create windowed sequences for time series prediction.\n"
                "    Returns: (X, y) arrays\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    X, y = None, None\n"
                "    ### END CODE HERE ###\n"
                "    return X, y"
            ),
            "solution_code": (
                "def preprocess_series(series, window_size=10):\n"
                "    from sklearn.preprocessing import MinMaxScaler\n"
                "    scaler = MinMaxScaler()\n"
                "    values = scaler.fit_transform(series.values.reshape(-1, 1)).flatten()\n"
                "    X, y = [], []\n"
                "    for i in range(len(values) - window_size):\n"
                "        X.append(values[i:i+window_size])\n"
                "        y.append(values[i+window_size])\n"
                "    return np.array(X), np.array(y)"
            ),
            "public_tests": [
                "series = pd.Series(range(100, dtype=float))\n"
                "X, y = func(series, window_size=10)\n"
                "assert X.shape == (90, 10), f'Expected (90,10), got {X.shape}'\n"
                "assert len(y) == 90"
            ],
            "hidden_tests": [
                "assert X.max() <= 1.0, 'Values must be scaled to [0,1]'\n"
                "assert X.min() >= 0.0"
            ],
            "hints": ["Hint: Use a loop to create overlapping windows of length window_size"],
        }

    def _feature_engineering_exercise(self) -> Dict:
        return {
            "title": "Exercise 3: Feature Engineering",
            "function_name": "add_time_features",
            "points": 20,
            "instructions": (
                "Add time-based features to improve predictions.\n\n"
                "**Requirements:** Add `day_of_week`, `month`, `is_weekend` columns. Return augmented DataFrame."
            ),
            "starter_code": (
                "def add_time_features(df, date_col='date'):\n"
                "    \"\"\"\n"
                "    Add time-based features.\n"
                "    Returns: DataFrame with day_of_week, month, is_weekend added\n"
                "    \"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    df_new = df.copy()\n"
                "    ### END CODE HERE ###\n"
                "    return df_new"
            ),
            "solution_code": (
                "def add_time_features(df, date_col='date'):\n"
                "    df_new = df.copy()\n"
                "    dates = pd.to_datetime(df_new[date_col])\n"
                "    df_new['day_of_week'] = dates.dt.dayofweek\n"
                "    df_new['month'] = dates.dt.month\n"
                "    df_new['is_weekend'] = (dates.dt.dayofweek >= 5).astype(int)\n"
                "    return df_new"
            ),
            "public_tests": [
                "df = pd.read_csv(DATA_DIR / 'train.csv')\n"
                "result = func(df)\n"
                "assert 'day_of_week' in result.columns\n"
                "assert 'month' in result.columns\n"
                "assert 'is_weekend' in result.columns"
            ],
            "hidden_tests": [
                "assert result['day_of_week'].between(0, 6).all()\n"
                "assert result['month'].between(1, 12).all()"
            ],
            "hints": ["Hint: Use pd.to_datetime() and .dt.dayofweek"],
        }

    def _model_training_exercise(self) -> Dict:
        return {
            "title": "Exercise 4: Forecasting Model",
            "function_name": "train_forecaster",
            "points": 30,
            "instructions": "Train a model to forecast future values. Returns fitted model with predict().",
            "starter_code": (
                "def train_forecaster(X_train, y_train):\n"
                "    \"\"\"Train a forecasting model. Returns fitted model.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    model = None\n"
                "    ### END CODE HERE ###\n"
                "    return model"
            ),
            "solution_code": (
                "def train_forecaster(X_train, y_train):\n"
                "    from sklearn.ensemble import GradientBoostingRegressor\n"
                "    model = GradientBoostingRegressor(n_estimators=100, random_state=42)\n"
                "    model.fit(X_train, y_train)\n"
                "    return model"
            ),
            "public_tests": [
                "X = np.random.rand(100, 10)\n"
                "y = np.random.rand(100)\n"
                "model = func(X, y)\n"
                "assert model is not None\n"
                "assert hasattr(model, 'predict')"
            ],
            "hidden_tests": [
                "from sklearn.metrics import r2_score\n"
                "preds = model.predict(X_test)\n"
                "r2 = r2_score(y_test, preds)\n"
                "assert r2 >= 0.3, f'R² {r2:.3f} too low for forecasting'"
            ],
            "hints": ["Hint: Try GradientBoostingRegressor or RandomForestRegressor"],
        }

    def _forecasting_evaluation_exercise(self) -> Dict:
        return {
            "title": "Exercise 5: Forecast Evaluation",
            "function_name": "evaluate_forecast",
            "points": 20,
            "instructions": "Evaluate forecasting accuracy. Return dict with `rmse`, `mae`, `mape`.",
            "starter_code": (
                "def evaluate_forecast(y_true, y_pred):\n"
                "    \"\"\"Returns dict with rmse, mae, mape.\"\"\"\n"
                "    ### START CODE HERE ###\n"
                "    metrics = {}\n"
                "    ### END CODE HERE ###\n"
                "    return metrics"
            ),
            "solution_code": (
                "def evaluate_forecast(y_true, y_pred):\n"
                "    from sklearn.metrics import mean_squared_error, mean_absolute_error\n"
                "    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))\n"
                "    mae = float(mean_absolute_error(y_true, y_pred))\n"
                "    mape = float(np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + 1e-9))) * 100)\n"
                "    return {'rmse': rmse, 'mae': mae, 'mape': mape}"
            ),
            "public_tests": [
                "y_true = np.array([1.0, 2.0, 3.0, 4.0])\n"
                "y_pred = np.array([1.1, 2.1, 2.9, 4.2])\n"
                "result = func(y_true, y_pred)\n"
                "assert set(result.keys()) >= {'rmse', 'mae', 'mape'}\n"
                "assert result['rmse'] >= 0"
            ],
            "hidden_tests": ["assert result['mae'] >= 0\nassert result['mape'] >= 0"],
            "hints": ["Hint: MAPE = mean(|actual - predicted| / |actual|) * 100"],
        }

    def get_imports(self) -> List[str]:
        return [
            "import pandas as pd",
            "import numpy as np",
            "import matplotlib.pyplot as plt",
            "from sklearn.preprocessing import MinMaxScaler",
            "from sklearn.model_selection import train_test_split",
            "from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor",
            "from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score",
        ]

    def get_description(self) -> str:
        return (
            f"Build a time series forecasting model for **{self.topic}**. "
            f"You will analyze temporal patterns, engineer features, and train a forecaster."
        )

    def get_learning_objectives(self) -> List[str]:
        return [
            "Visualize and understand time series patterns (trend, seasonality)",
            "Create sliding-window features for supervised forecasting",
            "Engineer calendar-based features",
            "Train and evaluate regression-based forecasters",
            "Interpret RMSE, MAE, and MAPE for forecasting",
        ]
