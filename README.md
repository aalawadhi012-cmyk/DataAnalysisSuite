# Data Analysis Suite

## 📊 Overview
**Data Analysis Suite** is an interactive data analysis system built with **Streamlit**.  
It provides a complete environment for:

- Exploratory Data Analysis (EDA)
- Data preprocessing and cleaning
- Missing value and outlier detection
- Relationship and correlation analysis
- Exporting datasets and analytical reports

The project follows a **modular architecture**, where each analytical stage is implemented as an independent, extensible component.

---

## 🚀 Features

### 1. Data Ingestion
- Upload CSV / Excel / Parquet files
- Automatic file encoding detection
- Dataset stored in a single active session

### 2. Data Overview
- Number of rows and columns
- Data types summary
- Duplicate detection
- Basic descriptive statistics

### 3. Missing Values Analysis
- Missing count and percentage per column
- Detailed summary table
- Clear bar visualization of missing values
- Missing value treatment (Drop / Impute)

### 4. Univariate Analysis
- Single-variable analysis
- Histograms, KDE, and boxplots for numeric variables
- Frequency tables and bar charts for categorical variables
- Statistical metrics (Mean, Median, Std, IQR)

### 5. Outlier Analysis
- Outlier detection using the IQR method
- Boxplot visualization
- Treatment options:
  - Remove outliers
  - Cap values (Winsorization)

### 6. Bivariate Analysis
- Relationship analysis between two variables:
  - Numeric × Numeric
  - Numeric × Categorical
  - Categorical × Categorical
- Scatter plots
- Boxplots
- Aggregated statistical tables

### 7. Correlation Analysis
- Pearson / Spearman / Kendall correlation methods
- Correlation matrix and heatmap
- Identification of highly correlated feature pairs

### 8. Preprocessing
- Numeric and categorical imputation
- One-Hot Encoding
- Feature scaling (Standard, MinMax, Robust)
- Pipelines using ColumnTransformer
- Export of processed datasets

### 9. Export
- Export dataset as CSV
- Export dataset as Excel
- Export analysis report as JSON
- Export full ZIP package (dataset + report)
- User-controlled export selection

### 10. Session Awareness
- Real-time dataset status (loaded / not loaded)
- Display of dataset dimensions
- Ready for pipeline tracking and undo/reset extensions

---

## 🧱 Project Structure

