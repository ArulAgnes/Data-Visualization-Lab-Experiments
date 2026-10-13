"""Tests for the five synthetic distributions and dataset summaries."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.distribution_analysis import (
    dataset_distribution_summary,
    describe_shape,
    make_bimodal,
    make_gaussian,
    make_left_skewed,
    make_right_skewed,
    make_uniform,
    normal_reference_curve,
    summarise,
)


@pytest.mark.parametrize(
    "factory, expected_sign",
    [
        (make_gaussian, "near_zero"),
        (make_uniform, "near_zero"),
        (make_right_skewed, "positive"),
        (make_left_skewed, "negative"),
    ],
)
def test_generators_reproduce_expected_skew(factory, expected_sign):
    values = factory(seed=42)
    skew = summarise(values)["skewness"]
    if expected_sign == "positive":
        assert skew > 1.0
    elif expected_sign == "negative":
        assert skew < -1.0
    else:
        assert abs(skew) < 0.2


def test_seed_reproducibility():
    assert np.allclose(make_gaussian(seed=42), make_gaussian(seed=42))
    assert not np.allclose(make_gaussian(seed=42), make_gaussian(seed=43))


def test_bimodal_has_two_clear_peaks():
    values, labels = make_bimodal(seed=42)
    assert set(np.unique(labels)) == {"group_A", "group_B"}
    mean_a = values[labels == "group_A"].mean()
    mean_b = values[labels == "group_B"].mean()
    assert mean_b - mean_a > 20
    # a mixture of two well separated groups has two local maxima
    density, edges = np.histogram(values, bins=50, density=True)
    peaks = np.sum((density[1:-1] > density[:-2]) & (density[1:-1] > density[2:]))
    assert peaks >= 2


def test_normal_reference_curve_is_a_density():
    x, y = normal_reference_curve(make_gaussian(seed=1))
    area = float(np.trapezoid(y, x)) if hasattr(np, "trapezoid") else float(np.trapz(y, x))
    assert np.isclose(area, 1.0, atol=0.01)


def test_dataset_summary_labels_shapes(raw_dataset):
    summary = dataset_distribution_summary(raw_dataset)
    assert set(summary["variable"]) >= {"bill_length_mm", "body_mass_g"}
    assert (summary["shape"] == "approximately symmetric").all()


def test_describe_shape_rules():
    assert describe_shape(0.1) == "approximately symmetric"
    assert describe_shape(1.4) == "right-skewed (positive)"
    assert describe_shape(-1.4) == "left-skewed (negative)"


def test_summarise_drops_missing_values():
    summary = summarise(pd.Series([1.0, 2.0, np.nan, 4.0]))
    assert summary["n"] == 3
