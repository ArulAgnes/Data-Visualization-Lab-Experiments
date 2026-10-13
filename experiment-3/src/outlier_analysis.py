"""Outlier detection with the Interquartile Range (IQR) rule.

    Q1  = 25th percentile
    Q3  = 75th percentile
    IQR = Q3 - Q1
    lower fence = Q1 - 1.5 * IQR
    upper fence = Q3 + 1.5 * IQR

Values outside the fences are *potential* outliers. They are reported, never
automatically deleted - an outlier can be a data error, a valid extreme
observation, or an important rare event.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import pandas as pd

DEFAULT_SEED = 42
FENCE_MULTIPLIER = 1.5


def iqr_bounds(series, multiplier: float = FENCE_MULTIPLIER) -> dict:
    """Compute Q1, Q3, IQR and the Tukey fences of one numerical variable."""
    values = pd.Series(series, dtype="float64").dropna()
    if values.empty:
        raise ValueError("Cannot compute IQR bounds of an empty series.")
    q1 = float(values.quantile(0.25))
    q3 = float(values.quantile(0.75))
    iqr = q3 - q1
    lower = q1 - multiplier * iqr
    upper = q3 + multiplier * iqr
    outliers = values[(values < lower) | (values > upper)]
    return {
        "n": int(values.size),
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "multiplier": multiplier,
        "lower_fence": lower,
        "upper_fence": upper,
        "n_outliers": int(outliers.size),
        "percent_outliers": float(round(100 * outliers.size / values.size, 3)),
        "outlier_values": [float(v) for v in outliers.sort_values()],
        "min": float(values.min()),
        "max": float(values.max()),
    }


def detect_outliers(
    df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
    group_col: Optional[str] = None,
    multiplier: float = FENCE_MULTIPLIER,
    index_name: str = "index",
) -> tuple:
    """Run the IQR rule on every requested column.

    ``group_col`` (e.g. species) enables *grouped* detection, which is the
    honest approach when sub-populations have different typical values.

    Returns ``(rows_for_report_table, detail_dict)``.
    """
    if columns is None:
        columns = list(df.select_dtypes(include="number").columns)
    columns = [c for c in columns if c in df.columns]
    if not columns:
        raise ValueError("No numerical columns available for outlier detection.")

    report_rows = []
    detail: dict = {}

    def _evaluate(sub: pd.DataFrame, col: str, scope: str, label: str) -> None:
        stats = iqr_bounds(sub[col], multiplier=multiplier)
        idx = sub.index[(sub[col] < stats["lower_fence"]) | (sub[col] > stats["upper_fence"])]
        # keep row identifiers readable in the report
        identifiers = [f"{index_name}={i}" for i in idx.tolist()]
        detail[f"{scope}::{col}"] = {**stats, "outlier_row_ids": identifiers}
        report_rows.append(
            {
                "scope": scope,
                "group": label,
                "variable": col,
                "n": stats["n"],
                "q1": round(stats["q1"], 4),
                "q3": round(stats["q3"], 4),
                "iqr": round(stats["iqr"], 4),
                "lower_fence": round(stats["lower_fence"], 4),
                "upper_fence": round(stats["upper_fence"], 4),
                "n_outliers": stats["n_outliers"],
                "percent_outliers": stats["percent_outliers"],
                "outlier_values": ", ".join(f"{v:g}" for v in stats["outlier_values"][:12]),
                "outlier_row_ids": ", ".join(identifiers[:12]),
            }
        )

    for col in columns:
        _evaluate(df, col, "overall", "all rows")
        if group_col is not None and group_col in df.columns:
            for label, sub in df.groupby(group_col, observed=True):
                _evaluate(sub, col, f"by_{group_col}", str(label))

    report_df = pd.DataFrame(report_rows)
    return report_df, detail


def save_outlier_report(report_df: pd.DataFrame, path: str | Path) -> Path:
    """Write the outlier report as CSV (overwrites on re-run)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    report_df.to_csv(path, index=False)
    return path


def synthetic_outlier_example(n: int = 100, seed: int = DEFAULT_SEED) -> pd.Series:
    """Clearly labelled synthetic sample containing known extreme values.

    Used only for teaching the IQR mechanics - the real dataset is never
    modified with these artificial points.
    """
    rng = np.random.default_rng(seed)
    base = rng.normal(loc=50, scale=5, size=n)
    extreme = np.array([5.0, 8.5, 130.0, 145.0])  # known injected outliers
    values = np.concatenate([base, extreme])
    series = pd.Series(values, name="synthetic_measurement")
    series.attrs["known_outliers"] = extreme.tolist()
    return series


def print_outlier_summary(report_df: pd.DataFrame, scope: str = "overall") -> None:
    """Console/notebook friendly summary of the IQR results."""
    subset = report_df[report_df["scope"] == scope]
    print("=" * 72)
    print(f"IQR OUTLIER DETECTION ({scope})")
    print("=" * 72)
    if subset.empty:
        print("No rows to display.")
        return
    for _, row in subset.iterrows():
        status = "NO outlier detected" if row["n_outliers"] == 0 else f"{row['n_outliers']} outlier(s)"
        print(
            f"{row['variable']:<22} fences=({row['lower_fence']:>9.2f}, {row['upper_fence']:>9.2f})  "
            f"-> {status} ({row['percent_outliers']:.2f}%)"
        )
    print("=" * 72)
