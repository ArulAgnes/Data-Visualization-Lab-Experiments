"""Build ``EXPERIMENT 3.ipynb`` programmatically (chunk 1 of 3).

The notebook and ``src/run_eda.py`` share the same core logic (the ``src/``
package), so the two can never drift apart.  Regenerate the notebook with:

    python src/build_notebook.py
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "EXPERIMENT 3.ipynb"

cells: list[tuple[str, str]] = []


def md(text: str) -> None:
    cells.append(("markdown", text.strip() + "\n"))


def code(text: str) -> None:
    cells.append(("code", text.strip() + "\n"))


def build() -> "nbf.NotebookNode":
    """Turn the collected cells into an nbformat notebook."""
    notebook = nbf.v4.new_notebook()
    notebook.metadata.update(
        {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11"},
            "colab": {"provenance": [], "name": "EXPERIMENT 3.ipynb"},
        }
    )
    notebook.cells = [
        nbf.v4.new_markdown_cell(src) if kind == "markdown" else nbf.v4.new_code_cell(src)
        for kind, src in cells
    ]
    # every generated code cell must be valid Python before we save anything
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type == "code":
            try:
                compile(cell.source, f"<cell {index}>", "exec")
            except SyntaxError as exc:  # pragma: no cover - build-time guard
                raise SyntaxError(f"Generated code cell {index} is invalid: {exc}") from exc
    return notebook


# ===========================================================================
# 1. Title and objectives
# ===========================================================================
md(
    """
# EXPERIMENT 3 - Exploratory Data Analysis Through Statistical Visualization
### of Distributions, Relationships, Correlations, and Outliers

**Aim:** perform a complete, reproducible Exploratory Data Analysis (EDA) on a
real-world dataset using statistical visualizations.

**Objectives**

1. Load, inspect and document a real-world dataset.
2. Detect and clean quality problems (missing values, duplicates, impossible values).
3. Visualise and interpret the **five** canonical distribution shapes.
4. Analyse relationships between variables with scatter plots.
5. Compute Pearson's correlation coefficient (by library **and** by formula),
   build a correlation matrix and a heatmap.
6. Fit and evaluate a simple linear regression model.
7. Detect outliers with the Interquartile-Range (IQR) rule and box plots.
8. Produce additional statistical visualizations (pair plot, violin plots,
   Q-Q plots, count plots, bar charts).
9. Document findings, limitations and answers to common viva questions.

**Main dataset:** Palmer Penguins (real observations, documented source below).
Synthetic data is used **only** where a pattern cannot be demonstrated with the
real dataset, and every such use is clearly labelled.

**How to run:** *Runtime -> Run all* (Google Colab) or open in Jupyter and run
top-to-bottom. The notebook detects Google Colab, Kaggle and local Python by
itself and needs no manual path changes.
"""
)

# ===========================================================================
# 2. Environment setup
# ===========================================================================
code(
    """
# ============================================================
# 0. ENVIRONMENT SETUP  (local Python / Google Colab / Kaggle)
# ============================================================
import importlib.util
import os
import subprocess
import sys
import zipfile
from pathlib import Path

# --- detect where this notebook is running -------------------
try:
    import google.colab  # type: ignore  # noqa: F401
    IS_COLAB = True
except Exception:
    IS_COLAB = False

IS_KAGGLE = Path("/kaggle/input").exists() or os.environ.get("KAGGLE_KERNEL_RUN_TYPE") is not None
IS_LOCAL = not (IS_COLAB or IS_KAGGLE)
ENV_NAME = "Google Colab" if IS_COLAB else ("Kaggle" if IS_KAGGLE else "Local Python")

print(f"Environment  : {ENV_NAME}")
print(f"Python       : {sys.version.split()[0]}")
print(f"Working dir  : {Path.cwd()}")

# --- install only missing libraries (Google Colab convenience) ---
REQUIRED = ["pandas", "numpy", "matplotlib", "seaborn", "scipy", "sklearn"]
missing = [m for m in REQUIRED if importlib.util.find_spec(m) is None]
if missing:
    print("Missing libraries:", missing)
    if IS_COLAB:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
                               "pandas", "numpy", "matplotlib", "seaborn",
                               "scipy", "scikit-learn"])
        print("Libraries installed.")
    else:
        print("Install them with:  pip install -r requirements.txt")
else:
    print("All required libraries are already installed.")
"""
)

code(
    """
# --- locate the project folder (works on any machine / Colab / Kaggle) ---
def find_project_root(start=None):
    start = Path(start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / "src").is_dir() and (candidate / "data").is_dir():
            return candidate
    return start

ROOT = find_project_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- Google Colab: no project files yet? upload the project ZIP or a CSV ---
if IS_COLAB and not (ROOT / "src").is_dir():
    from google.colab import files  # type: ignore
    print("No project files found. Upload the project ZIP (eda_experiment3_outputs.zip)")
    print("or at least the dataset CSV (e.g. penguins.csv):")
    uploaded = files.upload()
    for name, content in uploaded.items():
        Path(name).write_bytes(content)
        if name.lower().endswith(".zip"):
            with zipfile.ZipFile(name) as zf:
                zf.extractall("/content")
    ROOT = find_project_root()
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

# --- create every output directory (idempotent) ---------------
for sub in ["data/raw", "data/processed", "outputs/plots", "outputs/reports", "outputs/logs"]:
    (ROOT / sub).mkdir(parents=True, exist_ok=True)

print("Project root  :", ROOT)
print("Dataset folder:", ROOT / "data" / "raw")
"""
)

md(
    """
## 2. Dataset source and description

**Palmer Penguins** - measurements collected at Palmer Station, Antarctica
(Gorman, Williams & Fraser, 2014), packaged by Dr. Allison Horst
(`palmerpenguins` R package, **CC0 1.0** public-domain dedication).

| Column | Type | Meaning |
|---|---|---|
| `species` | categorical | Adelie, Chinstrap or Gentoo penguin |
| `island` | categorical | Torgersen, Biscoe or Dream island |
| `bill_length_mm` | numerical | length of the bill (mm) |
| `bill_depth_mm` | numerical | depth of the bill (mm) |
| `flipper_length_mm` | numerical | length of the flipper (mm) |
| `body_mass_g` | numerical | body mass (g) |
| `sex` | categorical | male / female (some missing) |
| `year` | ordinal | 2007, 2008 or 2009 |

* Local source file: `data/raw/penguins.csv`
* Download URL: `https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv`
* Citation: Gorman KB, Williams TD, Fraser WR (2014), *PLoS ONE* 9(3): e109091,
  DOI 10.1371/journal.pone.0109091
* 344 rows x 8 columns with real missing values - ideal for a realistic EDA.
"""
)

code(
    """
# ============================================================
# 1. LIBRARIES AND CONFIGURATION
# ============================================================
import json
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from src import data_cleaning, correlation_analysis, distribution_analysis
from src import outlier_analysis, regression_analysis, relationship_analysis
from src.data_loader import (
    describe_environment, find_kaggle_input, initial_inspection,
    kaggle_credentials_available, list_columns, load_dataset,
    missing_report, resolve_dataset_path,
)
from src.visualization import apply_style, save_figure, subplots

apply_style()

SEED = 42                       # fixed seed -> fully reproducible results
np.random.seed(SEED)
DATASET_PATH = None             # e.g. "data/raw/penguins.csv" (None = auto-detect)
KAGGLE_DATASET_SLUG = ""        # e.g. "owner/penguins" when running on Kaggle
X_COL, Y_COL = "flipper_length_mm", "body_mass_g"     # regression pair
TEST_SIZE, RANDOM_STATE = 0.25, 42

print(json.dumps(describe_environment(), indent=2))
print("Kaggle credentials available:", kaggle_credentials_available(),
      "(token values are never displayed)")
"""
)

# ===========================================================================
# 3. Loading and initial inspection
# ===========================================================================
md(
    """
## 3. Dataset loading

The loader resolves the dataset in a fixed order: explicit path ->
environment variable `EDA_DATASET_PATH` -> `data/raw/penguins.csv` -> a mounted
Kaggle dataset (`/kaggle/input`) -> an interactive upload in Google Colab.
No machine-specific path is hard-coded.
"""
)
code(
    """
# Kaggle: point to a mounted dataset slug when needed (never downloads if mounted)
if IS_KAGGLE and KAGGLE_DATASET_SLUG:
    os.environ["EDA_KAGGLE_DATASET"] = KAGGLE_DATASET_SLUG
    print("Kaggle input dataset slug:", KAGGLE_DATASET_SLUG)

raw = load_dataset(DATASET_PATH, root=ROOT, allow_upload=IS_COLAB)
print("Source file :", raw.attrs.get("source_path"))
print("Dimensions  :", raw.shape, "(rows x columns)")
print()
print("First 10 rows:")
raw.head(10)
"""
)
code(
    """
print("Last 5 rows:")
raw.tail(5)
"""
)
code(
    """
print("Column names      :", list(raw.columns))
print()
print("Data types:")
print(raw.dtypes)
print()
print("Unique values per column:")
print(raw.nunique(dropna=True))
print()
print("Duplicate rows    :", int(raw.duplicated().sum()))
print("Total missing     :", int(raw.isna().sum().sum()))
info = initial_inspection(raw)
print("Memory usage (MB) :", info["memory_mb"])
"""
)

# ===========================================================================
# 4. Data-quality analysis
# ===========================================================================
md(
    """
## 4. Data-quality analysis

Before any analysis we check: missing values, duplicate rows, constant columns,
suspicious or impossible values, and categorical inconsistencies such as
accidental whitespace (`"male "` would silently become a third sex category).
"""
)
code(
    """
missing = missing_report(raw)
print("Missing values per column:")
display(missing)
print()
print("Total missing values :", int(raw.isna().sum().sum()))
print("Duplicate rows       :", int(raw.duplicated().sum()))
print("Rows x Columns       :", raw.shape)
"""
)
code(
    """
print("Numerical summary statistics:")
display(raw.describe().T)
"""
)
code(
    """
print("Categorical summary statistics:")
display(raw.describe(include="all").T)
"""
)
code(
    """
# --- data-quality checks with the shared cleaning module ---
from src.data_cleaning import (
    check_numeric_ranges, find_constant_columns, find_duplicate_rows,
    strip_categorical_whitespace,
)

VALID_RANGES = {
    "bill_length_mm": (25.0, 70.0),
    "bill_depth_mm": (10.0, 25.0),
    "flipper_length_mm": (150.0, 250.0),
    "body_mass_g": (2000.0, 7000.0),
    "year": (2007, 2009),
}
POSITIVE_COLUMNS = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

print("Constant columns         :", find_constant_columns(raw) or "none")
print("Duplicate rows           :", len(find_duplicate_rows(raw)))
_trimmed, changed = strip_categorical_whitespace(raw)
print("Columns needing trimming :", changed or "none")
print("Impossible-value findings:", check_numeric_ranges(raw, VALID_RANGES, POSITIVE_COLUMNS))
"""
)

md(
    """
## 5. Data cleaning

Every rule below is recorded in `outputs/reports/data_cleaning_report.json`:

1. strip whitespace from categorical values,
2. remove exact duplicate rows (only if any exist),
3. **drop** rows whose *every* measurement column is missing - such rows carry
   no measurable information (documented justification),
4. fill remaining categorical missing values with the label `Unknown` so the
   rows are kept and the missingness stays visible,
5. numerical missing values are **never** imputed silently,
6. impossible values are **flagged, not deleted**,
7. the raw file is never overwritten - the cleaned table is saved separately.
"""
)
code(
    """
cleaned, cleaning_report = data_cleaning.clean_dataset(
    raw,
    valid_ranges=VALID_RANGES,
    positive_columns=POSITIVE_COLUMNS,
    source=str(raw.attrs.get("source_path", "in-memory dataframe")),
)
data_cleaning.print_cleaning_summary(cleaning_report)

cleaned_path = data_cleaning.save_cleaned_dataset(
    cleaned, ROOT / "data" / "processed" / "cleaned_dataset.csv")
report_path = data_cleaning.save_cleaning_report(
    cleaning_report, ROOT / "outputs" / "reports" / "data_cleaning_report.json")
print("Saved cleaned dataset ->", cleaned_path)
print("Saved cleaning report ->", report_path)
"""
)
code(
    """
print("Before-and-after comparison")
display(pd.DataFrame(cleaning_report["before_after"]))
print()
print("Rows removed    :", cleaning_report["rows_removed"])
print("Columns modified:", cleaning_report["columns_modified"])
print("Cleaning decisions:")
for decision in cleaning_report["decisions"]:
    print("  -", decision)
"""
)

# ===========================================================================
# 5. Descriptive statistics
# ===========================================================================
md(
    """
## 6. Descriptive statistics and column identification

The numerical columns drive the distribution and correlation analysis. `year`
is a low-cardinality ordinal code, so it stays in the correlation matrix (it
gives a useful *near-zero* correlation example) but is excluded from the
continuous-variable distribution and box plots.
"""
)
code(
    """
columns = list_columns(cleaned)
NUMERIC_COLS = columns["numerical"]
CAT_COLS = columns["categorical"]
MEASUREMENT_COLS = [c for c in NUMERIC_COLS if cleaned[c].nunique(dropna=True) > 10] or NUMERIC_COLS

print("Numerical columns   :", NUMERIC_COLS)
print("Measurement columns :", MEASUREMENT_COLS)
print("Categorical columns :", CAT_COLS)
print()
display(cleaned[NUMERIC_COLS].describe().T)
print()
display(cleaned[CAT_COLS].astype("string").describe())
"""
)

# ===========================================================================
# 6. Five synthetic distribution demonstrations
# ===========================================================================
md(
    """
## 7. Distribution analysis - the five canonical shapes (SYNTHETIC DATA)

These five demonstrations use **synthetic, seeded** samples so that every shape
is shown clearly. They are kept strictly separate from the real penguins
analysis that follows.
"""
)

md(
    """
### Type 1 - Gaussian / Normal distribution

Bell-shaped and symmetric: mean = median = mode, and about 68 % of the values
lie within one standard deviation of the mean.
"""
)
code(
    """
# --- Type 1: Gaussian (normal) distribution -------------------
values = distribution_analysis.make_gaussian(n=1000, mean=50, std=10, seed=SEED)
summary = distribution_analysis.summarise(values, "gaussian")

fig, ax = subplots(1, 1, (8, 5))
ax.hist(values, bins=40, density=True, alpha=0.65, edgecolor="white", label="Histogram")
sns.kdeplot(values, ax=ax, linewidth=2, label="KDE")
x_norm, y_norm = distribution_analysis.normal_reference_curve(values)
ax.plot(x_norm, y_norm, "r--", linewidth=2, label="Fitted normal curve")
ax.axvline(summary["mean"], color="black", linestyle=":", label=f"Mean = {summary['mean']:.2f}")
ax.axvline(summary["median"], color="green", linestyle="-.", label=f"Median = {summary['median']:.2f}")
ax.set_title("Type 1 - Gaussian (Normal) Distribution (synthetic)")
ax.set_xlabel("Value")
ax.set_ylabel("Density")
ax.legend()
save_figure(fig, "distribution_gaussian", root=ROOT)
plt.show()

print(f"n = {summary['n']}, mean = {summary['mean']:.3f}, median = {summary['median']:.3f}, "
      f"std = {summary['std']:.3f}, skewness = {summary['skewness']:.3f}, "
      f"excess kurtosis = {summary['kurtosis']:.3f}")
"""
)
md(
    """
**Interpretation:** the histogram and the KDE form the classic symmetric bell.
The mean (~50.0) and the median (~50.1) are almost identical and the skewness is
~0, so both sides of the peak balance. The red dashed curve is the theoretical
normal density fitted to the sample and it tracks the bars closely.
"""
)

md("### Type 2 - Uniform distribution\n\nEvery value inside the interval is equally likely -> a flat histogram.")
code(
    """
# --- Type 2: Uniform distribution -----------------------------
values = distribution_analysis.make_uniform(n=1000, low=0, high=100, seed=SEED)
summary = distribution_analysis.summarise(values, "uniform")

fig, ax = subplots(1, 1, (8, 5))
ax.hist(values, bins=25, density=True, alpha=0.65, color="#55a868", edgecolor="white", label="Histogram")
sns.kdeplot(values, ax=ax, linewidth=2, color="black", label="KDE")
ax.axhline(1 / 100, color="red", linestyle="--", label="Theoretical density 1/(b-a) = 0.01")
ax.set_title("Type 2 - Uniform Distribution (synthetic)")
ax.set_xlabel("Value")
ax.set_ylabel("Density")
ax.legend()
save_figure(fig, "distribution_uniform", root=ROOT)
plt.show()

print(f"n = {summary['n']}, mean = {summary['mean']:.3f}, median = {summary['median']:.3f}, "
      f"std = {summary['std']:.3f}, skewness = {summary['skewness']:.3f}")
"""
)
md(
    """
**Interpretation:** the bars are all about the same height - no region of the
interval is preferred. The theoretical density of a Uniform(0, 100) variable is
`1/(b-a) = 0.01` (red line) and the KDE oscillates around it. The mean sits in
the middle of the interval (~50) and the skewness is ~0.
"""
)

md("### Type 3 - Right-skewed (positively skewed) distribution\n\nMost observations are small; a few very large values stretch the tail to the right.")
code(
    """
# --- Type 3: Right-skewed (positive skew) ---------------------
values = distribution_analysis.make_right_skewed(n=1500, sigma=0.6, seed=SEED)
summary = distribution_analysis.summarise(values, "right_skewed")

fig, ax = subplots(1, 1, (8, 5))
ax.hist(values, bins=45, density=True, alpha=0.65, color="#c44e52", edgecolor="white", label="Histogram")
sns.kdeplot(values, ax=ax, linewidth=2, color="black", label="KDE")
ax.axvline(summary["mean"], color="red", linestyle="--", label=f"Mean = {summary['mean']:.2f}")
ax.axvline(summary["median"], color="green", linestyle="-.", label=f"Median = {summary['median']:.2f}")
ax.set_title("Type 3 - Right-Skewed (Positive) Distribution (synthetic log-normal)")
ax.set_xlabel("Value")
ax.set_ylabel("Density")
ax.legend()
save_figure(fig, "distribution_right_skewed", root=ROOT)
plt.show()

print(f"n = {summary['n']}, mean = {summary['mean']:.3f}, median = {summary['median']:.3f}, "
      f"std = {summary['std']:.3f}, skewness = {summary['skewness']:.3f}")
print("Mean > median is the signature of a right-skewed distribution.")
"""
)
md(
    """
**Interpretation:** the bulk of the data is on the left while a long tail
stretches to the right (typical for incomes, house prices, waiting times).
Skewness is about +2 (strong positive skew) and, as expected, **mean > median**:
the few extreme values drag the mean to the right much more than the median.
"""
)

md("### Type 4 - Left-skewed (negatively skewed) distribution\n\nMirror image of Type 3: most observations are large and a few very small values stretch the tail to the left.")
code(
    """
# --- Type 4: Left-skewed (negative skew) ----------------------
values = distribution_analysis.make_left_skewed(n=1500, sigma=0.6, seed=SEED)
summary = distribution_analysis.summarise(values, "left_skewed")

fig, ax = subplots(1, 1, (8, 5))
ax.hist(values, bins=45, density=True, alpha=0.65, color="#8172b3", edgecolor="white", label="Histogram")
sns.kdeplot(values, ax=ax, linewidth=2, color="black", label="KDE")
ax.axvline(summary["mean"], color="red", linestyle="--", label=f"Mean = {summary['mean']:.2f}")
ax.axvline(summary["median"], color="green", linestyle="-.", label=f"Median = {summary['median']:.2f}")
ax.set_title("Type 4 - Left-Skewed (Negative) Distribution (synthetic mirror example)")
ax.set_xlabel("Value")
ax.set_ylabel("Density")
ax.legend()
save_figure(fig, "distribution_left_skewed", root=ROOT)
plt.show()

print(f"n = {summary['n']}, mean = {summary['mean']:.3f}, median = {summary['median']:.3f}, "
      f"std = {summary['std']:.3f}, skewness = {summary['skewness']:.3f}")
print("Mean < median is the signature of a left-skewed distribution.")
"""
)
md(
    """
**Interpretation:** the tail now stretches to the left. Skewness is about -2
(strong negative skew) and **mean < median**. A typical real example is the mark
distribution of a very easy exam, where most students score high and only a few
score low.
"""
)

md("### Type 5 - Bimodal distribution\n\nTwo peaks usually reveal two hidden sub-groups inside one dataset.")
code(
    """
# --- Type 5: Bimodal distribution -----------------------------
values, labels = distribution_analysis.make_bimodal(n=1600, mean_a=40, std_a=6,
                                                   mean_b=70, std_b=6, seed=SEED)
summary = distribution_analysis.summarise(values, "bimodal")

fig, ax = subplots(1, 1, (8, 5))
for label, colour in (("group_A", "#4c72b0"), ("group_B", "#c44e52")):
    subset = values[labels == label]
    ax.hist(subset, bins=40, density=True, alpha=0.5, color=colour, edgecolor="white",
            label=f"{label} (mean={subset.mean():.1f})")
sns.kdeplot(values, ax=ax, linewidth=2, color="black", label="KDE of the combined data")
ax.axvline(summary["mean"], color="green", linestyle="-.", label=f"Combined mean = {summary['mean']:.1f}")
ax.set_title("Type 5 - Bimodal Distribution (two overlapping groups, synthetic)")
ax.set_xlabel("Value")
ax.set_ylabel("Density")
ax.legend()
save_figure(fig, "distribution_bimodal", root=ROOT)
plt.show()

density, _edges = np.histogram(values, bins=50, density=True)
peaks = int(np.sum((density[1:-1] > density[:-2]) & (density[1:-1] > density[2:])))
print(f"n = {summary['n']}, mean = {summary['mean']:.3f}, median = {summary['median']:.3f}, "
      f"skewness = {summary['skewness']:.3f}")
print(f"Local maxima in the combined histogram: {peaks} (two = bimodal)")
"""
)
md(
    """
**Interpretation:** each coloured group is a normal distribution by itself, but
their mixture produces **two clear peaks**. The overall mean (~55) falls into the
valley between the peaks where hardly any observation lies - a good reminder that
one average can describe such data poorly. In real datasets a bimodal shape
suggests splitting by a hidden factor (species, gender, customer segment).
"""
)

# ===========================================================================
# 7. Dataset distribution analysis
# ===========================================================================
md(
    """
## 8. Distribution analysis of the REAL dataset

The same tools are now applied to the penguins measurements (cleaned data).
"""
)
code(
    """
dist_summary = distribution_analysis.dataset_distribution_summary(cleaned, MEASUREMENT_COLS)
display(dist_summary)
dist_summary.round(4).to_csv(ROOT / "outputs" / "reports" / "dataset_distribution_summary.csv", index=False)
print("Saved ->", ROOT / "outputs" / "reports" / "dataset_distribution_summary.csv")
"""
)
code(
    """
# --- histograms + KDE for every measurement column -------------
n = len(MEASUREMENT_COLS)
ncols, nrows = 2, int(np.ceil(n / 2))
fig, axes = subplots(nrows, ncols, figsize=(6 * ncols, 4 * nrows))
axes = np.atleast_1d(axes).ravel()
for ax, col in zip(axes, MEASUREMENT_COLS):
    sns.histplot(cleaned[col].dropna(), bins=30, kde=True, ax=ax, color="#4c72b0")
    row = dist_summary[dist_summary["variable"] == col].iloc[0]
    ax.set_title(f"{col}\\nmean={row['mean']:.2f}, median={row['median']:.2f}, skew={row['skewness']:.2f}")
    ax.set_xlabel(col)
    ax.set_ylabel("Count")
for ax in axes[n:]:
    ax.axis("off")
fig.suptitle("Distribution of the penguin measurements (real data)", fontsize=14)
save_figure(fig, "dataset_distributions", root=ROOT)
plt.show()
"""
)
code(
    """
# --- Q-Q plots: how close is each variable to a normal shape? ---
fig, axes = subplots(nrows, ncols, figsize=(6 * ncols, 4 * nrows))
axes = np.atleast_1d(axes).ravel()
for ax, col in zip(axes, MEASUREMENT_COLS):
    stats.probplot(cleaned[col].dropna(), dist="norm", plot=ax)
    ax.set_title(f"Q-Q plot: {col}")
    ax.get_lines()[0].set(marker="o", markersize=2.5, alpha=0.6)
    ax.get_lines()[1].set(color="red", linewidth=1.5)
for ax in axes[n:]:
    ax.axis("off")
fig.suptitle("Q-Q plots - points close to the red line indicate approximate normality", fontsize=14)
save_figure(fig, "dataset_qq_plots", root=ROOT)
plt.show()
"""
)
md(
    """
**Interpretation:** all four measurements are **approximately symmetric**
(|skewness| < 0.5). Body mass has the largest skew (~0.47) with a small right
tail; bill depth is slightly left-skewed (~-0.14). In the Q-Q plots the points
follow the red line through the middle and bend a little at the ends (slightly
lighter tails than a perfect normal distribution) - completely normal for real
biological measurements.
"""
)

# ===========================================================================
# 8. Relationship analysis
# ===========================================================================
md(
    """
## 9. Relationship analysis - seven correlation patterns

Patterns that do **not all exist** in the penguins data (e.g. perfect
correlation) are shown with clearly labelled synthetic, seeded samples. Every
plot prints its own Pearson coefficient, computed from the plotted points.
"""
)
code(
    """
# --- strong positive & strong negative (synthetic) --------------
specs = [
    ("correlation_strong_positive", "strong_positive", "Strong positive correlation"),
    ("correlation_strong_negative", "strong_negative", "Strong negative correlation"),
]
demo_rows = []
for filename, demo_name, title in specs:
    frame = relationship_analysis.make_demo(demo_name, seed=SEED)
    r = float(stats.pearsonr(frame["x"], frame["y"]).statistic)
    demo_rows.append({"demo": demo_name, "n": len(frame), "pearson_r": round(r, 4)})
    fig, ax = subplots(1, 1, (7, 5))
    ax.scatter(frame["x"], frame["y"], s=30, alpha=0.75, edgecolor="white", linewidth=0.4)
    ax.set_title(f"{title}\\nPearson r = {r:.3f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    save_figure(fig, filename, root=ROOT)
    plt.show()
    print(f"{demo_name}: r = {r:.3f}  (n = {len(frame)})")
"""
)
code(
    """
# --- weak positive & weak negative (synthetic) ------------------
specs = [
    ("correlation_weak_positive", "weak_positive", "Weak positive correlation"),
    ("correlation_weak_negative", "weak_negative", "Weak negative correlation"),
]
for filename, demo_name, title in specs:
    frame = relationship_analysis.make_demo(demo_name, seed=SEED)
    r = float(stats.pearsonr(frame["x"], frame["y"]).statistic)
    demo_rows.append({"demo": demo_name, "n": len(frame), "pearson_r": round(r, 4)})
    fig, ax = subplots(1, 1, (7, 5))
    ax.scatter(frame["x"], frame["y"], s=30, alpha=0.75, color="#dd8452", edgecolor="white", linewidth=0.4)
    ax.set_title(f"{title}\\nPearson r = {r:.3f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    save_figure(fig, filename, root=ROOT)
    plt.show()
    print(f"{demo_name}: r = {r:.3f}  (n = {len(frame)})")
"""
)
md(
    """
**Interpretation:** the strong demos produce a tight band around a straight line
(|r| ~ 0.95). In the weak demos the point cloud is almost round with only a
slight tilt (|r| ~ 0.30). "Weak" means the linear link exists but explains very
little of the variation (r-squared ~ 0.09, i.e. only ~9 %).
"""
)
code(
    """
# --- no linear correlation: independent noise AND a parabola -----
independent = relationship_analysis.demo_no_linear(seed=SEED)
parabola = relationship_analysis.demo_nonlinear_parabola(seed=SEED)
r_ind = float(stats.pearsonr(independent["x"], independent["y"]).statistic)
r_par = float(stats.pearsonr(parabola["x"], parabola["y"]).statistic)
demo_rows += [
    {"demo": "no_linear_independent", "n": len(independent), "pearson_r": round(r_ind, 4)},
    {"demo": "no_linear_parabola", "n": len(parabola), "pearson_r": round(r_par, 4)},
]

fig, (ax1, ax2) = subplots(1, 2, figsize=(12, 5))
ax1.scatter(independent["x"], independent["y"], s=28, alpha=0.75, color="#55a868", edgecolor="white")
ax1.set_title(f"Independent x and y\\nPearson r = {r_ind:.3f}")
ax1.set_xlabel("x"); ax1.set_ylabel("y")
ax2.scatter(parabola["x"], parabola["y"], s=28, alpha=0.75, color="#c44e52", edgecolor="white")
ax2.set_title(f"Perfect parabola y = x^2 (+ tiny noise)\\nPearson r = {r_par:.3f}")
ax2.set_xlabel("x"); ax2.set_ylabel("y")
fig.suptitle("r near 0 does NOT mean 'no relationship' - only 'no LINEAR relationship'", fontsize=13)
save_figure(fig, "correlation_no_linear", root=ROOT)
plt.show()
print(f"independent: r = {r_ind:.3f} | parabola: r = {r_par:.3f}")
"""
)
md(
    """
**Interpretation:** the left panel has no structure at all (r ~ 0). The right
panel follows the exact curve y = x-squared - a **perfect non-linear
relationship** - yet Pearson's r is still ~0, because the rising and falling
halves cancel each other out. Lesson: **r = 0 means "no linear association"**,
not "no association" and not statistical independence.
"""
)
code(
    """
# --- perfect positive & perfect negative (exact maths, no noise) -
for filename, demo_name, title in [
    ("correlation_perfect_positive", "perfect_positive", "Perfect positive linear correlation"),
    ("correlation_perfect_negative", "perfect_negative", "Perfect negative linear correlation"),
]:
    frame = relationship_analysis.make_demo(demo_name)
    r = float(stats.pearsonr(frame["x"], frame["y"]).statistic)
    demo_rows.append({"demo": demo_name, "n": len(frame), "pearson_r": round(r, 4)})
    slope = np.polyfit(frame["x"], frame["y"], 1)
    fig, ax = subplots(1, 1, (7, 5))
    ax.scatter(frame["x"], frame["y"], s=35, color="#4c72b0", edgecolor="white", label="Points")
    ax.plot(frame["x"], np.polyval(slope, frame["x"]), "r--", linewidth=2,
            label=f"y = {slope[0]:.1f}x + {slope[1]:.1f}")
    ax.set_title(f"{title}\\nPearson r = {r:.1f}")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend()
    save_figure(fig, filename, root=ROOT)
    plt.show()
    print(f"{demo_name}: r = {r:.12f} (mathematically {'+1' if r > 0 else '-1'})")

demo_table = pd.DataFrame(demo_rows)
display(demo_table)
demo_table.to_csv(ROOT / "outputs" / "reports" / "correlation_demo_summary.csv", index=False)
print("Saved ->", ROOT / "outputs" / "reports" / "correlation_demo_summary.csv")
"""
)
md(
    """
**Interpretation:** without noise every point lies exactly on the fitted line, so
r = +1 (upward line) or r = -1 (downward line). These are mathematical ideals -
real measurements always contain some scatter.
"""
)

md(
    """
### Relationship patterns found in the REAL dataset

Only patterns that the computed coefficients actually support are described.
"""
)
code(
    """
# --- real dataset scatter plots --------------------------------
real_pairs = [
    ("flipper_length_mm", "body_mass_g"),
    ("bill_length_mm", "flipper_length_mm"),
    ("bill_depth_mm", "flipper_length_mm"),
    ("year", "body_mass_g"),
]
pair_results = []
for x_col, y_col in real_pairs:
    pair = relationship_analysis.real_pair(cleaned, x_col, y_col)
    entry = correlation_analysis.pearson_pair(pair["x"], pair["y"])
    pair_results.append({
        "pair": f"{x_col} ~ {y_col}", "n": entry["n_valid"],
        "pearson_r": round(entry["pearson_r"], 4), "p_value": entry["p_value"],
        "direction": entry["direction"], "strength": entry["strength"],
        "significant_at_0.05": entry["significant_at_alpha"],
    })
    fig, ax = subplots(1, 1, (7, 5))
    for spec, sub in pair.groupby(cleaned.loc[pair.index, "species"]):
        ax.scatter(sub["x"], sub["y"], s=30, alpha=0.8, label=spec, edgecolor="white")
    ax.set_title(f"{x_col} vs {y_col}\\nr = {entry['pearson_r']:.3f} "
                 f"({entry['strength']} {entry['direction']}), p = {entry['p_value']:.2g}, "
                 f"n = {entry['n_valid']}")
    ax.set_xlabel(x_col); ax.set_ylabel(y_col); ax.legend(title="species")
    save_figure(fig, f"real_scatter_{x_col}_vs_{y_col}", root=ROOT)
    plt.show()

pair_table = pd.DataFrame(pair_results)
display(pair_table)
"""
)
md(
    """
**Interpretation (real data):**

* `flipper_length_mm ~ body_mass_g`: **strong positive** (r ~ 0.87) - longer
  flippers belong to heavier penguins.
* `bill_length_mm ~ flipper_length_mm`: **moderate positive** (r ~ 0.66).
* `bill_depth_mm ~ flipper_length_mm`: **moderate negative** (r ~ -0.58) in the
  pooled data. Colouring by species shows why - see the findings section.
* `year ~ body_mass_g`: **no linear correlation** (r ~ 0.04, p ~ 0.44 > 0.05).
"""
)

# ===========================================================================
# 9. Pearson correlation
# ===========================================================================
md(
    """
## 10. Pearson correlation coefficient - formula and calculation

```
             sum((x - mean(x)) * (y - mean(y)))
r = ----------------------------------------------------------------
    sqrt( sum((x - mean(x))**2) * sum((y - mean(y))**2) )
```

r always lies in [-1, +1]. It is computed here **four** ways: by hand with
NumPy, with `scipy.stats.pearsonr`, `numpy.corrcoef` and
`pandas.DataFrame.corr(method="pearson")`.
"""
)
code(
    """
# --- teaching example: manual formula vs libraries --------------
x = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
y = np.array([1.0, 3.0, 5.0, 7.0, 9.0])

dx, dy = x - x.mean(), y - y.mean()
r_manual = np.sum(dx * dy) / np.sqrt(np.sum(dx ** 2) * np.sum(dy ** 2))

comparison = correlation_analysis.pearson_all_methods(x, y)
print("x =", x.tolist())
print("y =", y.tolist())
print()
print("Manual formula     :", r_manual)
print("scipy.stats.pearsonr:", comparison["scipy.stats.pearsonr"])
print("numpy.corrcoef      :", comparison["numpy.corrcoef"])
print("pandas .corr()      :", comparison["pandas.DataFrame.corr"])
print("Max difference      :", comparison["max_absolute_difference"])
assert comparison["max_absolute_difference"] < 1e-12
print()
print("All four methods agree - the manual formula is exactly what the libraries compute.")

import json as _json
(ROOT / "outputs" / "reports" / "pearson_formula_example.json").write_text(
    _json.dumps({"x": x.tolist(), "y": y.tolist(), **comparison}, indent=2), encoding="utf-8")
print("Saved ->", ROOT / "outputs" / "reports" / "pearson_formula_example.json")
"""
)

md(
    """
## 11. Correlation matrix and heatmap

Missing values are dropped **pairwise** (every pair uses all rows where both
variables are present). The colour scale is diverging and centred at zero.
"""
)
code(
    """
matrix = correlation_analysis.pearson_matrix(cleaned, NUMERIC_COLS)
n_table = correlation_analysis.pairwise_n(cleaned, NUMERIC_COLS)

print("Pearson correlation matrix:")
display(matrix.round(2))
print("Complete observations behind every cell:")
display(n_table)

matrix.round(4).to_csv(ROOT / "outputs" / "reports" / "pearson_correlation_matrix.csv")
print("Saved ->", ROOT / "outputs" / "reports" / "pearson_correlation_matrix.csv")
"""
)
code(
    """
fig, ax = subplots(1, 1, (9, 7))
sns.heatmap(matrix, annot=True, fmt=".2f", cmap="RdBu_r", center=0.0, vmin=-1, vmax=1,
            square=True, linewidths=0.5, cbar_kws={"label": "Pearson r"}, ax=ax)
ax.set_title("Pearson correlation matrix (annotated, diverging scale centred at 0)")
save_figure(fig, "pearson_correlation_heatmap", root=ROOT)
plt.show()
"""
)
code(
    """
# --- selected pairs: r, p-value, n, direction, strength, significance ---
pair_details = []
for a, b in [("flipper_length_mm", "body_mass_g"),
             ("bill_depth_mm", "flipper_length_mm"),
             ("bill_length_mm", "body_mass_g"),
             ("year", "body_mass_g")]:
    entry = correlation_analysis.pearson_pair(cleaned[a], cleaned[b], alpha=0.05)
    print(correlation_analysis.interpretation(entry, a, b))
    print()
    pair_details.append({"x": a, "y": b, **{k: entry[k] for k in
                        ("n_valid", "pearson_r", "p_value", "direction", "strength",
                         "significant_at_alpha", "ci95_low", "ci95_high")}})
display(pd.DataFrame(pair_details))
"""
)
md(
    """
**Important caveats**

* Pearson's r measures only **linear** association (see the parabola counter-example).
* A small p-value means "unlikely to be a pure sampling accident" - it is **not**
  proof of causation.
* The strength categories (very strong / strong / ...) are configurable rules of
  thumb, not universal scientific laws.
* r is sensitive to outliers and assumes roughly continuous variables; the
  p-value additionally assumes approximate bivariate normality.
"""
)

# ===========================================================================
# 10. Linear regression
# ===========================================================================
md(
    """
## 12. Simple linear regression

`y_hat = b0 + b1 * x` - predict body mass from flipper length.

The model is fitted **only on the training split** (75 %, `random_state = 42`)
and evaluated on the held-out 25 %, so the reported test metrics are honest
out-of-sample estimates. `scipy.stats.linregress` gives an independent
statistical cross-check.
"""
)
code(
    """
result = regression_analysis.fit_simple_regression(cleaned, X_COL, Y_COL,
                                                   test_size=TEST_SIZE,
                                                   random_state=RANDOM_STATE)
print("Equation             :", result["equation"])
print("Intercept  (b0)      :", round(result["intercept"], 4))
print("Slope      (b1)      :", round(result["slope"], 4))
print("Pearson r            :", round(result["pearson_r"], 4))
print("R^2 (from r)         :", round(result["pearson_r"] ** 2, 4))
print("R^2 on training data :", round(result["r_squared_train"], 4))
print("Split                :", result["split_note"])
print()
print("scipy.stats.linregress (all complete rows):",
      "slope =", round(result["scipy_slope"], 4),
      "| intercept =", round(result["scipy_intercept"], 4),
      "| r =", round(result["scipy_rvalue"], 4),
      "| p =", f"{result['scipy_pvalue']:.3g}",
      "| stderr(slope) =", round(result["scipy_stderr"], 4))
print()
print("TEST-set metrics  :", {k: round(v, 3) for k, v in result["metrics_test"].items()})
print("Full-data metrics :", {k: round(v, 3) for k, v in result["metrics_full"].items()})
"""
)
md(
    """
**Reading the numbers**

* slope b1 ~ 49.5 -> every extra millimetre of flipper length is associated with
  about **49.5 g** more body mass.
* intercept b0 ~ -5741 -> a penguin with a 0 mm flipper does not exist, so the
  intercept only anchors the line; it has no physical meaning here.
* r ~ 0.871 and R-squared = r-squared ~ 0.76 -> about **76 %** of the variation
  in body mass is explained by flipper length (linearly - not causally!).

Note the difference: the **slope** (49.5 g/mm) is a rate of change, **r**
dimensionless strength of linear association, and **R-squared** the explained
variance share. They are related but not interchangeable.
"""
)
code(
    """
# --- plot 1: data + fitted regression line ---------------------
data = result["data"]
fig, ax = subplots(1, 1, (8, 6))
ax.scatter(data[X_COL], data[Y_COL], s=28, alpha=0.6, color="#4c72b0", label="Observations")
x_line = np.linspace(data[X_COL].min(), data[X_COL].max(), 100).reshape(-1, 1)
ax.plot(x_line, result["model"].predict(x_line), color="red", linewidth=2,
        label=f"Fit: {result['equation']}")
ax.set_title(f"Simple linear regression: {Y_COL} ~ {X_COL}\\nr = {result['pearson_r']:.3f}, "
             f"R2 = {result['pearson_r'] ** 2:.3f}")
ax.set_xlabel(X_COL); ax.set_ylabel(Y_COL); ax.legend()
save_figure(fig, "linear_regression_fit", root=ROOT)
plt.show()
"""
)
code(
    """
# --- plot 2: actual vs predicted (TEST set) --------------------
fig, ax = subplots(1, 1, (7, 6))
ax.scatter(result["y_test"], result["y_pred_test"], s=32, alpha=0.75, color="#55a868")
lo = min(result["y_test"].min(), result["y_pred_test"].min())
hi = max(result["y_test"].max(), result["y_pred_test"].max())
ax.plot([lo, hi], [lo, hi], "r--", linewidth=1.5, label="Perfect prediction line")
m = result["metrics_test"]
ax.set_title(f"Actual vs predicted ({Y_COL}, TEST set, n={m['n']})\\n"
             f"MAE = {m['MAE']:.1f} g | RMSE = {m['RMSE']:.1f} g | R2 = {m['R2']:.3f}")
ax.set_xlabel("Actual values (g)"); ax.set_ylabel("Predicted values (g)"); ax.legend()
save_figure(fig, "actual_vs_predicted", root=ROOT)
plt.show()
print("These are TEST-set metrics on unseen data, not training metrics.")
"""
)
code(
    """
# --- plots 3 & 4: residual analysis ----------------------------
fig, ax = subplots(1, 1, (8, 5))
ax.scatter(result["y_pred_full"], result["residuals_full"], s=28, alpha=0.6, color="#8172b3")
ax.axhline(0, color="red", linewidth=1.5)
ax.set_title("Residual plot (residual = actual - predicted)")
ax.set_xlabel(f"Fitted values ({Y_COL}, g)"); ax.set_ylabel("Residual (g)")
save_figure(fig, "regression_residuals", root=ROOT)
plt.show()

fig, ax = subplots(1, 1, (8, 5))
ax.hist(result["residuals_full"], bins=30, density=True, alpha=0.7,
        color="#4c72b0", edgecolor="white", label="Residuals")
x_res, y_res = distribution_analysis.normal_reference_curve(result["residuals_full"])
ax.plot(x_res, y_res, "r--", linewidth=2, label="Normal reference curve")
ax.axvline(0, color="black", linewidth=1)
ax.set_title("Distribution of residuals")
ax.set_xlabel("Residual (g)"); ax.set_ylabel("Density"); ax.legend()
save_figure(fig, "residual_distribution", root=ROOT)
plt.show()

res = pd.Series(result["residuals_full"])
print(f"Residuals: mean = {res.mean():.3f} (must be ~0), std = {res.std():.1f} g, "
      f"min = {res.min():.1f}, max = {res.max():.1f}")
"""
)
md(
    """
**Residual analysis:** in the residual plot the points scatter randomly around
zero with no funnel or curve, so the linear form is reasonable. The residual
histogram is roughly bell-shaped and centred at zero, which supports (but does
not prove) the normality-of-errors assumption. The classical assumptions are
linearity, independent errors, constant variance and approximately normal
residuals - none of them implies causation, and no target leakage is present
because the model only uses flipper length to predict body mass.
"""
)
code(
    """
# --- single prediction inside the observed range ---------------
example_value = float(np.median(data[X_COL]))
prediction = regression_analysis.predict_for(result, example_value)
print(json.dumps(prediction, indent=2))

payload = regression_analysis.metrics_payload(result)
payload["prediction_example"] = prediction
metrics_path = regression_analysis.save_metrics(
    payload, ROOT / "outputs" / "reports" / "regression_metrics.json")
print("Saved ->", metrics_path)
"""
)

# ===========================================================================
# 11. Outliers
# ===========================================================================
md(
    """
## 13. Outlier detection with the Interquartile Range (IQR)

```
Q1 = 25th percentile      Q3 = 75th percentile      IQR = Q3 - Q1
lower fence = Q1 - 1.5 x IQR        upper fence = Q3 + 1.5 x IQR
```

Values below the lower fence or above the upper fence are *potential* outliers.
They are **reported, never deleted automatically** - an outlier may be a data
error, a valid extreme observation or an important rare event.
"""
)
code(
    """
# --- IQR analysis of every measurement column (pooled) ----------
report_df, outlier_detail = outlier_analysis.detect_outliers(
    cleaned, MEASUREMENT_COLS, group_col="species")

outlier_analysis.print_outlier_summary(report_df, scope="overall")
overall_rows = report_df[report_df["scope"] == "overall"]
display(overall_rows)
path = outlier_analysis.save_outlier_report(
    report_df, ROOT / "outputs" / "reports" / "outlier_report.csv")
print("Saved ->", path)
"""
)
code(
    """
# --- individual box plots (one panel per variable) -------------
n = len(MEASUREMENT_COLS)
ncols, nrows = 2, int(np.ceil(n / 2))
fig, axes = subplots(nrows, ncols, figsize=(6 * ncols, 4 * nrows))
axes = np.atleast_1d(axes).ravel()
for ax, col in zip(axes, MEASUREMENT_COLS):
    sns.boxplot(y=cleaned[col], ax=ax, color="#4c72b0", width=0.45,
                flierprops=dict(marker="o", markersize=4, alpha=0.7))
    row = overall_rows[overall_rows["variable"] == col].iloc[0]
    ax.set_title(f"Box plot: {col}\\nfences ({row['lower_fence']:.1f}, {row['upper_fence']:.1f}) "
                 f"-> {row['n_outliers']} outlier(s)")
    ax.set_ylabel(col)
for ax in axes[n:]:
    ax.axis("off")
fig.suptitle("Individual box plots (dots beyond the whiskers = potential outliers)", fontsize=13)
save_figure(fig, "boxplot_outlier_detection", root=ROOT)
plt.show()
"""
)
code(
    """
# --- combined box plot on a common scale (z-scores) ------------
z = (cleaned[MEASUREMENT_COLS] - cleaned[MEASUREMENT_COLS].mean()) / cleaned[MEASUREMENT_COLS].std(ddof=1)
fig, ax = subplots(1, 1, (10, 5))
sns.boxplot(data=z, orient="h", ax=ax, color="#55a868", width=0.5)
ax.set_title("Combined box plot of all measurement columns (standardised z-scores)\\n"
             "standardisation makes columns with different units comparable")
ax.set_xlabel("z-score (standard deviations from the mean)")
save_figure(fig, "boxplot_all_numeric", root=ROOT)
plt.show()
"""
)
code(
    """
# --- grouped detection: does species change the verdict? -------
grouped_rows = report_df[report_df["scope"] == "by_species"]
display(grouped_rows[["group", "variable", "n", "lower_fence", "upper_fence",
                      "n_outliers", "percent_outliers", "outlier_values"]])
print()
print("Pooled outliers :", int(overall_rows['n_outliers'].sum()))
print("Grouped outliers:", int(grouped_rows['n_outliers'].sum()),
      "(computed inside each species separately)")
"""
)
code(
    """
# --- clearly labelled SYNTHETIC outlier demonstration -----------
synth = outlier_analysis.synthetic_outlier_example()
bounds = outlier_analysis.iqr_bounds(synth)

fig, (ax1, ax2) = subplots(1, 2, figsize=(12, 5))
sns.histplot(synth, bins=30, kde=True, ax=ax1, color="#dd8452")
ax1.set_title("Synthetic sample with injected outliers\\ninjected values: "
              + ", ".join(f"{v:g}" for v in synth.attrs["known_outliers"]))
ax1.set_xlabel("Value")
sns.boxplot(y=synth, ax=ax2, color="#dd8452", width=0.4)
ax2.axhline(bounds["lower_fence"], color="red", linestyle="--",
            label=f"lower fence {bounds['lower_fence']:.1f}")
ax2.axhline(bounds["upper_fence"], color="red", linestyle="--",
            label=f"upper fence {bounds['upper_fence']:.1f}")
ax2.set_title(f"Synthetic box plot: {bounds['n_outliers']} potential outliers detected")
ax2.legend()
save_figure(fig, "boxplot_synthetic_example", root=ROOT)
plt.show()

print({k: round(v, 3) if isinstance(v, float) else v
       for k, v in bounds.items() if k in ("q1", "q3", "iqr", "lower_fence", "upper_fence",
                                           "n_outliers", "percent_outliers", "outlier_values")})
"""
)
md(
    """
**Interpretation:** pooled across all species the IQR rule finds **no** outliers
in the real data - the fences are so wide because the three species differ a lot.
Inside individual species, however, a few points do fall outside the
species-specific fences (6 points in total). This shows that outlier detection
depends on the comparison group. The synthetic example demonstrates the
mechanics clearly: 4 injected extreme values are flagged while the bulk of the
data stays inside the fences. **No outlier was removed** from the real dataset.
"""
)

# ===========================================================================
# 12. Additional statistical visualizations
# ===========================================================================
md(
    """
## 14. Additional statistical visualizations

Pair plot, violin plots, count plots and a bar chart of a categorical summary -
each with its own code, saved PNG and interpretation.
"""
)
code(
    """
# --- pair plot (joint view of all measurement variables) --------
plot_cols = MEASUREMENT_COLS + [c for c in ("species",) if c in cleaned.columns]
pair_grid = sns.pairplot(cleaned[plot_cols].dropna(),
                         hue="species" if "species" in cleaned.columns else None,
                         diag_kind="kde")
pair_grid.figure.suptitle("Pair plot of the measurement variables (coloured by species)", y=1.02)
save_figure(pair_grid.figure, "pairplot", root=ROOT)
plt.show()
"""
)
code(
    """
# --- violin plots: distribution shape per species --------------
fig, axes = subplots(1, len(MEASUREMENT_COLS), figsize=(4.2 * len(MEASUREMENT_COLS), 5))
axes = np.atleast_1d(axes).ravel()
hue = "species" if "species" in cleaned.columns else None
for ax, col in zip(axes, MEASUREMENT_COLS):
    sns.violinplot(data=cleaned, x=hue, y=col, ax=ax, inner="quartile", palette="Set2")
    ax.set_title(col)
    ax.set_xlabel(hue or "")
    ax.tick_params(axis="x", rotation=30)
fig.suptitle("Violin plots: distribution shape of every measurement by species", fontsize=13)
save_figure(fig, "violin_by_species", root=ROOT)
plt.show()
"""
)
code(
    """
# --- count plots for the categorical columns -------------------
cats = [c for c in CAT_COLS if cleaned[c].nunique() <= 10]
fig, axes = subplots(1, len(cats), figsize=(4.5 * len(cats), 4.5))
axes = np.atleast_1d(axes).ravel()
for ax, col in zip(axes, cats):
    order = cleaned[col].value_counts().index
    sns.countplot(data=cleaned, x=col, order=order, ax=ax, hue=col, palette="Set2", legend=False)
    ax.set_title(f"Count plot: {col}")
    ax.tick_params(axis="x", rotation=30)
fig.suptitle("Frequency of the categorical values (cleaned data)", fontsize=13)
save_figure(fig, "countplots_categorical", root=ROOT)
plt.show()
"""
)
code(
    """
# --- bar chart of a categorical summary ------------------------
summary = cleaned.groupby("species")["body_mass_g"].agg(["mean", "std"]).reset_index()
fig, ax = subplots(1, 1, (8, 5))
ax.bar(summary["species"], summary["mean"], yerr=summary["std"], capsize=8,
       color=["#4c72b0", "#55a868", "#c44e52"], alpha=0.85)
ax.set_title("Mean body mass by species (error bars = +/- 1 standard deviation)")
ax.set_xlabel("Species"); ax.set_ylabel("Mean body mass (g)")
save_figure(fig, "barplot_mean_mass_by_species", root=ROOT)
plt.show()
display(summary.round(1))
"""
)
md(
    """
**Interpretation:**

* the **pair plot** shows every pairwise relationship at once; the colouring
  reveals that the three species occupy different regions of the feature space,
  which explains several pooled correlations,
* the **violin plots** show the full shape of each measurement per species -
  Gentoo penguins are clearly the heaviest with the longest flippers,
* the **count plots** show balanced sampling (species: 151/68/123; sex nearly
  equal, plus the labelled `Unknown` category created during cleaning),
* the **bar chart** summarises the same message numerically with variability
  shown by the error bars.
"""
)

# ===========================================================================
# 13. Findings, conclusion, limitations
# ===========================================================================
md(
    """
## 15. Findings and observations

The cell below recomputes every key number from the cleaned data, so the
findings always match the actual run (no hand-written numbers).
"""
)
code(
    """
# --- dynamic findings, computed from the actual results --------
print("=" * 74)
print("KEY FINDINGS (computed from the cleaned dataset)")
print("=" * 74)
print(f"Dataset                  : {raw.shape[0]} rows x {raw.shape[1]} columns (raw)")
print(f"Cleaned dataset          : {cleaned.shape[0]} rows x {cleaned.shape[1]} columns")
print(f"Rows removed by cleaning : {cleaning_report['rows_removed']['total']}")
print()
print("Distributions (real data):")
for _, row in dist_summary.iterrows():
    print(f"  {row['variable']:<20} skew={row['skewness']:+.3f} -> {row['shape']}")
print()
print("Correlations (real data):")
for _, row in pair_table.iterrows():
    print(f"  {row['pair']:<45} r={row['pearson_r']:+.3f} p={row['p_value']:.3g} "
          f"({row['strength']} {row['direction']})")
print()
print("Regression (flipper -> mass):")
print(f"  {result['equation']}")
print(f"  r = {result['pearson_r']:.3f}, R2 = {result['pearson_r']**2:.3f}, "
      f"test RMSE = {result['metrics_test']['RMSE']:.1f} g, "
      f"test R2 = {result['metrics_test']['R2']:.3f}")
print()
print("Outliers (IQR, 1.5 x IQR fences):")
print(f"  pooled over all rows      : {int(overall_rows['n_outliers'].sum())} outlier(s)")
print(f"  computed per species      : {int(grouped_rows['n_outliers'].sum())} outlier(s)")
print(f"  removed from the data     : 0 (never delete outliers without justification)")
print("=" * 74)
"""
)
md(
    """
### Observations

1. **Data quality:** the raw penguins table has 344 rows, 19 missing values, 0
   duplicates and no impossible values. Cleaning removed 2 rows whose every
   measurement was missing and labelled 9 unknown sexes as `Unknown`, so 342
   complete observations remain.
2. **Distributions:** all four measurements are approximately symmetric
   (|skewness| < 0.5); body mass is the most right-skewed (0.47) and bill depth
   slightly left-skewed (-0.14). None of them is bimodal *within* a species,
   but pooling species makes body mass look wider - visible in the violin plots.
3. **Relationships:** the strongest real linear relationship is
   flipper length vs body mass (r = 0.871, p < 10^-100). `year` shows no linear
   relationship with body mass (r = 0.042, p = 0.44).
4. **Simpson's paradox:** pooled, bill depth and flipper length correlate
   *negatively* (r = -0.584), yet *inside every species* the correlation is
   *positive*. The pooled sign is driven by the species mix - a classic warning
   against interpreting a correlation without checking subgroups.
5. **Regression:** body mass = -5741.26 + 49.51 x flipper length; test R2 = 0.78,
   test RMSE ~ 348 g. Residuals scatter randomly around zero.
6. **Outliers:** the pooled IQR rule flags 0 observations, while the same rule
   applied inside each species flags 6. Outliers depend on the reference group,
   and none of them was deleted.
"""
)

md(
    """
## 16. Conclusion

The experiment met all of its objectives: the real Palmer Penguins dataset was
loaded, documented, quality-checked and cleaned with a reproducible,
fully-logged workflow; the five canonical distribution shapes were demonstrated
with seeded synthetic data and then verified on the real measurements;
relationships were visualised and quantified with Pearson's r (computed by hand
and by three libraries, agreeing to machine precision); a correlation matrix and
annotated heatmap were produced; a simple linear regression was trained on a
75 % split and honestly evaluated on the remaining 25 %; outliers were detected
with the IQR rule both pooled and per species; and a full set of additional
statistical visualizations was saved as high-resolution PNG files.

All figures, tables and reports are regenerated automatically by
`python src/run_eda.py --data data/raw/penguins.csv` - the notebook and the
script share the same core functions in `src/`.
"""
)

md(
    """
## 17. Limitations and references

**Limitations**

* The dataset covers only one region (Palmer Station, Antarctica) and three
  breeding seasons (2007-2009), so the findings are not automatically valid for
  other penguin populations or years.
* Pearson's r and simple linear regression capture only *linear* patterns;
  non-linear or interaction effects (e.g. species x sex) are not modelled.
* Correlation is not causation - nothing here proves that a longer flipper
  *causes* a higher body mass; both may be driven by species, age or sex.
* 9 rows had an unknown sex and 2 rows had no measurements at all; the
  `Unknown` label keeps them visible but they cannot contribute to
  sex-specific analysis.
* The p-values assume approximate bivariate normality and independence of
  observations; the three measurements per year are not strictly independent
  (same colony, same season).
* The synthetic demonstrations are teaching devices, not empirical evidence.

**References**

1. Gorman KB, Williams TD, Fraser WR (2014). *Ecological sexual dimorphism and
   environmental variability within a community of Antarctic penguins (genus
   Pygoscelos)*. PLoS ONE 9(3): e109091. DOI 10.1371/journal.pone.0109091
2. Horst A (2020). *palmerpenguins: Palmer Archipelago (Antarctica) penguin
   data*. R package, CRAN. Data released under CC0 1.0.
3. Wickham H (2014). *Exploratory Data Analysis*. Had.co.nz.
4. Tukey JW (1977). *Exploratory Data Analysis*. Addison-Wesley.
5. McGrew JC Jr (2014). *Introductory Forecasts and Exploratory Data Analysis*.
6. scikit-learn documentation: `LinearRegression`,
   https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
7. SciPy documentation: `scipy.stats.pearsonr`, `scipy.stats.linregress`.
"""
)

md(
    """
## 18. Viva questions

A list of **33 beginner-friendly viva questions with answers** (EDA basics,
distributions, skewness, correlation, p-values, regression, R-squared,
residuals, outliers, IQR, correlation vs causation, tools) is saved in:

`outputs/reports/viva_questions.md`

It is also included in the downloadable ZIP archive at the end of this notebook.
"""
)

# ===========================================================================
# 14. Packaging and downloads
# ===========================================================================
md(
    """
## 19. Package all deliverables

Everything produced by this notebook (plots, reports, cleaned data, scripts,
README, this notebook) is packed into one ZIP archive. In Google Colab the
download starts automatically; locally the path is printed.
"""
)
code(
    """
# --- package plots, reports, cleaned data, scripts and this notebook ---
zip_path = ROOT / "outputs" / "eda_experiment3_outputs.zip"
include_folders = [
    ROOT / "outputs" / "plots", ROOT / "outputs" / "reports", ROOT / "outputs" / "logs",
    ROOT / "data" / "processed", ROOT / "data" / "raw", ROOT / "src", ROOT / "tests",
]
optional_files = [ROOT / "EXPERIMENT 3.ipynb", ROOT / "README.md",
                  ROOT / "requirements.txt", ROOT / ".gitignore"]

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for folder in include_folders:
        if folder.exists():
            for file in sorted(folder.rglob("*")):
                if file.is_file() and "__pycache__" not in file.parts \\
                        and file.suffix not in {".pyc", ".pyo"}:
                    zf.write(file, file.relative_to(ROOT))
    for file in optional_files:
        if file.exists():
            zf.write(file, file.relative_to(ROOT))

print("ZIP archive created:", zip_path, f"({zip_path.stat().st_size / 1e6:.2f} MB)")
print()
print("Contents:")
with zipfile.ZipFile(zip_path) as zf:
    for name in zf.namelist():
        print("  ", name)
print()
print("No API token, credential file or secret configuration is included in the ZIP.")

# --- Colab convenience: start downloads -------------------------------------
if IS_COLAB:
    from google.colab import files  # type: ignore
    print("\\nDownloading the ZIP archive ...")
    files.download(str(zip_path))
"""
)
code(
    """
# --- individual downloads / quick access (optional) -------------------------
targets = [
    ROOT / "data" / "processed" / "cleaned_dataset.csv",
    ROOT / "outputs" / "reports" / "data_cleaning_report.json",
    ROOT / "outputs" / "reports" / "pearson_correlation_matrix.csv",
    ROOT / "outputs" / "reports" / "regression_metrics.json",
    ROOT / "outputs" / "reports" / "outlier_report.csv",
    ROOT / "outputs" / "reports" / "viva_questions.md",
]
print("Key deliverables:")
for target in targets:
    size = f"{target.stat().st_size / 1024:.1f} KB" if target.exists() else "MISSING"
    print(f"  {str(target.relative_to(ROOT)):<55} {size}")

if IS_COLAB:
    answer = input("Download any of these files individually? (y/n): ").strip().lower()
    if answer == "y":
        from google.colab import files  # type: ignore
        for target in targets:
            if target.exists():
                files.download(str(target))
else:
    print("\\nRun the whole experiment again from the command line with:")
    print("    python src/run_eda.py --data data/raw/penguins.csv --output outputs")
    print("Re-running the notebook or the script overwrites previous outputs (no duplicates).")
"""
)

md(
    """
### Running this experiment elsewhere

**Google Colab** - upload `eda_experiment3_outputs.zip` (or this notebook plus
`data/raw/penguins.csv`) and use *Runtime -> Run all*. The notebook installs any
missing library, detects Colab, uploads a CSV when no dataset exists and
downloads the finished ZIP at the end.

**Kaggle** - create a new notebook, attach this project ZIP (or a dataset with
`penguins.csv`) as an *Input dataset*, then run top-to-bottom. The notebook
detects Kaggle, reads the CSV from `/kaggle/input/` (no download if already
mounted) and writes everything under `/kaggle/working/`. To use the Kaggle API
locally, place your credentials in `~/.kaggle/kaggle.json` with permissions 600
and never commit that file (it is listed in `.gitignore`).

**Local Python**

```
pip install -r requirements.txt
python src/run_eda.py --data data/raw/penguins.csv --output outputs
pytest                 # optional: run the automated tests
```
"""
)


if __name__ == "__main__":
    notebook = build()
    nbf.write(notebook, NOTEBOOK_PATH)
    print(f"Wrote {NOTEBOOK_PATH} with {len(notebook.cells)} cells.")


