# EXPERIMENT 3 — Exploratory Data Analysis Through Statistical Visualization of Distributions, Relationships, Correlations, and Outliers

A complete, reproducible, beginner-friendly EDA practical built on the **real**
Palmer Penguins dataset, with a Jupyter/Colab/Kaggle notebook, modular Python
code, automated tests, saved figures, machine-readable reports and a
downloadable ZIP archive.

**Kaggle (private):** https://www.kaggle.com/code/arulmariaagnes/experiment-3-statistical-visualization-and-eda

---

## 1. Aim

Perform a complete Exploratory Data Analysis (EDA) on a real-world dataset using
statistical visualizations of distributions, relationships, correlations,
regression and outliers.

## 2. Objectives

1. Load, inspect and document a real-world dataset.
2. Detect and clean data-quality problems (missing values, duplicates, impossible
   values, categorical inconsistencies) with a fully documented workflow.
3. Demonstrate the **five** canonical distribution shapes (Gaussian, uniform,
   right-skewed, left-skewed, bimodal) and analyse the real dataset's distributions.
4. Visualise seven relationship patterns (strong/weak/no/perfect, positive/negative).
5. Compute Pearson's correlation coefficient by formula and by three libraries,
   build a correlation matrix and an annotated heatmap.
6. Fit and honestly evaluate a simple linear regression (train/test split).
7. Detect outliers with the IQR rule and visualise them with box plots.
8. Produce additional statistical visualizations (pair plot, violin plots,
   Q-Q plots, count plots, bar charts).
9. Document findings, limitations and 33 viva Q&As.

## 3. Software and libraries

| Library | Purpose |
|---|---|
| Python ≥ 3.9 | runtime |
| pandas | tables, CSV I/O, statistics |
| NumPy | arrays, numerical maths |
| Matplotlib | plotting |
| Seaborn | statistical plots (KDE, heatmap, box/violin/pair plots) |
| SciPy | `pearsonr`, `linregress`, skewness, Q-Q plots |
| scikit-learn | `LinearRegression`, metrics, train/test split |
| nbformat / nbclient / ipykernel | build and execute the notebook |
| pytest | automated tests |
| kaggle (optional) | Kaggle API access |

## 4. Dataset

**Palmer Penguins** — 344 real observations of Adelie, Chinstrap and Gentoo
penguins collected at Palmer Station, Antarctica (2007–2009).

| Column | Type | Meaning |
|---|---|---|
| `species` | categorical | Adelie / Chinstrap / Gentoo |
| `island` | categorical | Torgersen / Biscoe / Dream |
| `bill_length_mm` | numerical | bill length (mm) |
| `bill_depth_mm` | numerical | bill depth (mm) |
| `flipper_length_mm` | numerical | flipper length (mm) |
| `body_mass_g` | numerical | body mass (g) |
| `sex` | categorical | male / female / (missing) |
| `year` | ordinal | 2007 / 2008 / 2009 |

* **Local file:** `data/raw/penguins.csv` (included in this project)
* **Download URL:** `https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv`
* **License:** CC0 1.0 (public domain dedication) via the `palmerpenguins` R package
* **Citation:** Gorman KB, Williams TD, Fraser WR (2014), *PLoS ONE* 9(3): e109091,
  DOI 10.1371/journal.pone.0109091
* **Quality profile:** 19 missing values (2 rows with no measurements, 9 rows
  without recorded sex), 0 duplicate rows, no impossible values.

## 5. Installation

```bash
git clone https://github.com/ArulAgnes/Data-Visualization-Lab-Experiments.git
cd Data-Visualization-Lab-Experiments/experiment-3
pip install -r requirements.txt
```

## 6. Running the experiment

### Local (command line — regenerates every output)

```bash
python src/run_eda.py --data data/raw/penguins.csv --output outputs
```

Useful flags: `--seed 42`, `--x-col flipper_length_mm`, `--y-col body_mass_g`,
`--test-size 0.25`, `--random-state 42`, `--no-zip`, `--quiet`.
`--output <folder>` really does redirect every artefact (figures, reports and
log) into `<folder>/…` instead of `outputs/…` — it is verified by running the
command twice and checking that only the requested folder receives files.
Running it twice with the same folder overwrites the previous outputs — no
duplicates are created.

### Local (notebook)

```bash
jupyter notebook "EXPERIMENT 3.ipynb"     # then Runtime → Run All
```

### Automated tests

```bash
pytest            # 69 tests: cleaning, correlation, regression, outliers, loading
```

### Google Colab

1. Download `outputs/eda_experiment3_outputs.zip` (contains the notebook, `src/`,
   `data/raw/penguins.csv` and everything else).
2. In Colab: *File → Upload notebook* → upload `EXPERIMENT 3.ipynb`, **or** upload
   the ZIP in the first code cell when it asks for project files.
3. *Runtime → Run all*. The notebook installs missing libraries, detects Colab,
   creates all output folders, and downloads the finished ZIP automatically.
4. Alternatively upload only a CSV: the notebook will ask for it when no dataset
   path is configured (`google.colab.files.upload()`).

No Google Drive access is required and no local Windows path is assumed.

### Kaggle

The experiment is already published as a **private** Kaggle notebook that is
self-contained: the project code, the dataset and the reports are embedded in
the notebook itself, so it needs no attached dataset.

1. Open https://www.kaggle.com/code/arulmariaagnes/experiment-3-statistical-visualization-and-eda
   (private — visible to the owner and anyone invited).
2. *Run all*. The notebook restores `src/` and `data/raw/penguins.csv` from its
   embedded archive when they are missing, reads the CSV from
   `/kaggle/input/…` when a dataset *is* attached, and writes plots/reports/ZIP
   to `/kaggle/working/`.
3. To publish your own copy, use the CLI from `experiment-3/`:

   ```bash
   # kernel-metadata.json: is_private = "true", enable_internet = "false"
   kaggle kernels push -p <folder-with-notebook-and-metadata>
   kaggle kernels status <owner>/<slug>
   ```

4. If you attach a dataset containing `penguins.csv`, the loader finds it under
   `/kaggle/input/`; set `KAGGLE_DATASET_SLUG` in the configuration cell to look
   only in that mounted folder.
5. To download a Kaggle dataset from your machine, configure the API securely:

   ```bash
   # Windows
   mkdir %USERPROFILE%\.kaggle
   # place kaggle.json (from Kaggle → Account → Create New API Token) there
   icacls %USERPROFILE%\.kaggle\kaggle.json /inheritance:r /grant:r "%USERNAME%:R"
   # macOS / Linux
   mkdir -p ~/.kaggle && chmod 600 ~/.kaggle/kaggle.json
   kaggle datasets download -d <owner>/<dataset> -p data/raw --unzip
   ```

   Never paste the token into a notebook, chat, source file or Git repository.
   `kaggle.json` and `.kaggle/` are already listed in `.gitignore`, the code only
   checks whether credentials exist (never prints them), and no secrets are
   placed inside the ZIP archive. Nothing is published to Kaggle without your
   explicit action and confirmation.

## 7. Project structure

```
experiment-3/
├── EXPERIMENT 3.ipynb                      # the executed source notebook (89 cells)
├── EXPERIMENT 3 - Statistical Visualization and EDA.ipynb
│                                           # upload-ready copy (91 cells) with src/ + data embedded
├── README.md                               # this file
├── requirements.txt
├── .gitignore                              # blocks kaggle.json, .kaggle/, checkpoints, caches, ZIP
├── data/
│   ├── raw/penguins.csv                    # original dataset (never modified)
│   └── processed/cleaned_dataset.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # multi-environment loading (local/Colab/Kaggle) + output-folder control
│   ├── data_cleaning.py        # documented cleaning workflow + JSON report
│   ├── distribution_analysis.py# 5 synthetic shapes + dataset summaries
│   ├── relationship_analysis.py# 7 correlation demos (seeded)
│   ├── correlation_analysis.py # manual formula, pairwise stats, matrix, heatmap data
│   ├── regression_analysis.py  # sklearn + scipy regression, metrics, prediction
│   ├── outlier_analysis.py     # IQR fences, grouped detection, synthetic example
│   ├── visualization.py        # shared plotting/saving helpers (300 dpi PNG)
│   ├── run_eda.py              # unified command-line runner + ZIP packaging (--output works)
│   ├── build_notebook.py       # regenerates EXPERIMENT 3.ipynb from the same code
│   └── build_colab_notebook.py # regenerates the upload-ready copy (embeds src/ + data)
├── outputs/
│   ├── plots/                  # 30 high-resolution PNG figures
│   ├── reports/                # JSON/CSV reports + viva_questions.md
│   ├── logs/eda_run.log        # execution log
│   └── eda_experiment3_outputs.zip   # regenerated by the runner; not tracked by git
└── tests/                      # 69 pytest tests (conftest + 5 test modules)
```

## 8. Statistical formulas used

**Pearson correlation**

```
r = Σ((x − x̄)(y − ȳ)) / sqrt( Σ(x − x̄)² · Σ(y − ȳ)² )
```

**Simple linear regression:** `y_hat = b0 + b1·x`
with `b1 = cov(x, y)/var(x)`, `b0 = ȳ − b1·x̄`; for simple OLS `R² = r²`.

**IQR outlier rule**

```
Q1 = 25th percentile,  Q3 = 75th percentile,  IQR = Q3 − Q1
lower fence = Q1 − 1.5·IQR       upper fence = Q3 + 1.5·IQR
```

**Metrics:** `MAE = mean|y − ŷ|`, `MSE = mean(y − ŷ)²`, `RMSE = sqrt(MSE)`,
`R² = 1 − SS_res/SS_tot`, `p`-value from the t-distribution of r (df = n − 2).

## 9. Description of each visualization

| Figure | What it shows |
|---|---|
| `distribution_gaussian.png` | bell-shaped sample, fitted normal curve, mean/median lines |
| `distribution_uniform.png` | flat histogram vs theoretical density 0.01 |
| `distribution_right_skewed.png` | long right tail, mean > median |
| `distribution_left_skewed.png` | long left tail, mean < median |
| `distribution_bimodal.png` | two peaks from two overlapping groups |
| `dataset_distributions.png` | hist + KDE of the four real measurements |
| `dataset_qq_plots.png` | Q-Q plots assessing normality of real data |
| `correlation_strong_positive/negative.png` | tight bands, r ≈ ±0.95 |
| `correlation_weak_positive/negative.png` | diffuse clouds, r ≈ ±0.30 |
| `correlation_no_linear.png` | independent noise *and* a parabola, both r ≈ 0 |
| `correlation_perfect_positive/negative.png` | exact lines, r = ±1 |
| `real_scatter_*.png` | four real penguin pairs coloured by species |
| `pearson_correlation_heatmap.png` | annotated diverging heatmap centred at 0 |
| `linear_regression_fit.png` | observations + fitted line with the equation |
| `actual_vs_predicted.png` | test-set actual vs predicted with the perfect line |
| `regression_residuals.png` | residuals vs fitted values (random scatter around 0) |
| `residual_distribution.png` | residual histogram vs normal reference curve |
| `boxplot_outlier_detection.png` | individual box plots with fence values |
| `boxplot_all_numeric.png` | combined z-score box plot (comparable scales) |
| `boxplot_synthetic_example.png` | synthetic sample with 4 injected outliers |
| `pairplot.png` | all pairwise relationships coloured by species |
| `violin_by_species.png` | distribution shape per species |
| `countplots_categorical.png` | frequencies of species / island / sex |
| `barplot_mean_mass_by_species.png` | mean body mass ± 1 sd per species |

## 10. Results of the actual run (verified locally)

* **Cleaning:** 344 → 342 rows (2 rows missing all measurements dropped);
  19 → 0 missing values (9 `sex` gaps labelled `Unknown`); 0 duplicates;
  no column dropped; report saved as JSON.
* **Real distributions:** all approximately symmetric —
  bill length skew +0.05, bill depth −0.14, flipper +0.34, body mass +0.47.
* **Correlations (pooled, n = 342):** flipper↔mass **r = 0.871** (p ≈ 4e-107),
  bill length↔flipper r = 0.656, bill depth↔flipper **r = −0.584**,
  year↔mass r = 0.042 (p = 0.44 → not significant).
* **Simpson's paradox:** inside every species the bill depth↔flipper correlation
  is *positive*, even though the pooled correlation is negative.
* **Regression:** `body_mass_g = −5741.26 + 49.51 × flipper_length_mm`;
  r = 0.871, R² = 0.76; **test** metrics (25 % hold-out): MAE 281.98 g,
  RMSE 347.99 g, R² = 0.783; median-flipper prediction included in the report.
* **Outliers (1.5 × IQR):** 0 pooled, **6** when computed inside each species
  (1 bill length, 1 bill depth, 2 flipper length, 2 body mass). None deleted.
* **Tests:** 69/69 passed. **Notebook:** 89 cells executed top-to-bottom,
  0 errors, 30 inline figures.

## 11. Limitations

* One region and three breeding seasons only — results do not automatically
  generalise to other populations or years.
* Only linear patterns are quantified; interactions (species × sex) are not modelled.
* Correlation ≠ causation; no causal claim is made anywhere.
* 9 rows have an unlabelled sex (`Unknown`) and 2 rows have no measurements.
* p-values assume approximate bivariate normality and independent observations.
* The synthetic demonstrations are teaching devices, not empirical evidence.
* Google Colab execution requires your own account/session. The Kaggle copy is
  published (private) and was run to completion by the Kaggle worker — see the
  kernel link at the top of this file.

## 12. Troubleshooting

| Symptom | Fix |
|---|---|
| `FileNotFoundError: No dataset found` | pass `--data <path>` or place the CSV at `data/raw/penguins.csv` |
| `ModuleNotFoundError: src` | run from the project root, or `pip install -e .` is not needed — the runner inserts the root into `sys.path` automatically |
| Plots do not appear in the notebook | make sure the cell ends with `plt.show()` and you are in Jupyter/Colab (not a plain `.py` run) |
| `No module named 'nbclient'` | `pip install nbclient ipykernel nbformat` |
| Colab asks for a file | upload the project ZIP (preferred) or the CSV when prompted |
| Kaggle: dataset not found | set `KAGGLE_DATASET_SLUG` or attach the dataset in *Add data* |
| `kaggle` CLI auth errors | check `~/.kaggle/kaggle.json` exists with permissions 600; the value is never printed by this project |
| Outputs look stale | re-run `python src/run_eda.py --data data/raw/penguins.csv` — files are overwritten, never duplicated |

## 13. Conclusion

This experiment delivers a complete, honest EDA pipeline: real data loaded and
documented, cleaning decisions recorded and justified, all five distribution
shapes demonstrated, seven correlation patterns visualised, Pearson's r
verified four different ways, a regression model evaluated on unseen data,
outliers detected (and kept), and every figure/report saved automatically. The
notebook and the command-line runner share one code base, so the results are
fully reproducible on a laptop, in Google Colab or on Kaggle.

## 14. Viva preparation

See `outputs/reports/viva_questions.md` — 33 beginner-friendly questions with
answers covering EDA, cleaning, all five distributions, scatter plots,
correlation, Pearson's r, p-values, regression, slope/intercept, R², residuals,
outliers, IQR, heatmaps and the difference between correlation and causation.
