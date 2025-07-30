import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from category_encoders import TargetEncoder
from typing import Optional, List

class AdvancedEncoder:
    """
    Handles One-Hot, Ordinal, and Target encoding.
    """

    def __init__(self, method: str = "onehot", drop_first: bool = True):
        if method not in {"onehot", "ordinal", "target"}:
            raise ValueError(f"Invalid encoding method: {method}")
        self.method = method
        self.drop_first = drop_first
        self.encoder = None

    def fit(self, df: pd.DataFrame, columns: Optional[List[str]] = None, target: Optional[str] = None):
        try:
            columns = columns or df.select_dtypes(include=['object', 'category']).columns.tolist()

            if self.method == "ordinal":
                self.encoder = OrdinalEncoder()
                self.encoder.fit(df[columns])
            elif self.method == "target":
                if not target:
                    raise ValueError("Target must be provided for target encoding.")
                self.encoder = TargetEncoder(cols=columns)
                self.encoder.fit(df[columns], df[target])
            return self
        except Exception as e:
            raise RuntimeError(f"Error fitting encoder: {e}")

    def transform(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        try:
            columns = columns or df.select_dtypes(include=['object', 'category']).columns.tolist()
            df_copy = df.copy()

            if self.method == "onehot":
                return pd.get_dummies(df_copy, columns=columns, drop_first=self.drop_first)
            elif self.method in {"ordinal", "target"}:
                df_copy[columns] = self.encoder.transform(df_copy[columns])
                return df_copy
        except Exception as e:
            raise RuntimeError(f"Error transforming with encoder: {e}")

    def fit_transform(self, df: pd.DataFrame, columns: Optional[List[str]] = None, target: Optional[str] = None) -> pd.DataFrame:
        return self.fit(df, columns, target).transform(df, columns)

    def __repr__(self):
        return f"{self.__class__.__name__}(method={self.method}, drop_first={self.drop_first})"
