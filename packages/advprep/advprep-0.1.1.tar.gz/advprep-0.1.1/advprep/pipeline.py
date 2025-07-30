
import pandas as pd
from typing import List, Any
import logging

logging.basicConfig(level=logging.INFO)

class PreprocessingPipeline:
    """
    Flexible pipeline for chaining preprocessing steps.
    """

    def __init__(self, steps: List[Any]):
        self.steps = steps

    def fit(self, df: pd.DataFrame):
        try:
            for step in self.steps:
                if hasattr(step, 'fit'):
                    logging.info(f"Fitting: {step}")
                    step.fit(df)
            return self
        except Exception as e:
            raise RuntimeError(f"Error during pipeline fitting: {e}")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            for step in self.steps:
                logging.info(f"Applying: {step}")
                df = step.transform(df)
            return df
        except Exception as e:
            raise RuntimeError(f"Error during pipeline transform: {e}")

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)

    def __repr__(self):
        return f"{self.__class__.__name__}(steps={[str(step) for step in self.steps]})"
