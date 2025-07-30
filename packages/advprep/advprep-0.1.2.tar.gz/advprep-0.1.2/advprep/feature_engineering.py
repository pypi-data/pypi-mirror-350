import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from typing import List

class FeatureEngineer:
    """
    Feature engineering utilities for temporal and polynomial features.
    """

    @staticmethod
    def extract_date_features(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        try:
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            df_copy["year"] = df_copy[date_column].dt.year
            df_copy["month"] = df_copy[date_column].dt.month
            df_copy["day"] = df_copy[date_column].dt.day
            df_copy["weekday"] = df_copy[date_column].dt.weekday
            df_copy["hour"] = df_copy[date_column].dt.hour
            return df_copy
        except Exception as e:
            raise RuntimeError(f"Error extracting date features: {e}")

    @staticmethod
    def generate_polynomial_features(df: pd.DataFrame, columns: List[str], degree: int = 2) -> pd.DataFrame:
        try:
            poly = PolynomialFeatures(degree=degree, include_bias=False)
            poly_features = poly.fit_transform(df[columns])
            feature_names = poly.get_feature_names_out(columns)
            poly_df = pd.DataFrame(poly_features, columns=feature_names, index=df.index)
            return pd.concat([df.drop(columns=columns), poly_df], axis=1)
        except Exception as e:
            raise RuntimeError(f"Error generating polynomial features: {e}")
