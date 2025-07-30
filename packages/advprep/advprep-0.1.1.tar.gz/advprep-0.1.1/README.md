# advprep

**advprep** is a Python package offering advanced preprocessing tools for machine learning and deep learning pipelines.

## Features

- Missing value imputation (mean, median, mode, forward/backward fill, KNN)
- Ready for integration into pipelines
- Fast, reliable, and production-ready

## Usage

```python
from advprep import AdvancedImputer
import pandas as pd

df = pd.read_csv("data.csv")
imputer = AdvancedImputer(method="knn")
df_imputed = imputer.fit_transform(df)

