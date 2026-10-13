#!/usr/bin/env python
"""Unified command-line runner for Experiment 3 (EDA).

Runs the complete experiment in sequence:

    python src/run_eda.py --data data/raw/penguins.csv --output outputs

Every figure is written to ``outputs/plots``, every report to
``outputs/reports`` and the execution log to ``outputs/logs``.
Re-running the script overwrites the previous outputs (idempotent).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# headless-safe backend BEFORE matplotlib is imported anywhere
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# allow "python src/run_eda.py" from any working directory
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SRC_DIR.parent))

from src import data_cleaning, correlation_analysis, distribution_analysis
from src import outlier_analysis, regression_analysis, relationship_analysis
from src.data_loader import (
    outputs_dir,
    set_outputs_dirname,
    describe_environment,
    ensure_output_dirs,
    find_project_root,
    initial_inspection,
    kaggle_credentials_available,
    list_columns,
    load_dataset,
    missing_report,
    resolve_dataset_path,
)
from src.visualization import apply_style, new_figure, save_figure, subplots

LOGGER = logging.getLogger("eda_experiment3")
GENERATED_FILES: list[str] = []


def _record(path) -> Path:
    path = Path(path)
    GENERATED_FILES.append(str(path))
    return path


def setup_logging(log_dir: Path, verbose: bool = True) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "eda_run.log"
    LOGGER.setLevel(logging.INFO)
    LOGGER.handlers.clear()
    formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)
    if verbose:
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        LOGGER.addHandler(stream)
    _record(log_file)


def step_environment() -> dict:
    info = describe_environment()
    LOGGER.info("Python %s on %s", info["python_version"], info["platform"])
    LOGGER.info("Colab=%s Kaggle=%s", info["google_colab"], info["kaggle"])
    for name, version in info["libraries"].items():
        LOGGER.info("  library %-10s %s", name, version)
    LOGGER.info("Kaggle credentials available: %s (contents never displayed)", kaggle_credentials_available())
    return info


def step_load(data_path, root: Path, valid_ranges: dict, positive_columns: list):
    LOGGER.info("Loading dataset: %s", data_path)
    raw = load_dataset(data_path, root=root, allow_upload=False)
    info = initial_inspection(raw)
    LOGGER.info("Dataset shape: %s x %s", *info["shape"])
    LOGGER.info("Columns: %s", info["columns"])
    LOGGER.info("Duplicate rows: %s | missing values: %s", info["duplicate_rows"], info["missing_total"])
    report_path = _record(outputs_dir(root) / "reports" / "dataset_profile.json")
    with report_path.open("w", encoding="utf-8") as fh:
        json.dump({"inspection": info, "missing": missing_report(raw).to_dict(orient="index")}, fh, indent=2, default=str)
    cleaned, cleaning_report = data_cleaning.clean_dataset(
        raw,
        valid_ranges=valid_ranges,
        positive_columns=positive_columns,
        source=str(data_path),
    )
    data_cleaning.print_cleaning_summary(cleaning_report)
    cleaned_path = _record(data_cleaning.save_cleaned_dataset(cleaned, root / "data" / "processed" / "cleaned_dataset.csv"))
    report_path = _record(data_cleaning.save_cleaning_report(cleaning_report, outputs_dir(root) / "reports" / "data_cleaning_report.json"))
    LOGGER.info("Saved cleaned dataset -> %s", cleaned_path)
    LOGGER.info("Saved cleaning report -> %s", report_path)
    return raw, cleaned, cleaning_report


def step_descriptive_statistics(cleaned: pd.DataFrame, root: Path) -> dict:
    columns = list_columns(cleaned)
    num_cols, cat_cols = columns["numerical"], columns["categorical"]
    desc_num = cleaned[num_cols].describe().T
    desc_cat = cleaned[cat_cols].astype("string").describe()
    LOGGER.info("Descriptive statistics (numerical):\n%s", desc_num.to_string())
    LOGGER.info("Descriptive statistics (categorical):\n%s", desc_cat.to_string())
    payload = {
        "numerical_columns": num_cols,
        "categorical_columns": cat_cols,
        "numerical_summary": desc_num.to_dict(orient="index"),
        "categorical_summary": desc_cat.to_dict(),
        "unique_values": {c: int(cleaned[c].nunique(dropna=True)) for c in cleaned.columns},
    }
    path = _record(outputs_dir(root) / "reports" / "descriptive_statistics.json")
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str)
    return payload


def step_synthetic_distributions(root: Path, seed: int) -> pd.DataFrame:
    """Five canonical shapes, clearly separated from the real-dataset analysis."""
    generators = [
        ("distribution_gaussian", "Gaussian (Normal) Distribution", distribution_analysis.make_gaussian),
        ("distribution_uniform", "Uniform Distribution", distribution_analysis.make_uniform),
        ("distribution_right_skewed", "Right-Skewed (Positive) Distribution", distribution_analysis.make_right_skewed),
        ("distribution_left_skewed", "Left-Skewed (Negative) Distribution", distribution_analysis.make_left_skewed),
    ]
    rows = []
    for filename, title, generator in generators:
        values = generator(seed=seed)
        summary = distribution_analysis.summarise(values, name=filename)
        rows.append(summary)
        fig = new_figure((8, 5))
        ax = fig.gca()
        ax.hist(values, bins=40, density=True, alpha=0.65, edgecolor="white", label="Histogram")
        try:
            sns.kdeplot(values, ax=ax, linewidth=2, label="KDE")
        except Exception:
            pass
        if "gaussian" in filename:
            x, y = distribution_analysis.normal_reference_curve(values)
            ax.plot(x, y, "r--", linewidth=2, label="Fitted normal curve")
        ax.set_title(f"{title}\nmean={summary['mean']:.2f}, median={summary['median']:.2f}, std={summary['std']:.2f}, skew={summary['skewness']:.2f}")
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.legend()
        path = _record(save_figure(fig, filename, root=root))
        plt.close(fig)
        LOGGER.info("Saved %s | skewness=%.3f", path.name, summary["skewness"])

    # bimodal
    values, labels = distribution_analysis.make_bimodal(seed=seed)
    summary = distribution_analysis.summarise(values, name="distribution_bimodal")
    rows.append(summary)
    fig = new_figure((8, 5))
    ax = fig.gca()
    for label, colour in (("group_A", "#4c72b0"), ("group_B", "#c44e52")):
        subset = values[labels == label]
        ax.hist(subset, bins=40, density=True, alpha=0.55, color=colour, edgecolor="white", label=label)
    sns.kdeplot(values, ax=ax, linewidth=2, color="black", label="KDE of combined data")
    ax.set_title(
        f"Bimodal Distribution (two overlapping groups)\n"
        f"mean={summary['mean']:.2f}, median={summary['median']:.2f}, skew={summary['skewness']:.2f}"
    )
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    ax.legend()
    path = _record(save_figure(fig, "distribution_bimodal", root=root))
    plt.close(fig)
    LOGGER.info("Saved %s", path.name)

    table = pd.DataFrame(rows)
    csv_path = _record(outputs_dir(root) / "reports" / "distribution_summary.csv")
    table.round(4).to_csv(csv_path, index=False)
    LOGGER.info("Saved distribution summary -> %s", csv_path)
    return table


def step_dataset_distributions(cleaned: pd.DataFrame, numeric_cols: list, root: Path) -> pd.DataFrame:
    summary = distribution_analysis.dataset_distribution_summary(cleaned, numeric_cols)
    LOGGER.info("Dataset distribution summary:\n%s", summary[["variable", "mean", "median", "std", "skewness", "shape"]].to_string(index=False))
    path = _record(outputs_dir(root) / "reports" / "dataset_distribution_summary.csv")
    summary.round(4).to_csv(path, index=False)

    n = len(numeric_cols)
    ncols = min(2, n)
    nrows = int(np.ceil(n / ncols))
    fig, axes = subplots(nrows, ncols, figsize=(6 * ncols, 4 * nrows))
    axes = np.atleast_1d(axes).ravel()
    for ax, col in zip(axes, numeric_cols):
        sns.histplot(cleaned[col].dropna(), bins=30, kde=True, ax=ax, color="#4c72b0")
        stats_row = summary[summary["variable"] == col].iloc[0]
        ax.set_title(f"{col}\nmean={stats_row['mean']:.2f}, median={stats_row['median']:.2f}, skew={stats_row['skewness']:.2f}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
    for ax in axes[n:]:
        ax.axis("off")
    fig.suptitle("Distribution analysis of the real dataset", fontsize=14)
    path = _record(save_figure(fig, "dataset_distributions", root=root))
    plt.close(fig)

    fig, axes = subplots(nrows, ncols, figsize=(6 * ncols, 4 * nrows))
    axes = np.atleast_1d(axes).ravel()
    for ax, col in zip(axes, numeric_cols):
        stats.probplot(cleaned[col].dropna(), dist="norm", plot=ax)
        ax.set_title(f"Q-Q plot: {col}")
        ax.get_lines()[0].set(marker="o", markersize=2.5, alpha=0.6)
        ax.get_lines()[1].set(color="red", linewidth=1.5)
    for ax in axes[n:]:
        ax.axis("off")
    fig.suptitle("Q-Q plots (points on the red line = normally distributed)", fontsize=14)
    path = _record(save_figure(fig, "dataset_qq_plots", root=root))
    plt.close(fig)
    LOGGER.info("Saved dataset distribution figures")
    return summary


def step_relationship_demos(root: Path, seed: int, cleaned: pd.DataFrame) -> pd.DataFrame:
    specs = [
        ("correlation_strong_positive", "strong_positive", "Strong positive correlation"),
        ("correlation_strong_negative", "strong_negative", "Strong negative correlation"),
        ("correlation_weak_positive", "weak_positive", "Weak positive correlation"),
        ("correlation_weak_negative", "weak_negative", "Weak negative correlation"),
        ("correlation_perfect_positive", "perfect_positive", "Perfect positive linear correlation (r = +1)"),
        ("correlation_perfect_negative", "perfect_negative", "Perfect negative linear correlation (r = -1)"),
    ]
    rows = []
    for filename, demo_name, title in specs:
        frame = relationship_analysis.make_demo(demo_name, seed=seed)
        r = float(stats.pearsonr(frame["x"], frame["y"]).statistic)
        rows.append({"demo": demo_name, "n": len(frame), "pearson_r": round(r, 4)})
        fig = new_figure((7, 5))
        ax = fig.gca()
        ax.scatter(frame["x"], frame["y"], s=28, alpha=0.75, edgecolor="white", linewidth=0.4)
        ax.set_title(f"{title}\nPearson r = {r:.3f}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        path = _record(save_figure(fig, filename, root=root))
        plt.close(fig)
        LOGGER.info("Saved %s (r=%.3f)", path.name, r)

    # no-linear correlation: independent noise AND a parabolic relation (r ~ 0)
    independent = relationship_analysis.demo_no_linear(seed=seed)
    parabola = relationship_analysis.demo_nonlinear_parabola(seed=seed)
    r_ind = float(stats.pearsonr(independent["x"], independent["y"]).statistic)
    r_par = float(stats.pearsonr(parabola["x"], parabola["y"]).statistic)
    rows.append({"demo": "no_linear_independent", "n": len(independent), "pearson_r": round(r_ind, 4)})
    rows.append({"demo": "no_linear_parabola", "n": len(parabola), "pearson_r": round(r_par, 4)})
    fig, (ax1, ax2) = subplots(1, 2, figsize=(12, 5))
    ax1.scatter(independent["x"], independent["y"], s=28, alpha=0.75, color="#55a868", edgecolor="white")
    ax1.set_title(f"Independent x and y\nPearson r = {r_ind:.3f}")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax2.scatter(parabola["x"], parabola["y"], s=28, alpha=0.75, color="#c44e52", edgecolor="white")
    ax2.set_title(f"Non-linear (parabolic) relation\nPearson r = {r_par:.3f}")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    fig.suptitle("r close to 0 does NOT mean 'no relationship' - only 'no LINEAR relationship'", fontsize=13)
    path = _record(save_figure(fig, "correlation_no_linear", root=root))
    plt.close(fig)
    LOGGER.info("Saved correlation_no_linear.png (r_ind=%.3f, r_par=%.3f)", r_ind, r_par)

    # real dataset pairs
    real_pairs = [
        ("flipper_length_mm", "body_mass_g"),
        ("bill_length_mm", "flipper_length_mm"),
        ("bill_depth_mm", "flipper_length_mm"),
        ("year", "body_mass_g"),
    ]
    for x_col, y_col in real_pairs:
        pair = relationship_analysis.real_pair(cleaned, x_col, y_col)
        entry = correlation_analysis.pearson_pair(pair["x"], pair["y"])
        rows.append({"demo": f"real::{x_col}~{y_col}", "n": entry["n_valid"], "pearson_r": round(entry["pearson_r"], 4)})
        fig = new_figure((7, 5))
        ax = fig.gca()
        colours = cleaned.loc[pair.index, "species"] if "species" in cleaned.columns else None
        ax.scatter(pair["x"], pair["y"], s=30, alpha=0.75, c="#4c72b0" if colours is None else None, edgecolor="white")
        if colours is not None:
            for spec, sub in pair.groupby(cleaned.loc[pair.index, "species"]):
                ax.scatter(sub["x"], sub["y"], s=30, alpha=0.8, label=spec, edgecolor="white")
            ax.legend(title="species")
        ax.set_title(
            f"Real data: {x_col} vs {y_col}\nPearson r = {entry['pearson_r']:.3f} "
            f"({entry['strength']}, {entry['direction']}), p = {entry['p_value']:.2g}, n = {entry['n_valid']}"
        )
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        path = _record(save_figure(fig, f"real_scatter_{x_col}_vs_{y_col}", root=root))
        plt.close(fig)
        LOGGER.info("Real pair %s~%s: r=%.3f p=%.3g n=%d", x_col, y_col, entry["pearson_r"], entry["p_value"], entry["n_valid"])

    table = pd.DataFrame(rows)
    csv_path = _record(outputs_dir(root) / "reports" / "correlation_demo_summary.csv")
    table.to_csv(csv_path, index=False)
    return table


def step_correlation_matrix(cleaned: pd.DataFrame, numeric_cols: list, root: Path) -> pd.DataFrame:
    matrix = correlation_analysis.pearson_matrix(cleaned, numeric_cols)
    n_table = correlation_analysis.pairwise_n(cleaned, numeric_cols)
    csv_path = _record(correlation_analysis.save_correlation_matrix(matrix, outputs_dir(root) / "reports" / "pearson_correlation_matrix.csv"))
    LOGGER.info("Correlation matrix saved -> %s", csv_path)

    fig, ax = subplots(1, 1, figsize=(9, 7))
    sns.heatmap(
        matrix,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0.0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"label": "Pearson r"},
        ax=ax,
    )
    ax.set_title(f"Pearson correlation matrix ({len(numeric_cols)} numerical columns)\ncomplete rows used per pair: {int(n_table.min().min())}-{int(n_table.max().max())}")
    path = _record(save_figure(fig, "pearson_correlation_heatmap", root=root))
    plt.close(fig)
    LOGGER.info("Saved %s", path.name)
    return matrix


def step_pearson_teaching_example(root: Path) -> dict:
    """Small labelled example comparing the manual formula with the libraries."""
    x = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
    y = np.array([1.0, 3.0, 5.0, 7.0, 9.0])
    comparison = correlation_analysis.pearson_all_methods(x, y)
    LOGGER.info("Teaching example x=%s y=%s", x.tolist(), y.tolist())
    for method, value in comparison.items():
        LOGGER.info("  %-24s %s", method, value)
    payload = {"x": x.tolist(), "y": y.tolist(), **comparison}
    path = _record(outputs_dir(root) / "reports" / "pearson_formula_example.json")
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return payload


def step_regression(cleaned: pd.DataFrame, x_col: str, y_col: str, root: Path, test_size: float, random_state: int) -> dict:
    result = regression_analysis.fit_simple_regression(
        cleaned, x_col, y_col, test_size=test_size, random_state=random_state
    )
    LOGGER.info("Regression: %s", result["equation"])
    LOGGER.info("  split: %s", result["split_note"])
    LOGGER.info("  test metrics: %s", result["metrics_test"])

    data = result["data"]
    fig = new_figure((8, 6))
    ax = fig.gca()
    ax.scatter(data[x_col], data[y_col], s=28, alpha=0.65, color="#4c72b0", label="Observations")
    x_line = np.linspace(data[x_col].min(), data[x_col].max(), 100).reshape(-1, 1)
    ax.plot(x_line, result["model"].predict(x_line), color="red", linewidth=2, label=f"Fit: {result['equation']}")
    ax.set_title(f"Simple linear regression: {y_col} ~ {x_col}\nr = {result['pearson_r']:.3f}, R² = {result['pearson_r']**2:.3f}")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend()
    path = _record(save_figure(fig, "linear_regression_fit", root=root))
    plt.close(fig)

    fig, ax = subplots(1, 1, (7, 6))
    ax.scatter(result["y_test"], result["y_pred_test"], s=30, alpha=0.7, color="#55a868")
    lo = min(result["y_test"].min(), result["y_pred_test"].min())
    hi = max(result["y_test"].max(), result["y_pred_test"].max())
    ax.plot([lo, hi], [lo, hi], "r--", linewidth=1.5, label="Perfect prediction line")
    ax.set_title(f"Actual vs predicted ({y_col}, test set)\nRMSE = {result['metrics_test']['RMSE']:.1f}")
    ax.set_xlabel("Actual values")
    ax.set_ylabel("Predicted values")
    ax.legend()
    path = _record(save_figure(fig, "actual_vs_predicted", root=root))
    plt.close(fig)

    fig, ax = subplots(1, 1, (8, 5))
    ax.scatter(result["y_pred_full"], result["residuals_full"], s=28, alpha=0.65, color="#8172b3")
    ax.axhline(0, color="red", linewidth=1.5)
    ax.set_title("Residual plot (residuals vs fitted values)")
    ax.set_xlabel(f"Fitted values ({y_col})")
    ax.set_ylabel("Residual (actual - predicted)")
    path = _record(save_figure(fig, "regression_residuals", root=root))
    plt.close(fig)

    fig, ax = subplots(1, 1, (8, 5))
    ax.hist(result["residuals_full"], bins=30, density=True, alpha=0.7, color="#4c72b0", edgecolor="white", label="Residuals")
    xr, yr = distribution_analysis.normal_reference_curve(result["residuals_full"])
    ax.plot(xr, yr, "r--", linewidth=2, label="Normal reference curve")
    ax.axvline(0, color="black", linewidth=1)
    ax.set_title("Distribution of residuals (should look roughly normal)")
    ax.set_xlabel("Residual")
    ax.set_ylabel("Density")
    ax.legend()
    path = _record(save_figure(fig, "residual_distribution", root=root))
    plt.close(fig)

    payload = regression_analysis.metrics_payload(result)
    payload["prediction_example"] = regression_analysis.predict_for(
        result, float(np.median(data[x_col]))
    )
    metrics_path = _record(regression_analysis.save_metrics(payload, outputs_dir(root) / "reports" / "regression_metrics.json"))
    LOGGER.info("Saved regression metrics -> %s", metrics_path)
    return result


def step_outliers(cleaned: pd.DataFrame, numeric_cols: list, root: Path, group_col: str = "species") -> pd.DataFrame:
    group = group_col if group_col in cleaned.columns else None
    report_df, detail = outlier_analysis.detect_outliers(cleaned, numeric_cols, group_col=group)
    outlier_analysis.print_outlier_summary(report_df, scope="overall")
    if group:
        outlier_analysis.print_outlier_summary(report_df, scope=f"by_{group}")
    path = _record(outlier_analysis.save_outlier_report(report_df, outputs_dir(root) / "reports" / "outlier_report.csv"))
    LOGGER.info("Saved outlier report -> %s", path)

    n_overall = int(report_df[report_df["scope"] == "overall"]["n_outliers"].sum())
    n_grouped = int(report_df[report_df["scope"] != "overall"]["n_outliers"].sum())
    LOGGER.info("Outliers overall: %d | outliers inside subgroups (%s): %d", n_overall, group, n_grouped)

    # individual box plots
    n = len(numeric_cols)
    ncols = min(2, n)
    nrows = int(np.ceil(n / ncols))
    fig, axes = subplots(nrows, ncols, figsize=(6 * ncols, 4 * nrows))
    axes = np.atleast_1d(axes).ravel()
    for ax, col in zip(axes, numeric_cols):
        sns.boxplot(y=cleaned[col], ax=ax, color="#4c72b0", width=0.45, flierprops=dict(marker="o", markersize=4, alpha=0.7))
        ax.set_title(f"Box plot: {col}")
        ax.set_ylabel(col)
    for ax in axes[n:]:
        ax.axis("off")
    fig.suptitle("Individual box plots (points = potential outliers by the 1.5 x IQR rule)", fontsize=13)
    path = _record(save_figure(fig, "boxplot_outlier_detection", root=root))
    plt.close(fig)

    # combined (standardised) box plot
    z = (cleaned[numeric_cols] - cleaned[numeric_cols].mean()) / cleaned[numeric_cols].std(ddof=1)
    fig, ax = subplots(1, 1, (10, 5))
    sns.boxplot(data=z, ax=ax, orient="h", palette="Set2")
    ax.set_title("Combined box plot of all numerical columns (standardised: z-scores)\nstandardisation makes columns with different units comparable")
    ax.set_xlabel("z-score (number of standard deviations from the mean)")
    path = _record(save_figure(fig, "boxplot_all_numeric", root=root))
    plt.close(fig)

    # synthetic outlier demonstration (clearly separated from the real data)
    synth = outlier_analysis.synthetic_outlier_example()
    bounds = outlier_analysis.iqr_bounds(synth)
    fig, ax = subplots(1, 2, (12, 5))
    sns.histplot(synth, bins=30, kde=True, ax=ax[0], color="#dd8452")
    ax[0].set_title("Synthetic data with injected outliers\n(injected values: "
                    + ", ".join(f"{v:g}" for v in synth.attrs["known_outliers"]) + ")")
    ax[0].set_xlabel("Value")
    sns.boxplot(y=synth, ax=ax[1], color="#dd8452", width=0.4)
    ax[1].axhline(bounds["lower_fence"], color="red", linestyle="--", label=f"lower fence {bounds['lower_fence']:.1f}")
    ax[1].axhline(bounds["upper_fence"], color="red", linestyle="--", label=f"upper fence {bounds['upper_fence']:.1f}")
    ax[1].set_title(f"Synthetic box plot\n{bounds['n_outliers']} potential outliers detected")
    ax[1].legend()
    path = _record(save_figure(fig, "boxplot_synthetic_example", root=root))
    plt.close(fig)
    LOGGER.info("Saved box plots (synthetic example outliers: %d)", bounds["n_outliers"])
    return report_df


def step_additional_visualisations(cleaned: pd.DataFrame, numeric_cols: list, cat_cols: list, root: Path) -> None:
    # pair plot
    plot_cols = numeric_cols + [c for c in ("species",) if c in cleaned.columns]
    pair = sns.pairplot(cleaned[plot_cols].dropna(), hue="species" if "species" in cleaned.columns else None, diag_kind="kde")
    pair.figure.suptitle("Pair plot of the numerical variables (coloured by species)", y=1.02)
    path = _record(save_figure(pair.figure, "pairplot", root=root))
    plt.close(pair.figure)

    # violin plots
    fig, axes = subplots(1, len(numeric_cols), figsize=(4.2 * len(numeric_cols), 5))
    axes = np.atleast_1d(axes).ravel()
    hue = "species" if "species" in cleaned.columns else None
    for ax, col in zip(axes, numeric_cols):
        sns.violinplot(data=cleaned, x=hue, y=col, ax=ax, inner="quartile", palette="Set2")
        ax.set_title(col)
        ax.set_xlabel(hue or "")
    fig.suptitle("Violin plots: distribution shape of every numerical variable by species", fontsize=13)
    path = _record(save_figure(fig, "violin_by_species", root=root))
    plt.close(fig)

    # count plots for categorical columns
    cats = [c for c in cat_cols if cleaned[c].nunique() <= 10]
    if cats:
        fig, axes = subplots(1, len(cats), figsize=(4.5 * len(cats), 4.5))
        axes = np.atleast_1d(axes).ravel()
        for ax, col in zip(axes, cats):
            order = cleaned[col].value_counts().index
            sns.countplot(data=cleaned, x=col, order=order, ax=ax, palette="Set2", hue=col, legend=False)
            ax.set_title(f"Count plot: {col}")
            ax.tick_params(axis="x", rotation=30)
        fig.suptitle("Frequency of the categorical values", fontsize=13)
        path = _record(save_figure(fig, "countplots_categorical", root=root))
        plt.close(fig)

    # bar chart of a categorical summary
    if "species" in cleaned.columns and "body_mass_g" in cleaned.columns:
        summary = cleaned.groupby("species")["body_mass_g"].agg(["mean", "std"]).reset_index()
        fig, ax = subplots(1, 1, (8, 5))
        ax.bar(summary["species"], summary["mean"], yerr=summary["std"], capsize=8, color=["#4c72b0", "#55a868", "#c44e52"], alpha=0.85)
        ax.set_title("Mean body mass by species (error bars = +/- 1 standard deviation)")
        ax.set_xlabel("Species")
        ax.set_ylabel("Mean body mass (g)")
        path = _record(save_figure(fig, "barplot_mean_mass_by_species", root=root))
        plt.close(fig)
    LOGGER.info("Saved additional statistical visualisations")


def step_zip(root: Path, zip_name: str = "eda_experiment3_outputs.zip") -> Path:
    """Package plots, reports, cleaned data, scripts and the notebook."""
    zip_path = outputs_dir(root) / zip_name
    include = [
        outputs_dir(root) / "plots",
        outputs_dir(root) / "reports",
        outputs_dir(root) / "logs",
        root / "data" / "processed",
        root / "data" / "raw",
        root / "src",
        root / "tests",
    ]
    optional_files = [
        root / "EXPERIMENT 3.ipynb",
        root / "README.md",
        root / "requirements.txt",
        root / ".gitignore",
    ]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder in include:
            if not folder.exists():
                continue
            for file in sorted(folder.rglob("*")):
                if not file.is_file():
                    continue
                if "__pycache__" in file.parts or file.suffix in {".pyc", ".pyo"}:
                    continue
                zf.write(file, file.relative_to(root))
        for file in optional_files:
            if file.exists():
                zf.write(file, file.relative_to(root))
    LOGGER.info("Packaged outputs -> %s", zip_path)
    _record(zip_path)
    return zip_path


def run_all(
    data_path=None,
    output_root: Optional[Path] = None,
    seed: int = 42,
    x_col: str = "flipper_length_mm",
    y_col: str = "body_mass_g",
    test_size: float = 0.25,
    random_state: int = 42,
    make_zip: bool = True,
    verbose: bool = True,
) -> dict:
    """Run the whole experiment and return a summary dictionary."""
    root = find_project_root()
    if output_root:
        set_outputs_dirname(output_root)
    dirs = ensure_output_dirs(root)
    setup_logging(dirs["logs"], verbose=verbose)
    started = datetime.now(timezone.utc)
    LOGGER.info("=" * 72)
    LOGGER.info("EXPERIMENT 3 - Exploratory Data Analysis Through Statistical Visualization")
    LOGGER.info("=" * 72)

    env = step_environment()
    resolved = resolve_dataset_path(data_path, root=root, allow_upload=False)

    valid_ranges = {
        "bill_length_mm": (25.0, 70.0),
        "bill_depth_mm": (10.0, 25.0),
        "flipper_length_mm": (150.0, 250.0),
        "body_mass_g": (2000.0, 7000.0),
        "year": (2007, 2009),
    }
    positive_columns = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

    raw, cleaned, cleaning_report = step_load(resolved, root, valid_ranges, positive_columns)
    columns = list_columns(cleaned)
    numeric_cols, cat_cols = columns["numerical"], columns["categorical"]
    # continuous measurements = numeric columns with enough distinct values
    # (low-cardinality integer codes such as 'year' are kept for the correlation
    #  matrix but excluded from distribution / box-plot analysis)
    measurement_cols = [c for c in numeric_cols if cleaned[c].nunique(dropna=True) > 10] or numeric_cols
    LOGGER.info("Numerical columns: %s", numeric_cols)
    LOGGER.info("Continuous measurement columns: %s", measurement_cols)
    LOGGER.info("Categorical columns: %s", cat_cols)

    step_descriptive_statistics(cleaned, root)
    step_synthetic_distributions(root, seed)
    step_dataset_distributions(cleaned, measurement_cols, root)
    step_relationship_demos(root, seed, cleaned)
    step_pearson_teaching_example(root)
    step_correlation_matrix(cleaned, numeric_cols, root)
    regression_result = step_regression(cleaned, x_col, y_col, root, test_size, random_state)
    step_outliers(cleaned, measurement_cols, root)
    step_additional_visualisations(cleaned, measurement_cols, cat_cols, root)

    zip_path = step_zip(root) if make_zip else None
    elapsed = (datetime.now(timezone.utc) - started).total_seconds()
    summary = {
        "status": "completed",
        "elapsed_seconds": round(elapsed, 1),
        "dataset": str(resolved),
        "rows_raw": len(raw),
        "rows_cleaned": len(cleaned),
        "files_generated": sorted(set(GENERATED_FILES)),
        "n_files": len(set(GENERATED_FILES)),
        "zip": str(zip_path) if zip_path else None,
        "environment": env,
        "regression_equation": regression_result["equation"],
    }
    LOGGER.info("=" * 72)
    LOGGER.info("DONE in %.1fs - %d files generated", elapsed, summary["n_files"])
    for file in summary["files_generated"]:
        LOGGER.info("  %s", file)
    LOGGER.info("=" * 72)
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Experiment 3 (EDA) on a CSV dataset.",
        epilog="Example: python src/run_eda.py --data data/raw/penguins.csv --output outputs",
    )
    parser.add_argument("--data", default=None, help="Path to the CSV dataset (default: data/raw/penguins.csv)")
    parser.add_argument("--output", default="outputs", help="Output folder name (relative to project root)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for the synthetic demonstrations")
    parser.add_argument("--x-col", default="flipper_length_mm", help="Predictor column for the regression")
    parser.add_argument("--y-col", default="body_mass_g", help="Target column for the regression")
    parser.add_argument("--test-size", type=float, default=0.25, help="Test fraction for the train/test split")
    parser.add_argument("--random-state", type=int, default=42, help="Random state of the train/test split")
    parser.add_argument("--no-zip", action="store_true", help="Skip creation of the output ZIP archive")
    parser.add_argument("--quiet", action="store_true", help="Only log to file, not to the console")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        run_all(
            data_path=args.data,
            output_root=args.output,
            seed=args.seed,
            x_col=args.x_col,
            y_col=args.y_col,
            test_size=args.test_size,
            random_state=args.random_state,
            make_zip=not args.no_zip,
            verbose=not args.quiet,
        )
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
