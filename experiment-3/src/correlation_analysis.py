"""Pearson correlation: library helpers + from-scratch formula implementation.

Formula implemented manually:

    r = sum((x - mean(x)) * (y - mean(y)))
        / sqrt( sum((x - mean(x))**2) * sum((y - mean(y))**2) )
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import pandas as pd
from scipy import stats

# Configurable rule-of-thumb thresholds (NOT universal scientific laws).
STRENGTH_THRESHOLDS = {
    "very strong": 0.8,
    "strong": 0.6,
    "moderate": 0.4,
    "weak": 0.2,
    "negligible": 0.0,
}


def pearson_manual(x, y) -> float:
    """Pearson's r computed directly from the mathematical formula."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    dx = x - x.mean()
    dy = y - y.mean()
    numerator = float(np.sum(dx * dy))
    denominator = float(np.sqrt(np.sum(dx**2) * np.sum(dy**2)))
    if denominator == 0:
        raise ValueError("Pearson r is undefined when a variable has zero variance.")
    return numerator / denominator


def pearson_all_methods(x, y) -> dict:
    """Compute r with the manual formula and three standard libraries."""
    x = pd.Series(np.asarray(x, dtype=float)).dropna()
    y = pd.Series(np.asarray(y, dtype=float)).dropna()
    manual = pearson_manual(x, y)
    scipy_r = float(stats.pearsonr(x, y).statistic)
    numpy_r = float(np.corrcoef(x, y)[0, 1])
    pandas_r = float(pd.DataFrame({"x": x, "y": y}).corr(method="pearson").loc["x", "y"])
    return {
        "manual_formula": manual,
        "scipy.stats.pearsonr": scipy_r,
        "numpy.corrcoef": numpy_r,
        "pandas.DataFrame.corr": pandas_r,
        "max_absolute_difference": float(max(abs(manual - scipy_r), abs(manual - numpy_r), abs(manual - pandas_r))),
    }


def pearson_pair(x, y, alpha: float = 0.05, thresholds: Optional[dict] = None) -> dict:
    """Full pairwise statistics: r, p-value, n, direction, strength, significance.

    Missing values are removed pairwise (complete-case analysis) and the
    number of valid observations is reported.
    """
    xs, ys = pd.Series(x, dtype="float64"), pd.Series(y, dtype="float64")
    mask = xs.notna() & ys.notna()
    n_valid = int(mask.sum())
    n_dropped = int(len(xs) - n_valid)
    if n_valid < 3:
        raise ValueError("At least 3 complete (x, y) pairs are required for Pearson correlation.")

    xv, yv = xs[mask].to_numpy(), ys[mask].to_numpy()
    r = pearson_manual(xv, yv)
    result = stats.pearsonr(xv, yv)
    p_value = float(result.pvalue)
    ci_low = ci_high = float("nan")
    if hasattr(result, "confidence_interval"):
        try:
            ci = result.confidence_interval(confidence_level=0.95)
            ci_low, ci_high = float(ci.low), float(ci.high)
        except Exception:  # pragma: no cover - depends on scipy version
            pass

    return {
        "n_valid": n_valid,
        "n_missing_pairs_dropped": n_dropped,
        "pearson_r": float(r),
        "p_value": p_value,
        "r_squared": float(r**2),
        "direction": "positive" if r > 0 else ("negative" if r < 0 else "zero"),
        "strength": strength_label(abs(r), thresholds),
        "significant_at_alpha": bool(p_value < alpha),
        "alpha": alpha,
        "ci95_low": ci_low,
        "ci95_high": ci_high,
    }


def strength_label(abs_r: float, thresholds: Optional[dict] = None) -> str:
    """Map |r| to a strength category using configurable rule-of-thumb cut-offs."""
    thresholds = thresholds or STRENGTH_THRESHOLDS
    ordered = sorted(thresholds.items(), key=lambda kv: kv[1], reverse=True)
    for label, cut in ordered:
        if abs_r >= cut:
            return label
    return "negligible"


def pearson_matrix(
    df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
    method: str = "pearson",
) -> pd.DataFrame:
    """Correlation matrix of the selected (numeric) columns.

    Rows containing missing values are dropped pairwise by pandas; the number
    of complete rows used is reported by ``pairwise_n``.
    """
    if columns is None:
        columns = list(df.select_dtypes(include="number").columns)
    columns = [c for c in columns if c in df.columns]
    if len(columns) < 2:
        raise ValueError("At least two numerical columns are required for a correlation matrix.")
    sub = df[columns].apply(pd.to_numeric, errors="coerce")
    return sub.corr(method=method)


def pairwise_n(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """Number of complete observations behind every cell of the correlation matrix."""
    n_rows = len(columns)
    table = pd.DataFrame(np.nan, index=columns, columns=columns, dtype=float)
    for i, a in enumerate(columns):
        for b in columns[i:]:
            n = int(df[[a, b]].dropna().shape[0])
            table.loc[a, b] = n
            table.loc[b, a] = n
    return table.astype(int)


def format_matrix(matrix: pd.DataFrame, decimals: int = 2) -> pd.DataFrame:
    """Round a correlation matrix for pretty notebook display."""
    return matrix.round(decimals)


def save_correlation_matrix(matrix: pd.DataFrame, path: str | Path) -> Path:
    """Save the (rounded) correlation matrix as CSV (overwrites on re-run)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    matrix.round(4).to_csv(path)
    return path


def pair_report_table(pairs: Sequence[dict]) -> pd.DataFrame:
    """Tidy table of several ``pearson_pair`` results."""
    rows = []
    for entry in pairs:
        row = dict(entry)
        stats_dict = row.pop("stats", {})
        row.update(stats_dict)
        rows.append(row)
    return pd.DataFrame(rows)


def interpretation(entry: dict, x_name: str, y_name: str) -> str:
    """Beginner-friendly one-paragraph interpretation of a pairwise result."""
    r = entry["pearson_r"]
    direction = "increases" if r > 0 else "decreases"
    verdict = (
        f"r = {r:.3f} -> a {entry['strength']} {entry['direction']} linear relationship: "
        f"as {x_name} increases, {y_name} tends to {direction} as well."
    )
    if entry["significant_at_alpha"]:
        verdict += (
            f" The p-value ({entry['p_value']:.3g}) is below alpha = {entry['alpha']}, "
            "so the correlation is statistically significant - but significance is NOT causation."
        )
    else:
        verdict += (
            f" The p-value ({entry['p_value']:.3g}) is above alpha = {entry['alpha']}, "
            "so we cannot reject the 'no linear correlation' hypothesis."
        )
    return verdict
