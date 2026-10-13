"""Tests for the linear-regression module."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest
from scipy import stats

from src.regression_analysis import (
    compute_metrics,
    fit_simple_regression,
    metrics_payload,
    predict_for,
    save_metrics,
)


def test_perfect_line_recovers_coefficients():
    x = np.arange(0, 20, dtype=float)
    df = pd.DataFrame({"x": x, "y": 3.0 * x + 7.0})
    result = fit_simple_regression(df, "x", "y", test_size=0.25, random_state=0)
    assert result["intercept"] == pytest.approx(7.0, abs=1e-8)
    assert result["slope"] == pytest.approx(3.0, abs=1e-8)
    assert result["metrics_test"]["R2"] == pytest.approx(1.0, abs=1e-9)
    assert result["pearson_r"] == pytest.approx(1.0)


def test_scipy_and_sklearn_agree():
    rng = np.random.default_rng(7)
    x = rng.uniform(0, 10, 80)
    df = pd.DataFrame({"x": x, "y": 2.0 * x + 1.0 + rng.normal(0, 0.5, 80)})
    result = fit_simple_regression(df, "x", "y")
    # the sklearn model is fitted on the TRAINING split -> compare with scipy
    # on exactly the same rows
    train = stats.linregress(result["X_train"].ravel(), result["y_train"])
    assert result["slope"] == pytest.approx(train.slope, rel=1e-9)
    assert result["intercept"] == pytest.approx(train.intercept, rel=1e-9)
    # the independent scipy fit on all complete rows is very close
    assert result["scipy_slope"] == pytest.approx(result["slope"], rel=0.1)
    assert result["pearson_r"] == pytest.approx(result["scipy_rvalue"], rel=1e-9)



def test_r_squared_equals_pearson_r_squared_on_training_data():
    rng = np.random.default_rng(3)
    df = pd.DataFrame({"x": rng.normal(size=60), "y": rng.normal(size=60)})
    result = fit_simple_regression(df, "x", "y")
    from scipy import stats

    r_train = stats.pearsonr(result["X_train"].ravel(), result["y_train"]).statistic
    # for simple OLS with an intercept, R^2 = r^2 on the fitted data
    assert result["r_squared_train"] == pytest.approx(float(r_train) ** 2, abs=1e-9)


def test_metrics_are_finite():
    metrics = compute_metrics([1.0, 2.0, 3.0], [1.1, 2.2, 2.9])
    for value in metrics.values():
        assert np.isfinite(value)


def test_small_dataset_falls_back_to_in_sample():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], "y": [2.0, 4.0, 5.0, 4.0, 5.0, 7.0]})
    result = fit_simple_regression(df, "x", "y")
    assert result["used_split"] is False
    assert "no hold-out set" in result["split_note"]


def test_predict_for_flags_extrapolation():
    df = pd.DataFrame({"x": np.arange(0, 10, dtype=float), "y": np.arange(0, 10, dtype=float) * 2})
    result = fit_simple_regression(df, "x", "y")
    inside = predict_for(result, 5.0)
    outside = predict_for(result, 500.0)
    assert inside["within_observed_range"] is True
    assert outside["within_observed_range"] is False
    assert outside["predicted_value"] == pytest.approx(1000.0, rel=1e-6)


def test_metrics_payload_is_json_serialisable(tmp_path):
    df = pd.DataFrame({"x": np.arange(0, 40, dtype=float), "y": np.arange(0, 40, dtype=float) * 2 + 1})
    payload = metrics_payload(fit_simple_regression(df, "x", "y"))
    path = save_metrics(payload, tmp_path / "metrics.json")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["predictor"] == "x"
    assert np.isfinite(loaded["test_metrics"]["RMSE"])


def test_missing_column_raises(raw_dataset):
    with pytest.raises(KeyError):
        fit_simple_regression(raw_dataset, "not_a_column", "body_mass_g")


def test_too_few_rows_raises():
    df = pd.DataFrame({"x": [1.0, 2.0], "y": [1.0, 2.0]})
    with pytest.raises(ValueError):
        fit_simple_regression(df, "x", "y")


def test_real_dataset_regression_is_sensible(raw_dataset):
    """flipper length should predict body mass with a solid positive slope."""
    result = fit_simple_regression(raw_dataset, "flipper_length_mm", "body_mass_g")
    assert result["slope"] > 0
    assert result["metrics_test"]["R2"] > 0.5
    assert result["used_split"] is True
    for value in result["metrics_test"].values():
        assert np.isfinite(value)
