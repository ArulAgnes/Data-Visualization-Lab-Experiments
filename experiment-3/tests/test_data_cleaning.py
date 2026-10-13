"""Tests for the data-cleaning workflow."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from src.data_cleaning import (
    before_after_table,
    check_numeric_ranges,
    clean_dataset,
    find_constant_columns,
    find_duplicate_rows,
    missing_table,
    save_cleaned_dataset,
    save_cleaning_report,
    strip_categorical_whitespace,
)


def _toy_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["alice", " bob ", "carol", "dave", "erin"],
            "group": ["A", "B", "A", "B", "A"],
            "score": [88.0, 72.5, np.nan, 65.0, 91.0],
            "height": [170.0, 165.0, np.nan, 175.0, 158.0],
        }
    )


def test_raw_dataframe_is_not_modified():
    raw = _toy_dataset()
    snapshot = raw.copy(deep=True)
    clean_dataset(raw, source="toy")
    pd.testing.assert_frame_equal(raw, snapshot)


def test_whitespace_is_stripped():
    cleaned, changed = strip_categorical_whitespace(_toy_dataset())
    assert "name" in changed
    assert cleaned["name"].tolist()[1] == "bob"


def test_rows_missing_all_measurements_are_dropped():
    raw = _toy_dataset()
    cleaned, report = clean_dataset(raw, source="toy")
    assert len(cleaned) == len(raw) - 1  # carol has no score AND no height
    assert report["rows_removed"]["all_measurements_missing"] == 1


def test_categorical_missing_filled_and_numerical_left_missing():
    raw = _toy_dataset().assign(group=["A", None, "A", "B", "A"])
    cleaned, report = clean_dataset(raw, source="toy")
    assert cleaned["group"].isna().sum() == 0
    assert (cleaned["group"] == "Unknown").sum() == 1
    # numerical missing values are never silently imputed
    assert int(cleaned["score"].isna().sum()) == 0  # the only NaN row was dropped
    assert "Numerical missing values were left untouched" in " ".join(report["decisions"])


def test_duplicates_are_removed():
    raw = pd.concat([_toy_dataset(), _toy_dataset().head(2)], ignore_index=True)
    cleaned, report = clean_dataset(
        raw, measurement_columns=["score", "height"], source="toy"
    )
    assert report["rows_removed"]["duplicates"] == 2
    assert find_duplicate_rows(cleaned).empty


def test_constant_columns_detected():
    df = _toy_dataset().assign(flag=[1, 1, 1, 1, 1])
    assert find_constant_columns(df) == ["flag"]


def test_out_of_range_values_are_flagged_but_kept():
    raw = _toy_dataset()
    cleaned, report = clean_dataset(
        raw,
        measurement_columns=["score", "height"],
        valid_ranges={"score": (0, 100)},
        positive_columns=["height"],
        source="toy",
    )
    assert report["flagged_values"]["out_of_range"] == {}
    # only the documented 'all measurements missing' row disappears - the
    # in-range values are never deleted
    assert len(cleaned) == len(raw) - 1



def test_impossible_value_is_reported():
    raw = _toy_dataset()
    raw.loc[0, "score"] = 500  # impossible percentage
    _cleaned, report = clean_dataset(
        raw, measurement_columns=["score", "height"], valid_ranges={"score": (0, 100)}, source="toy"
    )
    assert report["flagged_values"]["out_of_range"]["score"]["count"] == 1


def test_report_structure_and_json_roundtrip(tmp_path):
    _cleaned, report = clean_dataset(_toy_dataset(), source="toy")
    for key in ("raw_profile", "cleaned_profile", "checks", "actions", "before_after", "decisions"):
        assert key in report
    path = save_cleaning_report(report, tmp_path / "report.json")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["raw_profile"]["rows"] == 5


def test_cleaned_dataset_saved(tmp_path):
    cleaned, _report = clean_dataset(_toy_dataset(), source="toy")
    path = save_cleaned_dataset(cleaned, tmp_path / "cleaned.csv")
    again = pd.read_csv(path)
    assert len(again) == len(cleaned)


def test_before_after_table_shape():
    raw = _toy_dataset()
    table = before_after_table(raw, raw.head(3))
    metrics = {row["metric"] for row in table}
    assert {"row_count", "missing_values", "duplicate_rows"} <= metrics


def test_missing_table_counts():
    table = missing_table(_toy_dataset())
    assert int(table.loc["score", "missing_count"]) == 1


def test_check_numeric_ranges_non_positive():
    df = pd.DataFrame({"a": [1.0, -2.0, 3.0]})
    findings = check_numeric_ranges(df, positive_columns=["a"])
    assert findings["non_positive"]["a"] == 1


def test_clean_dataset_on_real_data(raw_dataset):
    """The cleaning decisions reported for the real dataset must hold."""
    cleaned, report = clean_dataset(raw_dataset, source="penguins")
    assert len(cleaned) <= len(raw_dataset)
    assert report["rows_removed"]["duplicates"] == 0  # penguins has no duplicates
    assert report["rows_removed"]["all_measurements_missing"] == 2
    assert cleaned["sex"].isna().sum() == 0
    # the 2 dropped rows carried the only numerical gaps; the 9 remaining
    # sex gaps were filled with 'Unknown' -> no missing value is left
    assert int(cleaned.isna().sum().sum()) == 0
    assert report["cleaned_profile"]["missing_total"] == 0
