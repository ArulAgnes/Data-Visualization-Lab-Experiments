"""Tests for the IQR outlier-detection logic."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.outlier_analysis import (
    detect_outliers,
    iqr_bounds,
    print_outlier_summary,
    save_outlier_report,
    synthetic_outlier_example,
)


def test_iqr_bounds_textbook_calculation():
    # Q1 = 25, median = 50, Q3 = 75 -> IQR = 50
    series = pd.Series(np.arange(1, 101, dtype=float))
    bounds = iqr_bounds(series)
    assert bounds["q1"] == pytest.approx(25.75)
    assert bounds["q3"] == pytest.approx(75.25)
    assert bounds["iqr"] == pytest.approx(bounds["q3"] - bounds["q1"])
    assert bounds["lower_fence"] == pytest.approx(bounds["q1"] - 1.5 * bounds["iqr"])
    assert bounds["upper_fence"] == pytest.approx(bounds["q3"] + 1.5 * bounds["iqr"])


def test_known_outlier_is_detected():
    series = pd.Series([10.0, 12.0, 11.0, 13.0, 12.5, 11.5, 100.0])
    bounds = iqr_bounds(series)
    assert bounds["n_outliers"] == 1
    assert bounds["outlier_values"] == [100.0]
    assert bounds["percent_outliers"] == pytest.approx(100 / 7, abs=0.01)


def test_both_sides_are_checked():
    series = pd.Series([50.0, 51.0, 49.0, 50.5, 49.5, -500.0, 900.0])
    bounds = iqr_bounds(series)
    assert bounds["n_outliers"] == 2
    assert bounds["outlier_values"] == [-500.0, 900.0]


def test_clean_data_has_no_outliers():
    series = pd.Series(np.arange(0, 101, dtype=float))
    assert iqr_bounds(series)["n_outliers"] == 0


def test_empty_series_raises():
    with pytest.raises(ValueError):
        iqr_bounds(pd.Series([], dtype=float))


def test_detect_outliers_overall_and_grouped():
    df = pd.DataFrame(
        {
            "value": [10.0, 11.0, 12.0, 10.5, 11.5, 30.0, 200.0, 210.0, 190.0, 205.0],
            "group": ["a"] * 5 + ["b"] * 5,
        }
    )
    report, detail = detect_outliers(df, ["value"], group_col="group")
    overall = report[(report["scope"] == "overall") & (report["variable"] == "value")].iloc[0]
    # pooling the two sub-groups widens the fences so much that nothing is flagged
    assert int(overall["n_outliers"]) == 0
    per_group = report[report["scope"] == "by_group"]
    # inside group b the value 30 is far below the rest -> flagged only when grouped
    assert int(per_group[per_group["group"] == "b"]["n_outliers"].iloc[0]) == 1
    assert int(per_group[per_group["group"] == "a"]["n_outliers"].iloc[0]) == 0
    assert "overall::value" in detail


def test_report_save_roundtrip(tmp_path):
    df = pd.DataFrame({"v": [1.0, 2.0, 3.0, 2.0, 1.0, 99.0]})
    report, _ = detect_outliers(df, ["v"])
    path = save_outlier_report(report, tmp_path / "outliers.csv")
    loaded = pd.read_csv(path)
    assert list(loaded["variable"]) == ["v"]


def test_synthetic_example_contains_injected_outliers():
    series = synthetic_outlier_example()
    bounds = iqr_bounds(series)
    injected = series.attrs["known_outliers"]
    detected = set(bounds["outlier_values"])
    assert set(injected) <= detected


def test_print_outlier_summary_does_not_raise(capsys):
    df = pd.DataFrame({"v": [1.0, 2.0, 3.0, 4.0, 50.0]})
    report, _ = detect_outliers(df, ["v"])
    print_outlier_summary(report)
    assert "IQR OUTLIER DETECTION" in capsys.readouterr().out


def test_detect_outliers_on_real_dataset_reports_honestly(raw_dataset):
    """Pooled IQR finds no outliers in the penguins measurements - must be reported as such."""
    cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    report, detail = detect_outliers(raw_dataset, cols, group_col="species")
    overall = report[report["scope"] == "overall"]
    assert len(overall) == len(cols)
    assert int(overall["n_outliers"].sum()) == 0
    grouped = report[report["scope"] == "by_species"]
    assert len(grouped) == len(cols) * raw_dataset["species"].nunique()
    assert int(grouped["n_outliers"].sum()) > 0  # subgroups do reveal a few
