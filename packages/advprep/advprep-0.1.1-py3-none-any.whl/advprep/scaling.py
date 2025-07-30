import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, PowerTransformer
from typing import Optional, List

class AdvancedScaler:
    """
    Feature scaling using multiple strategies.
    """

    def __init__(self, method: str = "standard"):
        if method not in {"standard", "minmax", "robust", "power"}:
            raise ValueError(f"Invalid scaling method: {method}")
        self.method = method
        self.scaler = None

    def fit(self, df: pd.DataFrame, columns: Optional[List[str]] = None):
        try:
            columns = columns or df.select_dtypes(include=['number']).columns.tolist()
            scaler_map = {
                "standard": StandardScaler,
                "minmax": MinMaxScaler,
                "robust": RobustScaler,
                "power": PowerTransformer
            }
            self.scaler = scaler_map[self.method]()
            self.scaler.fit(df[columns])
            return self
        except Exception as e:
            raise RuntimeError(f"Error fitting scaler: {e}")

    def transform(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        try:
            columns = columns or df.select_dtypes(include=['number']).columns.tolist()
            df_copy = df.copy()
            df_copy[columns] = self.scaler.transform(df_copy[columns])
            return df_copy
        except Exception as e:
            raise RuntimeError(f"Error transforming with scaler: {e}")

    def fit_transform(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        return self.fit(df, columns).transform(df, columns)

    def __repr__(self):
        return f"{self.__class__.__name__}(method={self.method})"
