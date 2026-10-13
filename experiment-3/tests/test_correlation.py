"""Tests for the Pearson correlation implementations."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from scipy import stats

from src.correlation_analysis import (
    interpretation,
    pearson_all_methods,
    pearson_manual,
    pearson_matrix,
    pearson_pair,
    strength_label,
)
from src.relationship_analysis import make_demo


def test_manual_formula_matches_textbook_example():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]
    # hand-checked value for this classic example
    assert pearson_manual(x, y) == pytest.approx(0.7745966692, abs=1e-9)


def test_all_methods_agree():
    x = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
    y = np.array([1.0, 3.5, 5.0, 7.5, 9.0])
    results = pearson_all_methods(x, y)
    assert results["max_absolute_difference"] < 1e-12
    assert 0.99 < results["manual_formula"] < 1.0


def test_perfect_correlations():
    x = np.linspace(0, 10, 20)
    assert pearson_manual(x, 2 * x + 5) == pytest.approx(1.0)
    assert pearson_manual(x, -3 * x + 1) == pytest.approx(-1.0)


def test_correlation_is_symmetric():
    rng = np.random.default_rng(0)
    x, y = rng.normal(size=50), rng.normal(size=50)
    assert pearson_manual(x, y) == pytest.approx(pearson_manual(y, x))


def test_zero_variance_raises():
    with pytest.raises(ValueError):
        pearson_manual([1, 2, 3], [5, 5, 5])


def test_nan_values_are_dropped_pairwise():
    x = [1.0, 2.0, np.nan, 4.0, 5.0]
    y = [2.0, 4.0, 6.0, np.nan, 10.0]
    assert pearson_manual(x, y) == pytest.approx(1.0)


def test_pearson_pair_metadata():
    x = list(range(1, 21))
    y = [2 * v + 1 for v in x]
    result = pearson_pair(x, y)
    assert result["n_valid"] == 20
    assert result["direction"] == "positive"
    assert result["strength"] == "very strong"
    assert result["significant_at_alpha"] is True
    assert result["p_value"] < 0.001
    assert 0 <= result["p_value"] <= 1


def test_insufficient_sample_is_not_significant():
    result = pearson_pair([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
    assert result["p_value"] > 0.05
    assert result["significant_at_alpha"] is False


def test_pearson_pair_reports_missing_pairs():
    result = pearson_pair([1, 2, np.nan, 4, 5], [2, 4, 6, 8, 10])
    assert result["n_valid"] == 4
    assert result["n_missing_pairs_dropped"] == 1


def test_not_enough_observations_raises():
    with pytest.raises(ValueError):
        pearson_pair([1.0, np.nan], [2.0, np.nan])


def test_strength_labels_are_configurable():
    assert strength_label(0.9) == "very strong"
    assert strength_label(0.5) == "moderate"
    assert strength_label(0.05) == "negligible"
    assert strength_label(0.9, {"big": 0.9, "small": 0.0}) == "big"


def test_matrix_on_real_dataset(raw_dataset):
    cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    matrix = pearson_matrix(raw_dataset, cols)
    assert matrix.shape == (4, 4)
    assert np.allclose(np.diag(matrix.values), 1.0)  # diagonal
    # flipper vs mass is a strong positive relationship in the penguins data
    assert matrix.loc["flipper_length_mm", "body_mass_g"] > 0.8


def test_matrix_value_matches_manual_formula(raw_dataset):
    x = raw_dataset["flipper_length_mm"].dropna()
    y = raw_dataset.loc[x.index, "body_mass_g"].dropna()
    assert pearson_manual(x, y) == pytest.approx(float(x.corr(y)), abs=1e-12)


def test_demos_produce_expected_magnitude():
    expected = {
        "strong_positive": 0.95,
        "strong_negative": -0.95,
        "weak_positive": 0.30,
        "weak_negative": -0.30,
        "perfect_positive": 1.0,
        "perfect_negative": -1.0,
    }
    for name, target in expected.items():
        frame = make_demo(name)
        r = pearson_manual(frame["x"], frame["y"])
        assert r == pytest.approx(target, abs=0.02), f"{name}: expected r~{target}, got {r:.3f}"


def test_no_linear_demo_is_near_zero():
    r = pearson_manual(*(make_demo("no_linear")[["x", "y"]].T.to_numpy()))
    assert abs(r) < 0.3


def test_interpretation_mentions_causation_warning():
    result = pearson_pair([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
    text = interpretation(result, "x", "y")
    assert "causation" in text.lower()
