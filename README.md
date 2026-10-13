# Data Visualization Lab — Experiments 1–3

A single, reproducible repository for the three practical experiments of the
**M.E. CSE Data Visualization** lab. Every notebook in this repo was executed
top-to-bottom before it was committed, and every number quoted below was
re-computed from the shipped data.

| # | Experiment | Dataset / material | Notebook | Kaggle |
|---|------------|--------------------|----------|--------|
| 1 | **Iris dataset visualization** — descriptive EDA plus a Power BI dashboard | Fisher's Iris (150 rows) | `experiment-1/Iris_Visualization_Colab.ipynb` | [kernel](https://www.kaggle.com/code/arulmariaagnes/experiment-1-iris-dataset-visualization) |
| 2 | **Research-paper visualization redesign (EXERCISE-2)** — 15 published figures rebuilt as clear Python charts | 15 research papers + exercise statistics | `experiment-2/EXPERIMENT 2 - Research Visualization Redesign.ipynb` | [kernel](https://www.kaggle.com/code/arulmariaagnes/experiment-2-research-visualization-redesign) |
| 3 | **Exploratory data analysis through statistical visualization** — distributions, relationships, correlation, regression, outliers | Palmer Penguins (344 rows) | `experiment-3/EXPERIMENT 3.ipynb` (+ the upload-ready Colab/Kaggle copy) | [kernel](https://www.kaggle.com/code/arulmariaagnes/experiment-3-statistical-visualization-and-eda) |

All three Kaggle notebooks are **private** — none of them is publicly visible.

---

## Repository layout

```
Data-Visualization-Lab-Experiments/
├── README.md                     # this file
├── LICENSE                       # MIT (scope + third-party terms spelled out)
├── requirements.txt              # shared dependencies
├── .gitignore                    # blocks credentials, caches, regenerated archives
├── docs/
│   └── PROJECT_INVENTORY.md      # what was included, what was left out and why
├── experiment-1/                 # Experiment 1 — Iris
│   ├── Iris_Visualization_Colab.ipynb   # executed notebook (28 cells, 0 errors)
│   ├── iris_visualization_colab.py      # same analysis as a plain script
│   ├── data/                     # Iris.csv, Iris_processed.csv
│   ├── outputs/                  # 7 analysis figures + Power BI screenshots
│   ├── powerbi/                  # Iris_Dashboard.pbix + build automation
│   └── README.md
├── experiment-2/                 # Experiment 2 — EXERCISE-2 redesigns
│   ├── EXPERIMENT 2 - Research Visualization Redesign.ipynb
│   ├── build_kaggle_notebook.py  # regenerates the notebook from the scripts
│   ├── 15-paper-redesign/        # selection table, 15 scripts, figures, bib
│   ├── python/                   # the three EXERCISE-2 visualizations
│   ├── records/                  # EXERCISE-2 record documents (DOCX)
│   └── README.md
└── experiment-3/                 # Experiment 3 — Palmer Penguins EDA
    ├── EXPERIMENT 3.ipynb                       # source notebook (89 cells)
    ├── EXPERIMENT 3 - Statistical Visualization and EDA.ipynb  # self-contained copy
    ├── src/                    # loader, cleaning, analysis, runner, builders
    ├── tests/                  # 69 pytest tests
    ├── data/                   # penguins.csv (raw + processed)
    ├── outputs/                # 30 figures, machine-readable reports, log
    └── README.md
```

---

## Quick start

```bash
git clone https://github.com/ArulAgnes/Data-Visualization-Lab-Experiments.git
cd Data-Visualization-Lab-Experiments
pip install -r requirements.txt
```

**Experiment 1**

```bash
cd experiment-1
jupyter notebook Iris_Visualization_Colab.ipynb      # Runtime → Run All
# or, as a script:
python iris_visualization_colab.py
```

**Experiment 2**

```bash
cd experiment-2
jupyter notebook "EXPERIMENT 2 - Research Visualization Redesign.ipynb"
# or rebuild every figure from the command line:
cd 15-paper-redesign && python python/run_all_visualizations.py
```

**Experiment 3**

```bash
cd experiment-3
pytest                                                # 69 tests
python src/run_eda.py --data data/raw/penguins.csv    # regenerates outputs/
jupyter notebook "EXPERIMENT 3.ipynb"
```

On **Kaggle** or **Colab** no local path is required: the notebooks locate their
data themselves (`/kaggle/input/…`, an embedded archive, an environment
variable, or a file next to the notebook) and write results to
`/kaggle/working/…`, `/content/…` or the local `outputs/` folder.

---

## Verified results

Re-computed from the data in this repository at build time — not copied from a
report.

### Experiment 1 — Iris
* 150 rows, 3 species × 50, **0 missing values, 0 duplicate rows**.
* Setosa sepal length mean **5.006**, width **3.418**; virginica sepal length **6.588**.
* Setosa petal length **1.464** (sd 0.244), virginica petal length **5.552** (sd 2.026).
* Correlations: petal length ↔ petal width **r = 0.963**, sepal length ↔ petal length
  **0.872**, sepal length ↔ petal width **0.818**, sepal width ↔ petal length **−0.421**.
* Notebook: **28 cells / 13 code cells, executed with 0 errors**; the 7 saved figures
  match the original outputs (vis5 differs only because of the seaborn version).

### Experiment 2 — visualization redesigns
* **15 papers** catalogued with source, year, chart type and redesign problem.
* **18 figures generated** from Python: 3 EXERCISE-2 visualizations + 15 redesigns.
* All 15 scripts run through `run_all_visualizations.py` with **exit code 0**;
  the new Kaggle notebook executed **61 cells / 36 code cells with 0 errors**.

### Experiment 3 — Palmer Penguins EDA
* 344 → **342 rows** after cleaning; 19 → **0** missing values; 0 duplicates.
* Correlation: flipper length ↔ body mass **r = 0.871** (p ≈ 4e-107).
* Regression: `body_mass_g = −5741.26 + 49.51 × flipper_length_mm`, **R² = 0.759**;
  held-out test **MAE 281.98 g, RMSE 347.99 g, R² 0.783**.
* Outliers (1.5 × IQR): **0 pooled, 6 inside the species groups**, none deleted.
* **69/69 pytest tests pass**; source notebook **89 cells / 47 code cells, 0 errors**,
  upload-ready copy **91 cells / 48 code cells, 0 errors**; 30 figures + 11 reports.

---

## Datasets and third-party material

| Experiment | Data | Source / licence |
|---|---|---|
| 1 | Iris flower measurements (150 rows) | Fisher's dataset as distributed by the UCI Machine Learning Repository — see the UCI record for terms |
| 2 | 15 research papers (metadata, links, redesign briefs) | IEEE Xplore / ScienceDirect records; **titles and links only**, no publisher figures or text are redistributed |
| 3 | Palmer Penguins (344 rows) | CC0 1.0, Gorman, Williams & Fraser (2014), *PLoS ONE* 9(3): e109091 |

Code, notebooks, documentation and Python-generated figures are MIT-licensed —
see [`LICENSE`](LICENSE).

---

## Credentials

No credentials are stored in this repository. `.gitignore` blocks `kaggle.json`,
`.env`, `access_token` and friends; nothing here was ever signed with a token.
If you use the `kaggle` CLI, keep your token outside the repository
(`~/.kaggle/…` or an environment variable) and never paste it into a notebook.

---

## Documentation

* [`docs/PROJECT_INVENTORY.md`](docs/PROJECT_INVENTORY.md) — complete file
  inventory, the validation log, and every inclusion/exclusion decision.
* `experiment-1/README.md`, `experiment-2/README.md`, `experiment-3/README.md` —
  per-experiment detail (aim, method, figure-by-figure description, results).
