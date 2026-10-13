"""
Iris Dataset Visualization - Python Script
Equivalent to Google Colab Notebook
==========================================
This script creates comprehensive visualizations of the Iris dataset.
Run this script to generate all charts and save them as PNG files.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for professional-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Iris-inspired color palette
IRIS_COLORS = {'Iris-setosa': '#2196F3', 'Iris-versicolor': '#4CAF50', 'Iris-virginica': '#FF9800'}

print("=" * 60)
print("IRIS DATASET VISUALIZATION")
print("=" * 60)

# ============================================================
# SECTION 1: Load Dataset
# ============================================================
print("\n--- Loading Dataset ---")
df = pd.read_csv('Iris.csv')
print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ============================================================
# SECTION 2: Data Inspection
# ============================================================
print("\n--- Data Inspection ---")
print(f"\nShape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nDuplicate Rows: {df.duplicated().sum()}")
print(f"\nUnique Species: {df['Species'].unique()}")
print(f"\nSpecies Distribution:\n{df['Species'].value_counts()}")

# ============================================================
# SECTION 3: Descriptive Statistics
# ============================================================
print("\n--- Descriptive Statistics ---")
numeric_cols = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
print(df[numeric_cols].describe())

print("\nMean by Species:")
print(df.groupby('Species')[numeric_cols].mean().round(3))

print("\nStd by Species:")
print(df.groupby('Species')[numeric_cols].std().round(3))

# ============================================================
# VISUALIZATION 1: Species Distribution
# ============================================================
print("\n--- Generating Visualization 1: Species Distribution ---")
fig, ax = plt.subplots(figsize=(8, 6))
species_counts = df['Species'].value_counts()
bars = ax.bar(species_counts.index, species_counts.values,
              color=[IRIS_COLORS[s] for s in species_counts.index],
              edgecolor='white', linewidth=1.5)
for bar, count in zip(bars, species_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
            str(count), ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('Iris Species Distribution', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Species', fontsize=12)
ax.set_ylabel('Number of Flowers', fontsize=12)
ax.set_ylim(0, 60)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('vis1_species_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: vis1_species_distribution.png")

# ============================================================
# VISUALIZATION 2: Average Measurements by Species
# ============================================================
print("\n--- Generating Visualization 2: Average Measurements ---")
mean_by_species = df.groupby('Species')[numeric_cols].mean()
fig, ax = plt.subplots(figsize=(12, 7))
x = np.arange(len(numeric_cols))
width = 0.25
for i, species in enumerate(mean_by_species.index):
    values = mean_by_species.loc[species].values
    bars = ax.bar(x + i * width, values, width,
                  label=species, color=IRIS_COLORS[species],
                  edgecolor='white', linewidth=1)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                f'{val:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
ax.set_title('Average Iris Measurements by Species', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Measurement', fontsize=12)
ax.set_ylabel('Average Value (cm)', fontsize=12)
ax.set_xticks(x + width)
ax.set_xticklabels(['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width'])
ax.legend(title='Species', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('vis2_average_measurements.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: vis2_average_measurements.png")

# ============================================================
# VISUALIZATION 3: Sepal Length vs Sepal Width
# ============================================================
print("\n--- Generating Visualization 3: Sepal Length vs Sepal Width ---")
fig, ax = plt.subplots(figsize=(10, 7))
for species in df['Species'].unique():
    subset = df[df['Species'] == species]
    ax.scatter(subset['SepalLengthCm'], subset['SepalWidthCm'],
               c=IRIS_COLORS[species], label=species, s=80, alpha=0.7, edgecolors='white', linewidth=0.5)
ax.set_title('Sepal Length vs Sepal Width', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Sepal Length (cm)', fontsize=12)
ax.set_ylabel('Sepal Width (cm)', fontsize=12)
ax.legend(title='Species', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('vis3_sepal_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: vis3_sepal_scatter.png")

# ============================================================
# VISUALIZATION 4: Petal Length vs Petal Width
# ============================================================
print("\n--- Generating Visualization 4: Petal Length vs Petal Width ---")
fig, ax = plt.subplots(figsize=(10, 7))
for species in df['Species'].unique():
    subset = df[df['Species'] == species]
    ax.scatter(subset['PetalLengthCm'], subset['PetalWidthCm'],
               c=IRIS_COLORS[species], label=species, s=80, alpha=0.7, edgecolors='white', linewidth=0.5)
ax.set_title('Petal Length vs Petal Width', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Petal Length (cm)', fontsize=12)
ax.set_ylabel('Petal Width (cm)', fontsize=12)
ax.legend(title='Species', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('vis4_petal_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: vis4_petal_scatter.png")

# ============================================================
# VISUALIZATION 5: Boxplots
# ============================================================
print("\n--- Generating Visualization 5: Boxplots ---")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
measurements = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
titles = ['Sepal Length by Species', 'Sepal Width by Species',
          'Petal Length by Species', 'Petal Width by Species']
for idx, (col, title) in enumerate(zip(measurements, titles)):
    ax = axes[idx // 2][idx % 2]
    bp = sns.boxplot(data=df, x='Species', y=col, ax=ax,
                     palette=IRIS_COLORS, width=0.5)
    bp = sns.stripplot(data=df, x='Species', y=col, ax=ax,
                       color='black', alpha=0.3, size=3)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel('Species', fontsize=10)
    ax.set_ylabel('Measurement (cm)', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
plt.suptitle('Measurement Distributions by Species', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('vis5_boxplots.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: vis5_boxplots.png")

# ============================================================
# VISUALIZATION 6: Correlation Heatmap
# ============================================================
print("\n--- Generating Visualization 6: Correlation Heatmap ---")
corr = df[numeric_cols].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt='.3f', cmap='RdYlBu_r',
            center=0, square=True, linewidths=2, ax=ax,
            annot_kws={'size': 12, 'fontweight': 'bold'},
            xticklabels=['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width'],
            yticklabels=['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width'])
ax.set_title('Correlation Heatmap - Iris Measurements', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('vis6_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: vis6_correlation_heatmap.png")

# ============================================================
# VISUALIZATION 7: Pair Plot
# ============================================================
print("\n--- Generating Visualization 7: Pair Plot ---")
pair_plot = sns.pairplot(df, hue='Species', palette=IRIS_COLORS,
                         diag_kind='kde', height=2.5,
                         plot_kws={'alpha': 0.7, 's': 40, 'edgecolor': 'white', 'linewidth': 0.5},
                         diag_kws={'fill': True, 'alpha': 0.5})
pair_plot.figure.suptitle('Iris Dataset - Pair Plot', y=1.02, fontsize=16, fontweight='bold')
pair_plot.savefig('vis7_pairplot.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: vis7_pairplot.png")

# ============================================================
# FINAL OBSERVATIONS
# ============================================================
print("\n" + "=" * 60)
print("FINAL OBSERVATIONS")
print("=" * 60)

print("""
1. SPECIES DISTRIBUTION:
   - All three species have equal representation (50 samples each)
   - Dataset is perfectly balanced

2. SEPAL MEASUREMENTS:
   - Iris-setosa has the shortest sepals (mean: 5.01 cm) but widest sepals (mean: 3.42 cm)
   - Iris-virginica has the longest sepals (mean: 6.59 cm)
   - Sepal measurements show significant overlap between species

3. PETAL MEASUREMENTS:
   - Iris-setosa has dramatically smaller petals (mean length: 1.46 cm, width: 0.24 cm)
   - Iris-virginica has the largest petals (mean length: 5.55 cm, width: 2.03 cm)
   - Petal measurements show clear separation between species

4. PETAL LENGTH vs PETAL WIDTH:
   - Strong positive correlation (r = 0.963)
   - Clear linear relationship within and across species
   - Iris-setosa forms a distinct cluster in the lower-left

5. BEST SEPARATING FEATURES:
   - Petal length and petal width are the best features for distinguishing species
   - Iris-setosa is completely separable from the other two species using petal measurements
   - Iris-versicolor and Iris-virginica show some overlap in sepal measurements but separate well in petal measurements

6. KEY CORRELATIONS:
   - Petal Length and Petal Width: r = 0.963 (very strong positive)
   - Sepal Length and Petal Length: r = 0.872 (strong positive)
   - Sepal Length and Petal Width: r = 0.818 (strong positive)
   - Sepal Width and Petal Length: r = -0.421 (moderate negative)
""")

print("\n" + "=" * 60)
print("ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
print("=" * 60)
