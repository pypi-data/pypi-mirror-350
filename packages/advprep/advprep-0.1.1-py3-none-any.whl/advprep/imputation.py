import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer  # MUST be before IterativeImputer
from sklearn.impute import KNNImputer, IterativeImputer
from typing import Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedImputer:
    """
    Handles missing values in both numerical and categorical columns using various strategies.
    """

    def __init__(self, method: str = "mean", knn_neighbors: int = 5):
        """
        Parameters:
            method (str): Imputation strategy. Options: mean, median, mode, ffill, bfill, knn, iterative
            knn_neighbors (int): Number of neighbors for KNN imputer
        """
        valid_methods = {"mean", "median", "mode", "ffill", "bfill", "knn", "iterative"}
        if method not in valid_methods:
            raise ValueError(f"Unsupported imputation method: {method}")
        self.method = method
        self.knn_neighbors = knn_neighbors
        self.imputer = None
        self.columns = None

    def fit(self, df: pd.DataFrame, columns: Optional[List[str]] = None):
        """
        Fits the imputer on the specified columns.

        Parameters:
            df (pd.DataFrame): The input DataFrame.
            columns (List[str], optional): Specific columns to impute. If None, all numerical columns are selected.
        """
        try:
            self.columns = columns or df.select_dtypes(include=[np.number]).columns.tolist()

            if self.method == "knn":
                self.imputer = KNNImputer(n_neighbors=self.knn_neighbors)
                self.imputer.fit(df[self.columns])
            elif self.method == "iterative":
                self.imputer = IterativeImputer(random_state=42)
                self.imputer.fit(df[self.columns])
        except Exception as e:
            logger.error(f"Error fitting imputer: {e}")
            raise
        return self

    def transform(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Transforms the DataFrame by filling in missing values.

        Parameters:
            df (pd.DataFrame): The input DataFrame.
            columns (List[str], optional): Columns to impute. If None, uses previously fitted columns or infers from df.

        Returns:
            pd.DataFrame: A new DataFrame with missing values filled.
        """
        df_copy = df.copy()
        try:
            cols = columns or self.columns or df.columns.tolist()

            # Split numerical and categorical
            numeric_cols = df_copy[cols].select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df_copy[cols].select_dtypes(include=["object", "category"]).columns.tolist()

            # Numerical
            if self.method in {"knn", "iterative"} and numeric_cols:
                df_copy[numeric_cols] = self.imputer.transform(df_copy[numeric_cols])
            else:
                for col in numeric_cols:
                    if self.method == "mean":
                        df_copy[col] = df_copy[col].fillna(df_copy[col].mean())
                    elif self.method == "median":
                        df_copy[col] = df_copy[col].fillna(df_copy[col].median())
                    elif self.method == "mode":
                        df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])
                    elif self.method == "ffill":
                        df_copy[col] = df_copy[col].fillna(method="ffill")
                    elif self.method == "bfill":
                        df_copy[col] = df_copy[col].fillna(method="bfill")

            # Categorical
            for col in categorical_cols:
                if self.method in {"mode", "ffill", "bfill"}:
                    if self.method == "mode":
                        df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])
                    elif self.method == "ffill":
                        df_copy[col] = df_copy[col].fillna(method="ffill")
                    elif self.method == "bfill":
                        df_copy[col] = df_copy[col].fillna(method="bfill")
                else:
                    logger.warning(f"Method '{self.method}' not supported for categorical column '{col}'. Skipping.")
        except Exception as e:
            logger.error(f"Error transforming data with imputer: {e}")
            raise
        return df_copy

    def fit_transform(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Combines fit and transform steps.

        Parameters:
            df (pd.DataFrame): Input DataFrame.
            columns (List[str], optional): Columns to apply imputation on.

        Returns:
            pd.DataFrame: Transformed DataFrame.
        """
        return self.fit(df, columns).transform(df, columns)
