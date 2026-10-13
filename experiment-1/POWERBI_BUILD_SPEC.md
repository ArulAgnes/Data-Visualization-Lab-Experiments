# Power BI Build Specification - Iris Dataset Analytics Dashboard

## Overview

This document provides detailed instructions for building the Iris Dataset Analytics Dashboard in Power BI Desktop.

## Data Source

- **File:** Iris.csv
- **Rows:** 150
- **Columns:** 6

### Column Specifications

| Column | Data Type | Description |
|--------|-----------|-------------|
| Id | Whole Number | Unique identifier (1-150) |
| SepalLengthCm | Decimal Number | Sepal length in centimeters |
| SepalWidthCm | Decimal Number | Sepal width in centimeters |
| PetalLengthCm | Decimal Number | Petal length in centimeters |
| PetalWidthCm | Decimal Number | Petal width in centimeters |
| Species | Text | Flower species |

## DAX Measures

Create the following measures in Power BI:

### Core Measures

```dax
Total Flowers = COUNTROWS(Iris)

Species Count = DISTINCTCOUNT(Iris[Species])

Average Sepal Length = AVERAGE(Iris[SepalLengthCm])

Average Sepal Width = AVERAGE(Iris[SepalWidthCm])

Average Petal Length = AVERAGE(Iris[PetalLengthCm])

Average Petal Width = AVERAGE(Iris[PetalWidthCm])
```

### Species-Specific Measures

```dax
Setosa Count =
CALCULATE(
    [Total Flowers],
    Iris[Species] = "Iris-setosa"
)

Versicolor Count =
CALCULATE(
    [Total Flowers],
    Iris[Species] = "Iris-versicolor"
)

Virginica Count =
CALCULATE(
    [Total Flowers],
    Iris[Species] = "Iris-virginica"
)
```

## Dashboard Layout

### Page Settings
- **Size:** 16:9 Widescreen
- **Background:** Light gray (#F5F7FA)

### Header Section
- **Title:** "IRIS DATASET ANALYTICS"
  - Font: Segoe UI Semibold, 24pt, Dark gray
- **Subtitle:** "Exploratory Data Analysis of Iris Flower Measurements"
  - Font: Segoe UI, 12pt, Medium gray
- **Source:** "Source: Kaggle - UCI ML Iris Dataset"
  - Font: Segoe UI, 8pt, Light gray

### KPI Cards (Top Row)
Four cards in a horizontal row:

1. **Total Flowers**
   - Value: [Total Flowers]
   - Format: Whole number

2. **Species**
   - Value: [Species Count]
   - Format: Whole number

3. **Avg Sepal Length**
   - Value: [Average Sepal Length]
   - Format: 2 decimal places + " cm"

4. **Avg Petal Length**
   - Value: [Average Petal Length]
   - Format: 2 decimal places + " cm"

### Chart Specifications

#### Chart 1: Species Distribution
- **Type:** Clustered Column Chart
- **Axis:** Species
- **Values:** Total Flowers
- **Title:** "Species Distribution"
- **Colors:** Blue (#2196F3), Green (#4CAF50), Orange (#FF9800)

#### Chart 2: Average Measurements by Species
- **Type:** Clustered Bar Chart
- **Axis:** Species
- **Values:** Average Sepal Length, Average Sepal Width, Average Petal Length, Average Petal Width
- **Title:** "Average Measurements by Species"
- **Legend:** Measurement type

#### Chart 3: Sepal Length vs Sepal Width
- **Type:** Scatter Chart
- **X Axis:** SepalLengthCm
- **Y Axis:** SepalWidthCm
- **Legend:** Species
- **Title:** "Sepal Length vs Sepal Width"

#### Chart 4: Petal Length vs Petal Width
- **Type:** Scatter Chart
- **X Axis:** PetalLengthCm
- **Y Axis:** PetalWidthCm
- **Legend:** Species
- **Title:** "Petal Length vs Petal Width"

#### Chart 5: Box Plots
- **Type:** Box and Whisker Plot (or Python visual)
- **Category:** Species
- **Values:** SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm
- **Title:** "Measurement Distributions by Species"

#### Chart 6: Correlation Heatmap
- **Type:** Python Visual or Matrix
- **Rows/Columns:** Measurement names
- **Values:** Correlation coefficients
- **Title:** "Correlation Heatmap"

### Slicer

- **Type:** List Slicer
- **Field:** Species
- **Multi-select:** Enabled
- **Select All:** Enabled

### Interactions

- Configure cross-filtering between all visuals
- Slicer should filter all charts
- Scatter plots should cross-filter other visuals on click

### Theme

Import `Iris_PowerBI_Theme.json` for consistent styling.

## Verification Checklist

- [ ] 150 rows loaded
- [ ] 6 columns with correct data types
- [ ] All 9 DAX measures created
- [ ] 4 KPI cards displaying correctly
- [ ] Species Distribution chart working
- [ ] Average Measurements chart working
- [ ] Both scatter plots working
- [ ] Box plots showing distributions
- [ ] Correlation heatmap displaying
- [ ] Slicer filtering all visuals
- [ ] Cross-filtering enabled
- [ ] Theme applied
- [ ] No error visuals
- [ ] All tooltips configured
