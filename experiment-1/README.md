# Experiment 1 — Iris Dataset Visualization

Descriptive visualization of the classic Iris dataset in Python, plus a Power BI
dashboard built from the same data.

**Kaggle (private):** https://www.kaggle.com/code/arulmariaagnes/experiment-1-iris-dataset-visualization

## Aim

Load a real-world dataset, inspect it, and produce a set of clear,
publication-quality visualizations that reveal the structure between the four
measurements and the three species — then mirror the same story in an
interactive Power BI dashboard.

## Dataset

| | |
|---|---|
| Source | Fisher's Iris dataset as distributed by the UCI Machine Learning Repository |
| Records | 150 (50 per species) |
| Columns | `SepalLengthCm`, `SepalWidthCm`, `PetalLengthCm`, `PetalWidthCm`, `Species` |
| Quality | 0 missing values, 0 duplicate rows, no impossible values |
| Local copy | `data/Iris.csv` (original), `data/Iris_processed.csv` (cleaned) |

## Files

| File | Description |
|------|-------------|
| `Iris_Visualization_Colab.ipynb` | **The experiment** — executed notebook (28 cells, 13 code cells, 0 errors) |
| `iris_visualization_colab.py` | The same analysis as a plain Python script |
| `data/Iris.csv`, `data/Iris_processed.csv` | Dataset |
| `outputs/vis1…vis7_*.png` | The seven generated figures |
| `outputs/Iris_Dashboard.png` | Screenshot of the finished Power BI dashboard |
| `outputs/*.png` (remaining) | Power BI build screenshots (import, measures, DAX checks, final save) |
| `powerbi/Iris_Dashboard.pbix` | Power BI Desktop dashboard file |
| `powerbi/automation/*.py` | 54 scripts that drove the Power BI UI (build log/evidence) |
| `PowerBI_DAX.txt` | DAX measures |
| `Iris_PowerBI_Theme.json` | Custom theme (iris colour palette) |
| `POWERBI_BUILD_SPEC.md` | Build specification for the dashboard |
| `README.md` | This file |

## Running it

```bash
pip install -r ../requirements.txt     # numpy, pandas, matplotlib, seaborn
python iris_visualization_colab.py     # writes outputs/vis*.png
jupyter notebook Iris_Visualization_Colab.ipynb
```

The notebook finds its data without any manual step, in this order:

1. `IRIS_CSV` environment variable,
2. `Iris.csv` / `data/Iris.csv` next to the notebook,
3. any `Iris.csv` under `/kaggle/input/`,
4. a Colab upload prompt (only when running in Colab).

Figures are written to `/kaggle/working/outputs`, `/content/outputs` or
`./outputs`, whichever exists in the current runtime.

### Power BI

1. Open `powerbi/Iris_Dashboard.pbix` in Power BI Desktop.
2. If the data source needs refreshing, point it at `data/Iris.csv`.
3. Apply `Iris_PowerBI_Theme.json` for the iris colour palette.

## Visualizations

| # | Figure | Chart |
|---|--------|-------|
| 1 | `vis1_species_distribution.png` | species counts (bar) |
| 2 | `vis2_average_measurements.png` | mean measurements per species (grouped bar) |
| 3 | `vis3_sepal_scatter.png` | sepal length vs sepal width |
| 4 | `vis4_petal_scatter.png` | petal length vs petal width |
| 5 | `vis5_boxplots.png` | distribution of each measurement (box plot) |
| 6 | `vis6_correlation_heatmap.png` | feature correlation matrix |
| 7 | `vis7_pairplot.png` | pairwise relationships coloured by species |

Power BI mirrors these: KPI cards, species column chart, grouped bars, both
scatters, box plots, correlation heatmap and a species slicer.

## Verified results

Re-computed from `data/Iris.csv` while building this repository:

* 150 rows, 3 species × 50, **0 missing, 0 duplicates**.
* Setosa sepal length mean **5.006** (width **3.418**); virginica sepal length **6.588**.
* Setosa petal length **1.464** (sd **0.244**); virginica petal length **5.552** (sd **2.026**).
* Correlations: petal length ↔ petal width **r = 0.963**; sepal length ↔ petal length
  **0.872**; sepal length ↔ petal width **0.818**; sepal width ↔ petal length **−0.421**.

Interpretation: petal measurements separate the species almost perfectly
(setosa is linearly separable), while the sepal measurements overlap; the
negative sepal-width/petal-length correlation is the well-known Simpson-type
effect that appears when the three species are pooled.

**Notebook execution:** 28 cells / 13 code cells, **0 errors**. Six of the seven
figures are byte-identical to the original outputs; `vis5` differs only because
it was rendered with a newer seaborn release.

## Requirements

* Python 3.9+ — `numpy`, `pandas`, `matplotlib`, `seaborn`
* Power BI Desktop (optional, for the `.pbix`)
