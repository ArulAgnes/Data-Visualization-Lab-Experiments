"""Distribution analysis: the five canonical shapes + dataset summaries.

Synthetic generators use a fixed random seed so that every re-run produces
identical numbers and figures.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np
import pandas as pd
from scipy import stats

DEFAULT_SEED = 42


# --------------------------------------------------------------------------- #
# 1. Gaussian / normal
# --------------------------------------------------------------------------- #
def make_gaussian(n: int = 1000, mean: float = 50.0, std: float = 10.0, seed: int = DEFAULT_SEED) -> np.ndarray:
    """Bell-shaped, symmetric sample from N(mean, std)."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=mean, scale=std, size=n)


# --------------------------------------------------------------------------- #
# 2. Uniform
# --------------------------------------------------------------------------- #
def make_uniform(n: int = 1000, low: float = 0.0, high: float = 100.0, seed: int = DEFAULT_SEED) -> np.ndarray:
    """Every value in [low, high) is equally likely."""
    rng = np.random.default_rng(seed)
    return rng.uniform(low=low, high=high, size=n)


# --------------------------------------------------------------------------- #
# 3. Right-skewed (positive skew)
# --------------------------------------------------------------------------- #
def make_right_skewed(n: int = 1500, sigma: float = 0.6, seed: int = DEFAULT_SEED) -> np.ndarray:
    """Log-normal sample: bulk of the data on the left, long right tail."""
    rng = np.random.default_rng(seed)
    return rng.lognormal(mean=0.0, sigma=sigma, size=n)


# --------------------------------------------------------------------------- #
# 4. Left-skewed (negative skew)
# --------------------------------------------------------------------------- #
def make_left_skewed(n: int = 1500, sigma: float = 0.6, seed: int = DEFAULT_SEED) -> np.ndarray:
    """Mirror image of the log-normal sample: long left tail, bulk on the right."""
    rng = np.random.default_rng(seed)
    return -rng.lognormal(mean=0.0, sigma=sigma, size=n)


# --------------------------------------------------------------------------- #
# 5. Bimodal
# --------------------------------------------------------------------------- #
def make_bimodal(
    n: int = 1600,
    mean_a: float = 40.0,
    std_a: float = 6.0,
    mean_b: float = 70.0,
    std_b: float = 6.0,
    seed: int = DEFAULT_SEED,
) -> tuple:
    """Two normal subgroups with different means, returned as ``(values, labels)``."""
    rng = np.random.default_rng(seed)
    n_a = n // 2
    group_a = rng.normal(mean_a, std_a, n_a)
    group_b = rng.normal(mean_b, std_b, n - n_a)
    values = np.concatenate([group_a, group_b])
    labels = np.array(["group_A"] * n_a + ["group_B"] * (n - n_a))
    return values, labels


# --------------------------------------------------------------------------- #
# Summary statistics
# --------------------------------------------------------------------------- #
def summarise(values, name: str = "value") -> dict:
    """Descriptive statistics used for every distribution demonstration."""
    arr = np.asarray(pd.Series(values).dropna(), dtype=float)
    return {
        "variable": name,
        "n": int(arr.size),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr, ddof=1)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "skewness": float(stats.skew(arr)),
        "kurtosis": float(stats.kurtosis(arr)),  # excess kurtosis, normal = 0
        "shapiro_p_value": float(stats.shapiro(arr).pvalue) if arr.size <= 5000 else float("nan"),
    }


def summarise_table(rows: Sequence[dict]) -> pd.DataFrame:
    """Build a tidy DataFrame from one or more ``summarise`` dictionaries."""
    return pd.DataFrame(rows)


def dataset_distribution_summary(
    df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """Distribution summary for the real (cleaned) dataset columns.

    Skewness interpretation (rule of thumb, not a law of nature):
    ``|skew| < 0.5`` approximately symmetric, ``0.5..1`` moderate,
    ``> 1`` strong; mirrored for negative values.
    """
    if columns is None:
        columns = list(df.select_dtypes(include="number").columns)
    rows = []
    for col in columns:
        stats_dict = summarise(df[col].dropna(), name=col)
        stats_dict["shape"] = describe_shape(stats_dict["skewness"])
        rows.append(stats_dict)
    return pd.DataFrame(rows)


def describe_shape(skewness: float, threshold: float = 0.5) -> str:
    """Translate a skewness value into a beginner-friendly label."""
    if abs(skewness) < threshold:
        return "approximately symmetric"
    if skewness > 0:
        return "right-skewed (positive)" if skewness >= threshold * 2 else "slightly right-skewed"
    return "left-skewed (negative)" if skewness <= threshold * 2 else "slightly left-skewed"


def normal_reference_curve(values: np.ndarray) -> tuple:
    """Return ``(x, y)`` of a normal density fitted to ``values`` (overlay curve)."""
    arr = np.asarray(values, dtype=float)
    mean, std = float(np.mean(arr)), float(np.std(arr, ddof=1))
    x = np.linspace(mean - 4 * std, mean + 4 * std, 400)
    y = stats.norm.pdf(x, loc=mean, scale=std)
    return x, y
