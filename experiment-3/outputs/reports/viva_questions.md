# Viva Questions and Answers — Experiment 3 (EDA)

Beginner-friendly answers for an undergraduate practical viva. The numbers quoted
are the ones produced by this project's actual run on the Palmer Penguins dataset.

---

## Basic concepts

### 1. What is EDA?
**Exploratory Data Analysis (EDA)** is the first stage of any data project. You
inspect, summarise and visualise the data *before* building models, so that you
understand its shape, quality, patterns and problems. Tools include summary
statistics, histograms, box plots, scatter plots and correlation matrices.

### 2. Why do we clean data?
Real datasets contain missing values, duplicate rows, spelling mistakes
(`"male"` vs `"MALE "`), wrong data types and impossible numbers. If we skip
cleaning, statistics are biased (e.g. averages pulled down by missing rows) and
plots become misleading. Cleaning makes the analysis reproducible and honest.

### 3. What is the difference between raw and cleaned data?
The **raw** data is the untouched original file. The **cleaned** data has
documented corrections applied. In this project the raw file
(`data/raw/penguins.csv`) is never modified; the cleaned version is written to
`data/processed/cleaned_dataset.csv`, and every decision is recorded in
`outputs/reports/data_cleaning_report.json`.

### 4. What is a missing value?
A missing value is an observation that was not recorded (empty cell, `NaN`,
`NULL`). In the penguins dataset, 2 rows have no measurements at all and 9 rows
have no recorded sex. Missing values must be handled deliberately - dropped,
labelled, or imputed - never ignored.

---

## Distributions

### 5. What is a Gaussian (normal) distribution?
A bell-shaped, symmetric distribution defined by its mean and standard
deviation. About 68 % of the data lies within 1 standard deviation of the mean,
95 % within 2 and 99.7 % within 3. Many natural measurements (heights, exam
scores of large classes) are approximately normal. Mean = median = mode.

### 6. What is a uniform distribution?
Every value in an interval has (approximately) the same probability - the
histogram is flat. Example: rolling a fair die, or `np.random.uniform(0, 100)`.
The mean sits in the middle of the interval.

### 7. What is skewness?
Skewness measures the **asymmetry** of a distribution.
- **Right-skewed (positive skew)**: long tail on the right, mean > median.
  Example: household incomes.
- **Left-skewed (negative skew)**: long tail on the left, mean < median.
  Example: scores in a very easy exam (most students near 100).
Rule of thumb: |skewness| < 0.5 ≈ symmetric.

### 8. What is a bimodal distribution?
A distribution with **two peaks**, which usually means two sub-groups were
pooled together (e.g. male and female penguin body masses, or morning and
evening traffic). Plotting the data coloured by group reveals the hidden
structure.

### 9. What is a histogram?
A bar chart of how many observations fall into equal-width bins. It shows the
*shape* of a distribution. The height is a count (or a density).

### 10. What is a KDE plot?
A **Kernel Density Estimate** is a smooth curve that approximates the
probability density of the data. It is like a histogram drawn with a continuous
curve, so peaks and skew are easier to see.

### 11. What is a Q-Q plot?
A **quantile-quantile plot** compares the quantiles of your data with the
quantiles of a theoretical normal distribution. If the points follow the
straight red line, the data is approximately normal; S-shaped curves indicate
skew or heavy tails.

---

## Relationships and correlation

### 12. What is a scatter plot?
A plot of one dot per observation using two numerical variables (x on the
horizontal axis, y on the vertical). It reveals the direction, strength and
form of a relationship, plus unusual points.

### 13. What is correlation?
Correlation is a measure of how two numerical variables change *together*.
Positive correlation: both tend to rise together. Negative: one rises while the
other falls. Zero: no **linear** co-movement.

### 14. What is Pearson's correlation coefficient (r)?
Pearson's *r* is a number between −1 and +1 that measures the strength and
direction of the **linear** relationship between two continuous variables:

```
r = Σ((x − x̄)(y − ȳ)) / sqrt( Σ(x − x̄)² · Σ(y − ȳ)² )
```

It is computed here with `scipy.stats.pearsonr`, `numpy.corrcoef`,
`DataFrame.corr()` and by hand with NumPy - all give the same answer.

### 15. What does r = +1 mean?
A **perfect positive linear relationship**: all points lie exactly on an
upward-sloping straight line. Doubling x always increases y by a fixed amount.

### 16. What does r = −1 mean?
A **perfect negative linear relationship**: all points lie exactly on a
downward-sloping straight line.

### 17. What does r = 0 mean?
There is **no linear** relationship. It does **not** mean the variables are
independent - a strong curved (non-linear) relationship can also give r ≈ 0.
This experiment demonstrates that with a parabola: r ≈ 0 although y = x² exactly.

### 18. How do we interpret the strength of r?
Rules of thumb (configurable, not universal laws): |r| ≥ 0.8 very strong,
0.6–0.8 strong, 0.4–0.6 moderate, 0.2–0.4 weak, < 0.2 negligible. Context
matters: r = 0.5 can be huge in social sciences and tiny in physics.

### 19. What is a p-value in correlation testing?
The p-value is the probability of observing a correlation at least this strong
in a random sample **if the true population correlation were zero**. A small
p-value (e.g. < 0.05) means the correlation is unlikely to be a pure sampling
accident. In this dataset, flipper length vs body mass has p ≈ 10⁻¹⁰⁷ -
extremely significant.

### 20. What is a correlation heatmap?
A matrix of correlation coefficients rendered as colours - typically red for
positive, blue for negative and white near zero, centred at 0. It lets you scan
many variable pairs at once. Ours is `outputs/plots/pearson_correlation_heatmap.png`.

### 21. What is the difference between correlation and causation?
Correlation only says two variables move together; a **third variable** or
coincidence can create the pattern. Causation requires a plausible mechanism
and usually a controlled experiment. Example: ice-cream sales and drowning are
correlated - the sun (temperature) is the cause. **Never claim causation from a
correlation or a small p-value alone.**

---

## Regression

### 22. What is linear regression?
A method that finds the straight line that best predicts one numerical variable
(**target**) from another (**predictor**):

```
y_hat = b0 + b1 * x
```

`b0` is the intercept (predicted y when x = 0) and `b1` is the slope (change in
predicted y for a one-unit increase in x).

### 23. What are slope and intercept?
In this dataset the fitted equation is
`body_mass_g = -5741.26 + 49.51 × flipper_length_mm`, so every extra millimetre
of flipper length is associated with about **49.5 g** more body mass. The
intercept (−5741 g) is not physically meaningful - a 0 mm flipper penguin does
not exist - it only anchors the line.

### 24. What is R-squared?
R² is the fraction of the variance in the target explained by the model (0 to
1). In simple regression R² = r². Our model: r = 0.871, R² ≈ 0.76, so about
76 % of the variation in body mass is associated with flipper length. It never
proves the model is *correct*.

### 25. What are residuals?
A residual is `actual − predicted` for one observation. The residual plot shows
residuals against fitted values; for a good linear model they should scatter
randomly around 0 with no clear pattern. A funnel shape suggests heteroscedasticity.

### 26. Why use a train/test split?
If you evaluate a model on the same rows it was trained on, the metrics are
optimistic. We fit on 75 % of the penguins and evaluate on the unseen 25 %
(test RMSE ≈ 348 g, R² ≈ 0.78) - an honest estimate of performance on new data.

---

## Outliers

### 27. What is an outlier?
An observation that lies far away from the rest of the data. It may be a
measurement error, a data-entry mistake, or a genuine and important rare event
(e.g. the heaviest penguin ever recorded).

### 28. What is the IQR?
The **Interquartile Range** is `IQR = Q3 − Q1`, the width of the middle 50 % of
the data. Tukey's fences are `Q1 − 1.5×IQR` and `Q3 + 1.5×IQR`; values outside
are *potential* outliers (also drawn as points on a box plot).

### 29. Why should outliers not always be removed?
Blind deletion shrinks variance, biases means and hides real phenomena. An
outlier must be investigated: if it is a proven error it can be corrected or
removed with documentation; if it is real it should be kept (or analysed
separately). This project **reports** outliers and never deletes them.

### 30. Can a dataset have no outliers?
Yes. In the penguins data, applying the 1.5×IQR rule to the pooled
measurements flags **0** outliers, yet within individual species 6 points fall
outside the species-specific fences. This shows that outlier detection depends
on the group you compare against.

---

## Tools and workflow

### 31. What is pandas / NumPy / Matplotlib / Seaborn / SciPy / scikit-learn?
- **pandas**: tables (DataFrames), loading CSVs, summary statistics.
- **NumPy**: fast arrays and numerical maths.
- **Matplotlib**: low-level plotting (histograms, scatter, lines).
- **Seaborn**: high-level statistical plots on top of Matplotlib.
- **SciPy**: statistical tests (`pearsonr`, `linregress`, skewness).
- **scikit-learn**: machine learning tools (`LinearRegression`, train/test split).

### 32. Why fix a random seed?
`random_state = 42` makes random steps (synthetic data, train/test split)
identical every run, so the notebook, the reports and the figures are exactly
reproducible.

### 33. What is the difference between this notebook and `src/run_eda.py`?
Both call the **same** Python functions in `src/`. The notebook shows every step
with inline plots and explanations; `python src/run_eda.py --data data/raw/penguins.csv`
re-runs the entire experiment from the command line and rebuilds all outputs.
