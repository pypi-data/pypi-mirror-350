# FeatureLab

**FeatureLab** is a comprehensive Python package for feature engineering, offering statistical guidance and a suite of tools to streamline data preprocessing for machine learning projects.

---

## Features

- **Automatic Feature Type Detection:** Identify numeric, categorical, datetime, and text columns in your DataFrame.
- **Missing Value Visualization:** Visualize missing data patterns and distributions.
- **Outlier Visualization:** Easily spot and analyze outliers.
- **Feature Importance Plotting:** Visualize feature importance scores for model interpretability.
- **Correlation Matrix Heatmaps:** Explore feature correlations visually.
- **PCA & RFE Visualization:** Understand dimensionality reduction and feature selection results.
- **Memory Optimization:** Reduce DataFrame memory usage efficiently.
- **Datetime Feature Expansion:** Extract year, month, day, and more from datetime columns.
- **Categorical Distribution Plots:** Visualize the distribution of categorical features.
- **Duplicate Row Visualization:** Detect and visualize duplicate rows.
- **Easy Integration:** Designed to work seamlessly with pandas DataFrames.

---

## Installation

Clone the repository and install with pip:

```bash
git clone https://github.com/yourusername/featurelab.git
cd featurelab
pip install .
```

Or install directly if distributed on PyPI:

```bash
pip install featurelab
```

---

## Requirements

- Python >= 3.7
- numpy >= 1.20.0
- pandas >= 1.2.0
- scipy >= 1.6.0
- scikit-learn >= 0.24.0
- matplotlib >= 3.3.0
- seaborn >= 0.11.0
- missingno >= 0.4.2

---

## Usage

### Python API

```python
import pandas as pd
from featurelab.utils import FeatureUtils
from featurelab.visualizer import Visualizer

df = pd.read_csv("your_data.csv")

# Detect column types
col_types = FeatureUtils.detect_column_types(df)
print(col_types)

# Optimize memory usage
df_optimized = FeatureUtils.memory_optimize(df)

# Visualize missing values
viz = Visualizer()
viz.plot_null_matrix(df)

# Plot feature importance (example)
# importance_scores = ... # pd.Series with feature importances
# viz.plot_feature_importance(importance_scores)
```

### CLI (if implemented)

```bash
featurelab --help
```

---

## Project Structure




---

## Author

Shekhar Suman  
[s.sumanpathak513@gmail.com](mailto:s.sumanpathak513@gmail.com)

---

## License

MIT License

---

## Keywords

feature-engineering, data-preprocessing, machine-learning, pandas, visualization

---