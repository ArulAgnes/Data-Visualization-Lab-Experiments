"""Simple linear regression:  y_hat = b0 + b1 * x

Two independent implementations are used for comparison:

* ``sklearn.linear_model.LinearRegression`` (machine-learning style API)
* ``scipy.stats.linregress`` (statistical API)

A train/test split is used whenever the dataset is large enough so that
evaluation metrics are honest out-of-sample estimates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

MIN_ROWS_FOR_SPLIT = 30
DEFAULT_TEST_SIZE = 0.25
DEFAULT_RANDOM_STATE = 42


def compute_metrics(y_true, y_pred) -> dict:
    """MAE / MSE / RMSE / R^2 between observations and predictions."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    return {
        "n": int(y_true.size),
        "MAE": mae,
        "MSE": mse,
        "RMSE": float(np.sqrt(mse)),
        "R2": float(r2_score(y_true, y_pred)),
    }


def fit_simple_regression(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> dict:
    """Fit ``y ~ x`` on training data and evaluate on the held-out test data.

    Returns a dictionary with the fitted model, the split data, the metrics
    and the full-data statistical comparison (scipy).
    """
    if x_col not in df.columns or y_col not in df.columns:
        raise KeyError(f"Columns '{x_col}' / '{y_col}' not present in the dataframe.")
    data = df[[x_col, y_col]].dropna()
    if len(data) < 5:
        raise ValueError(
            f"Only {len(data)} complete observations - too few for a train/test regression."
        )
    X = data[[x_col]].to_numpy(dtype=float)
    y = data[y_col].to_numpy(dtype=float)

    use_split = len(data) >= MIN_ROWS_FOR_SPLIT
    if use_split:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        split_note = (
            f"train/test split ({int((1 - test_size) * 100)}/{int(test_size * 100)}), "
            f"random_state={random_state}"
        )
    else:
        X_train, X_test, y_train, y_test = X, X, y, y
        split_note = (
            f"dataset too small (n={len(data)} < {MIN_ROWS_FOR_SPLIT}): "
            "no hold-out set, metrics are in-sample demonstration values only"
        )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred_test = model.predict(X_test)
    y_pred_all = model.predict(X)

    # independent statistical fit on all complete rows
    linreg = stats.linregress(data[x_col].to_numpy(dtype=float), data[y_col].to_numpy(dtype=float))

    return {
        "x_col": x_col,
        "y_col": y_col,
        "n_total": int(len(data)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "used_split": use_split,
        "split_note": split_note,
        "model": model,
        "intercept": float(model.intercept_),
        "slope": float(model.coef_[0]),
        "equation": (
            f"{y_col} = {model.intercept_:.4f} + {model.coef_[0]:.4f} * {x_col}"
        ),
        "pearson_r": float(stats.pearsonr(data[x_col], data[y_col]).statistic),
        "r_squared_train": float(model.score(X_train, y_train)),
        "scipy_slope": float(linreg.slope),
        "scipy_intercept": float(linreg.intercept),
        "scipy_rvalue": float(linreg.rvalue),
        "scipy_pvalue": float(linreg.pvalue),
        "scipy_stderr": float(linreg.stderr),
        "metrics_test": compute_metrics(y_test, y_pred_test),
        "metrics_full": compute_metrics(y, y_pred_all),
        "data": data.reset_index(drop=True),
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "y_pred_test": y_pred_test,
        "y_pred_full": y_pred_all,
        "residuals_full": y - y_pred_all,
        "residuals_test": y_test - y_pred_test,
    }


def predict_for(result: dict, x_value: float) -> dict:
    """Single prediction at ``x_value`` (with a range guard against extrapolation)."""
    data = result["data"]
    x_min, x_max = float(data[result["x_col"]].min()), float(data[result["x_col"]].max())
    model: LinearRegression = result["model"]
    y_hat = float(model.predict(np.array([[float(x_value)]], dtype=float))[0])
    return {
        "input_variable": result["x_col"],
        "input_value": float(x_value),
        "predicted_variable": result["y_col"],
        "predicted_value": y_hat,
        "data_min": x_min,
        "data_max": x_max,
        "within_observed_range": bool(x_min <= x_value <= x_max),
        "equation": result["equation"],
    }


def metrics_payload(result: dict) -> dict:
    """JSON-serialisable summary of a regression run (saved as report)."""
    return {
        "model": "simple linear regression (sklearn LinearRegression)",
        "predictor": result["x_col"],
        "target": result["y_col"],
        "equation": result["equation"],
        "n_total": result["n_total"],
        "n_train": result["n_train"],
        "n_test": result["n_test"],
        "split": result["split_note"],
        "intercept_b0": round(result["intercept"], 6),
        "slope_b1": round(result["slope"], 6),
        "pearson_r": round(result["pearson_r"], 6),
        "r_squared_from_r": round(result["pearson_r"] ** 2, 6),
        "scipy_linregress": {
            "slope": round(result["scipy_slope"], 6),
            "intercept": round(result["scipy_intercept"], 6),
            "r_value": round(result["scipy_rvalue"], 6),
            "p_value": result["scipy_pvalue"],
            "standard_error_of_slope": round(result["scipy_stderr"], 6),
        },
        "test_metrics": {k: (round(v, 6) if isinstance(v, float) else v) for k, v in result["metrics_test"].items()},
        "full_data_metrics": {k: (round(v, 6) if isinstance(v, float) else v) for k, v in result["metrics_full"].items()},
        "residual_summary": {
            "mean": round(float(np.mean(result["residuals_full"])), 6),
            "std": round(float(np.std(result["residuals_full"], ddof=1)), 6),
            "min": round(float(np.min(result["residuals_full"])), 6),
            "max": round(float(np.max(result["residuals_full"])), 6),
        },
    }


def save_metrics(payload: dict, path: str | Path) -> Path:
    """Write the regression metrics JSON report (overwrites on re-run)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False, default=str)
    return path
