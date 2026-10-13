"""Tests for dataset loading and path handling."""

from __future__ import annotations

import pandas as pd
import pytest

from src.data_loader import (
    find_project_root,
    initial_inspection,
    list_columns,
    load_dataset,
    missing_report,
    resolve_dataset_path,
)


def test_project_root_is_detected(project_root):
    assert (project_root / "src").is_dir()
    assert find_project_root(project_root / "src") == project_root


def test_real_dataset_loads(raw_dataset):
    assert raw_dataset.shape == (344, 8)
    assert "body_mass_g" in raw_dataset.columns


def test_missing_dataset_raises_helpful_error(project_root, tmp_path):
    with pytest.raises(FileNotFoundError) as excinfo:
        resolve_dataset_path("does/not/exist.csv", root=project_root, allow_upload=False)
    assert "Dataset not found" in str(excinfo.value)


def test_empty_dataset_raises_value_error(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_text("a,b,c\n", encoding="utf-8")  # header only, no rows
    with pytest.raises(ValueError) as excinfo:
        load_dataset(empty, allow_upload=False)
    assert "0 data rows" in str(excinfo.value)


def test_columnless_file_raises_value_error(tmp_path):
    blank = tmp_path / "blank.csv"
    blank.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        load_dataset(blank, allow_upload=False)


def test_list_columns(raw_dataset):
    cols = list_columns(raw_dataset)
    assert "body_mass_g" in cols["numerical"]
    assert "species" in cols["categorical"]


def test_missing_report_matches_pandas(raw_dataset):
    report = missing_report(raw_dataset)
    assert int(report.loc["sex", "missing_count"]) == int(raw_dataset["sex"].isna().sum())


def test_initial_inspection(raw_dataset):
    info = initial_inspection(raw_dataset)
    assert info["shape"] == (344, 8)
    assert info["duplicate_rows"] == 0
    assert info["missing_total"] == int(raw_dataset.isna().sum().sum())


def test_invalid_path_does_not_silently_use_another_file(project_root):
    """A wrong path must fail instead of quietly loading an unrelated CSV."""
    with pytest.raises(FileNotFoundError):
        resolve_dataset_path("data/raw/this_file_does_not_exist.csv", root=project_root)
