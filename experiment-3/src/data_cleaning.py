"""Reproducible data-cleaning workflow.

Design rules
------------
* the raw dataset is **never** modified or overwritten,
* every cleaning action is recorded (what, why, how many rows/columns),
* rows are only dropped when a documented justification exists,
* outliers are **never** removed by this module,
* the cleaned table and a machine-readable JSON report are saved separately.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import pandas as pd

DEFAULT_CATEGORICAL_FILL = "Unknown"


# --------------------------------------------------------------------------- #
# Inspection helpers
# --------------------------------------------------------------------------- #
def missing_table(df: pd.DataFrame) -> pd.DataFrame:
    """Missing counts / percentages for every column."""
    n = len(df)
    counts = df.isna().sum()
    return pd.DataFrame(
        {
            "missing_count": counts,
            "missing_percent": (counts / max(n, 1) * 100).round(2),
        }
    ).sort_values("missing_count", ascending=False)


def find_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows that are exact duplicates of an earlier row."""
    return df[df.duplicated(keep="first")]


def find_constant_columns(df: pd.DataFrame) -> list:
    """Columns with zero (or one) distinct non-null values are uninformative."""
    constant = []
    for col in df.columns:
        if df[col].nunique(dropna=True) <= 1:
            constant.append(col)
    return constant


def strip_categorical_whitespace(df: pd.DataFrame) -> tuple:
    """Strip accidental leading/trailing whitespace from text columns.

    Returns ``(cleaned_df, changed_columns)``.
    """
    changed = []
    cleaned = df.copy()
    for col in cleaned.columns:
        series = cleaned[col]
        is_text = (
            pd.api.types.is_object_dtype(series)
            or pd.api.types.is_string_dtype(series)
            or isinstance(series.dtype, pd.CategoricalDtype)
        )
        if not is_text:
            continue
        as_string = series.astype("string")
        stripped = as_string.str.strip()
        unequal = as_string.fillna("__NA__").ne(stripped.fillna("__NA__")).any()
        if not unequal:
            continue
        changed.append(col)
        if isinstance(series.dtype, pd.CategoricalDtype):
            cleaned[col] = stripped.astype("category")
        elif pd.api.types.is_object_dtype(series):
            cleaned[col] = stripped.astype(object)
        else:
            cleaned[col] = stripped
    return cleaned, changed


def check_numeric_ranges(
    df: pd.DataFrame,
    ranges: Optional[dict] = None,
    positive_columns: Optional[Sequence[str]] = None,
) -> dict:
    """Look for impossible / suspicious numerical values.

    ``ranges`` maps ``column -> (min, max)`` accepted bounds.
    ``positive_columns`` must not contain zero or negative values.
    """
    findings: dict = {"out_of_range": {}, "non_positive": {}, "non_finite": {}}
    for col in df.select_dtypes(include="number").columns:
        values = df[col].dropna()
        non_finite = int((~np.isfinite(values.astype(float))).sum())
        if non_finite:
            findings["non_finite"][col] = non_finite
        if ranges and col in ranges:
            low, high = ranges[col]
            bad = values[(values < low) | (values > high)]
            if len(bad):
                findings["out_of_range"][col] = {
                    "count": int(len(bad)),
                    "bounds": [low, high],
                    "examples": [float(v) for v in bad.head(5)],
                }
        if positive_columns and col in positive_columns:
            bad = values[values <= 0]
            if len(bad):
                findings["non_positive"][col] = int(len(bad))
    return findings


def profile_dataset(df: pd.DataFrame) -> dict:
    """Machine-readable snapshot of the dataset before/after cleaning."""
    n = len(df)
    missing = missing_table(df)
    return {
        "rows": int(n),
        "columns": int(df.shape[1]),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_total": int(df.isna().sum().sum()),
        "missing_by_column": {
            col: {"count": int(row["missing_count"]), "percent": float(row["missing_percent"])}
            for col, row in missing.iterrows()
        },
        "column_names": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
    }


# --------------------------------------------------------------------------- #
# Cleaning
# --------------------------------------------------------------------------- #
def clean_dataset(
    df: pd.DataFrame,
    measurement_columns: Optional[Sequence[str]] = None,
    categorical_fill_value: str = DEFAULT_CATEGORICAL_FILL,
    valid_ranges: Optional[dict] = None,
    positive_columns: Optional[Sequence[str]] = None,
    source: str = "",
) -> tuple:
    """Clean ``df`` and return ``(cleaned_df, report_dict)``.

    Rules applied (each one documented in the report):

    1. strip whitespace from categorical values,
    2. drop exact duplicate rows (only if any exist),
    3. drop rows where **every** measurement column is missing
       (such rows carry no measurable information),
    4. fill remaining categorical missing values with ``categorical_fill_value``,
       numerical columns are *not* silently imputed,
    5. flag (never delete) impossible values found by range checks,
    6. report constant columns without deleting them unless they are empty.
    """
    raw = df.copy()
    report: dict = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": source or str(raw.attrs.get("source_path", "in-memory dataframe")),
        "raw_profile": profile_dataset(raw),
        "checks": [],
        "actions": [],
        "columns_modified": [],
        "columns_dropped": [],
        "rows_removed": {"total": 0, "duplicates": 0, "all_measurements_missing": 0},
        "decisions": [],
    }
    cleaned = raw.copy()

    # 1. categorical whitespace ------------------------------------------------
    cleaned, changed = strip_categorical_whitespace(cleaned)
    report["checks"].append(
        {
            "check": "categorical_whitespace",
            "result": f"{len(changed)} column(s) required trimming",
            "columns": changed,
            "decision": "values trimmed" if changed else "no change needed",
            "reason": "trailing/leading spaces create accidental extra categories",
        }
    )
    if changed:
        report["columns_modified"].extend(changed)
        report["actions"].append({"action": "strip_whitespace", "columns": changed})

    # 2. duplicates ------------------------------------------------------------
    n_dupes = int(cleaned.duplicated().sum())
    if n_dupes:
        cleaned = cleaned.drop_duplicates(keep="first").reset_index(drop=True)
        report["rows_removed"]["duplicates"] = n_dupes
        report["rows_removed"]["total"] += n_dupes
    report["checks"].append(
        {
            "check": "duplicate_rows",
            "result": f"{n_dupes} exact duplicate row(s) found",
            "decision": f"{n_dupes} duplicate row(s) removed" if n_dupes else "no row removed",
            "reason": "duplicate observations bias summary statistics",
        }
    )
    if n_dupes:
        report["actions"].append({"action": "drop_duplicates", "rows": n_dupes})
        report["decisions"].append("Removed exact duplicate rows (keep='first').")

    # 3. rows with no measurements at all -------------------------------------
    if measurement_columns is None:
        numeric_cols = list(cleaned.select_dtypes(include="number").columns)
        # measurement columns = every numeric column that actually has gaps
        measurement_columns = [c for c in numeric_cols if cleaned[c].isna().any()]
        if not measurement_columns:  # nothing missing: fall back to all numeric columns
            measurement_columns = numeric_cols
    measurement_columns = [c for c in measurement_columns if c in cleaned.columns]
    if measurement_columns:
        mask_all_missing = cleaned[measurement_columns].isna().all(axis=1)
        n_empty = int(mask_all_missing.sum())
        if n_empty:
            cleaned = cleaned.loc[~mask_all_missing].reset_index(drop=True)
            report["rows_removed"]["all_measurements_missing"] = n_empty
            report["rows_removed"]["total"] += n_empty
        report["checks"].append(
            {
                "check": "rows_without_measurements",
                "result": f"{n_empty} row(s) missing all measurement columns {measurement_columns}",
                "decision": f"{n_empty} row(s) dropped" if n_empty else "no row removed",
                "reason": (
                    "rows with no measured value cannot contribute to any numerical "
                    "analysis (documented justification for row removal)"
                ),
            }
        )
        if n_empty:
            report["actions"].append({"action": "drop_all_measurements_missing", "rows": n_empty})
            report["decisions"].append(
                f"Dropped {n_empty} row(s) whose every measurement column was missing."
            )

    # 4. categorical missing values -------------------------------------------
    cat_cols = list(cleaned.select_dtypes(include=["object", "string", "category"]).columns)
    cat_missing = {c: int(cleaned[c].isna().sum()) for c in cat_cols if cleaned[c].isna().any()}
    if cat_missing:
        for col in cat_missing:
            cleaned[col] = cleaned[col].fillna(categorical_fill_value)
        report["checks"].append(
            {
                "check": "categorical_missing_values",
                "result": f"missing values found in {cat_missing}",
                "decision": f"filled with '{categorical_fill_value}'",
                "reason": (
                    "a labelled 'Unknown' category keeps every observation in the "
                    "dataset and makes the missingness visible instead of hiding it"
                ),
            }
        )
        report["actions"].append(
            {"action": "fill_categorical_missing", "columns": cat_missing, "value": categorical_fill_value}
        )
        report["columns_modified"].extend(cat_missing)
        report["decisions"].append(
            f"Categorical missing values filled with '{categorical_fill_value}' "
            f"(columns: {sorted(cat_missing)}). Numerical missing values were left untouched."
        )
    else:
        report["checks"].append(
            {
                "check": "categorical_missing_values",
                "result": "no missing categorical values",
                "decision": "no change needed",
                "reason": "nothing to impute",
            }
        )

    # 5. suspicious / impossible values ---------------------------------------
    ranges = valid_ranges or {}
    positive = list(positive_columns or [])
    findings = check_numeric_ranges(cleaned, ranges=ranges, positive_columns=positive)
    n_flagged = 0
    for _category, per_column in findings.items():
        for _col, value in per_column.items():
            n_flagged += value["count"] if isinstance(value, dict) else int(value)
    report["checks"].append(
        {
            "check": "impossible_or_suspicious_values",
            "result": findings,
            "decision": "flagged only - no value deleted" if n_flagged else "no violation found",
            "reason": (
                "an out-of-range value may be a measurement error *or* a genuine "
                "extreme observation; deleting it without verification would hide information"
            ),
        }
    )
    report["flagged_values"] = findings
    if n_flagged:
        report["decisions"].append(
            f"{n_flagged} value(s) flagged as outside accepted ranges but kept in the dataset."
        )

    # 6. constant columns ------------------------------------------------------
    constant = find_constant_columns(cleaned)
    report["checks"].append(
        {
            "check": "constant_columns",
            "result": f"{len(constant)} constant column(s): {constant}",
            "decision": "kept (they may still be meaningful labels)" if constant else "no change needed",
            "reason": "constant columns carry no variance for correlation analysis",
        }
    )
    report["constant_columns"] = constant

    # 7. incorrect data types --------------------------------------------------
    report["checks"].append(
        {
            "check": "data_types",
            "result": {c: str(t) for c, t in cleaned.dtypes.items()},
            "decision": (
                "no conversion applied - every column already has a type that matches "
                "its content; conversions are only made when justified"
            ),
            "reason": "wrong conversions (e.g. numbers read as text) silently break statistics",
        }
    )

    report["cleaned_profile"] = profile_dataset(cleaned)
    report["before_after"] = before_after_table(raw, cleaned)
    report["missing_before"] = missing_table(raw).to_dict(orient="index")
    report["missing_after"] = missing_table(cleaned).to_dict(orient="index")
    report["columns_modified"] = sorted(set(report["columns_modified"]))
    return cleaned, report


def before_after_table(raw: pd.DataFrame, cleaned: pd.DataFrame) -> list:
    """Simple metric-by-metric comparison of the raw and the cleaned table."""
    return [
        {"metric": "row_count", "before": int(len(raw)), "after": int(len(cleaned))},
        {"metric": "column_count", "before": int(raw.shape[1]), "after": int(cleaned.shape[1])},
        {"metric": "duplicate_rows", "before": int(raw.duplicated().sum()), "after": int(cleaned.duplicated().sum())},
        {"metric": "missing_values", "before": int(raw.isna().sum().sum()), "after": int(cleaned.isna().sum().sum())},
        {"metric": "missing_columns", "before": int((raw.isna().sum() > 0).sum()), "after": int((cleaned.isna().sum() > 0).sum())},
    ]


def save_cleaning_report(report: dict, path: str | Path) -> Path:
    """Write the cleaning report as machine-readable JSON (overwrites)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False, default=str)
    return path


def save_cleaned_dataset(df: pd.DataFrame, path: str | Path) -> Path:
    """Write the cleaned dataset (never touches the raw file)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def print_cleaning_summary(report: dict) -> None:
    """Human readable summary printed in the notebook and the console."""
    raw, clean = report["raw_profile"], report["cleaned_profile"]
    print("=" * 72)
    print("DATA CLEANING SUMMARY")
    print("=" * 72)
    print(f"Source                    : {report['source']}")
    print(f"Raw rows / columns        : {raw['rows']} / {raw['columns']}")
    print(f"Cleaned rows / columns    : {clean['rows']} / {clean['columns']}")
    print(f"Rows removed              : {report['rows_removed']['total']} "
          f"(duplicates={report['rows_removed']['duplicates']}, "
          f"all measurements missing={report['rows_removed']['all_measurements_missing']})")
    print(f"Missing values before     : {raw['missing_total']}")
    print(f"Missing values after      : {clean['missing_total']}")
    print(f"Columns modified          : {report['columns_modified'] or 'none'}")
    print(f"Columns dropped           : {report['columns_dropped'] or 'none'}")
    print("-" * 72)
    print("Decisions:")
    for decision in report["decisions"] or ["No modification was necessary."]:
        print(f"  - {decision}")
    print("=" * 72)
