"""Relationship demos: seven correlation patterns with reproducible data.

Six demos are synthetic (seeded) because the real dataset does not contain
every possible pattern. One demo (``real``) is taken from the loaded dataset.

Every demo returns a small ``pandas.DataFrame`` with columns ``x`` and ``y``
so the caller can plot and compute statistics the same way for each case.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

DEFAULT_SEED = 42

DEMO_NAMES = [
    "strong_positive",
    "strong_negative",
    "weak_positive",
    "weak_negative",
    "no_linear",
    "nonlinear_parabola",
    "perfect_positive",
    "perfect_negative",
]


def _base_frame(x: np.ndarray, y: np.ndarray) -> pd.DataFrame:
    return pd.DataFrame({"x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float)})


def _pairs_with_target_r(
    n: int,
    target_r: float,
    seed: int = DEFAULT_SEED,
    low: float = 0.0,
    high: float = 10.0,
    y_scale: float = 10.0,
    y_shift: float = 50.0,
) -> pd.DataFrame:
    """Build (x, y) pairs whose Pearson correlation equals ``target_r``.

    x is uniform, the noise is Gaussian; both are standardised, then mixed:

        y_std = target_r * x_std + sqrt(1 - target_r^2) * noise_std

    so the resulting sample correlation is (almost exactly) the requested one.
    This keeps every demonstration reproducible *and* correctly labelled.
    """
    rng = np.random.default_rng(seed)
    x = rng.uniform(low, high, n)
    noise = rng.normal(0.0, 1.0, n)
    xs = (x - x.mean()) / x.std(ddof=0)
    ns = (noise - noise.mean()) / noise.std(ddof=0)
    # remove the linear component of the noise that points along x, so the
    # realised sample correlation equals the requested target almost exactly
    ns = ns - xs * float(xs @ ns) / float(xs @ xs)
    ns = ns / ns.std(ddof=0)
    a = float(target_r)
    b = float(np.sqrt(max(1.0 - a**2, 0.0)))
    y = (a * xs + b * ns) * y_scale + y_shift
    return _base_frame(x, y)


def demo_strong_positive(n: int = 120, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """y rises almost perfectly as x rises (r close to +0.95)."""
    return _pairs_with_target_r(n, 0.95, seed, y_scale=25.0, y_shift=5.0)


def demo_strong_negative(n: int = 120, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """y falls almost perfectly as x rises (r close to -0.95)."""
    return _pairs_with_target_r(n, -0.95, seed, y_scale=25.0, y_shift=40.0)


def demo_weak_positive(n: int = 200, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """A slight upward tendency hidden inside large noise (r close to +0.30)."""
    return _pairs_with_target_r(n, 0.30, seed)


def demo_weak_negative(n: int = 200, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """A slight downward tendency hidden inside large noise (r close to -0.30)."""
    return _pairs_with_target_r(n, -0.30, seed)


def demo_no_linear(n: int = 200, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """x and y are independent -> Pearson r lands close to zero."""
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, n)
    y = rng.normal(0, 1, n)
    return _base_frame(x, y)


def demo_nonlinear_parabola(n: int = 200, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """Strong *non-linear* dependence with r ~ 0 (teaching counter-example)."""
    rng = np.random.default_rng(seed)
    x = np.linspace(-3, 3, n)
    y = x**2 + rng.normal(0, 0.25, n)
    return _base_frame(x, y)


def demo_perfect_positive(n: int = 50) -> pd.DataFrame:
    """Exact linear relation y = 2x + 5 -> r = +1 with no noise."""
    x = np.linspace(0, 10, n)
    y = 2 * x + 5
    return _base_frame(x, y)


def demo_perfect_negative(n: int = 50) -> pd.DataFrame:
    """Exact linear relation y = -2x + 25 -> r = -1 with no noise."""
    x = np.linspace(0, 10, n)
    y = -2 * x + 25
    return _base_frame(x, y)


DEMOS = {
    "strong_positive": demo_strong_positive,
    "strong_negative": demo_strong_negative,
    "weak_positive": demo_weak_positive,
    "weak_negative": demo_weak_negative,
    "no_linear": demo_no_linear,
    "nonlinear_parabola": demo_nonlinear_parabola,
    "perfect_positive": demo_perfect_positive,
    "perfect_negative": demo_perfect_negative,
}


def make_demo(name: str, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """Return one demo by name (raises ``ValueError`` for unknown names)."""
    if name not in DEMOS:
        raise ValueError(f"Unknown demo '{name}'. Choose from {sorted(DEMOS)}.")
    factory = DEMOS[name]
    try:
        return factory(seed=seed)
    except TypeError:
        return factory()


def real_pair(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
) -> pd.DataFrame:
    """Extract a complete-case (x, y) pair from the real dataset.

    Missing values are dropped **pairwise** and the number of removed rows
    is recorded in ``df.attrs`` of the returned frame.
    """
    if x_col not in df.columns or y_col not in df.columns:
        raise KeyError(f"Columns '{x_col}' and/or '{y_col}' not found in dataset.")
    pair = df[[x_col, y_col]].dropna().rename(columns={x_col: "x", y_col: "y"})
    dropped = int(len(df) - len(pair))
    pair.attrs["x_name"] = x_col
    pair.attrs["y_name"] = y_col
    pair.attrs["rows_dropped_for_missing"] = dropped
    return pair


def demo_catalog(df: Optional[pd.DataFrame] = None) -> list:
    """Describe every relationship demo (used in tables / reports)."""
    from scipy import stats  # local import keeps module import light

    catalogue = []
    for name in DEMO_NAMES:
        frame = make_demo(name)
        r = float(stats.pearsonr(frame["x"], frame["y"]).statistic)
        catalogue.append({"demo": name, "n": len(frame), "pearson_r": round(r, 4)})
    if df is not None:
        catalogue.append(
            {
                "demo": "real_dataset (flipper vs mass)",
                "n": int(df[["flipper_length_mm", "body_mass_g"]].dropna().shape[0]),
                "pearson_r": round(
                    float(df["flipper_length_mm"].corr(df["body_mass_g"])), 4
                ),
            }
        )
    return catalogue
