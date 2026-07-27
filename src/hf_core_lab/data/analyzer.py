"""
Dataset Quality Analyzer module.

Provides data quality inspection, missing-value analysis, duplicate detection,
class distribution checking, train/val/test data leakage checks, and split utilities.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

from hf_core_lab.exceptions import ValidationError
from hf_core_lab.logging_config import setup_logger

logger = setup_logger("hf_core_lab.data.analyzer")


@dataclass
class DatasetQualityReport:
    """Summary metrics of a dataset quality audit."""

    total_rows: int
    total_columns: int
    missing_value_counts: Dict[str, int]
    missing_value_ratios: Dict[str, float]
    duplicate_rows: int
    duplicate_ratio: float
    class_distribution: Dict[str, int]
    class_ratios: Dict[str, float]
    potential_leakage_columns: List[str] = field(default_factory=list)

    def is_clean(self, max_missing_ratio: float = 0.05, max_duplicate_ratio: float = 0.01) -> bool:
        """Check if dataset quality metrics pass threshold standards."""
        high_missing = any(r > max_missing_ratio for r in self.missing_value_ratios.values())
        high_duplicates = self.duplicate_ratio > max_duplicate_ratio
        return not (high_missing or high_duplicates or len(self.potential_leakage_columns) > 0)


class DatasetAnalyzer:
    """Quality analyzer for tabular DataFrames."""

    @staticmethod
    def analyze(df: pd.DataFrame, target_column: Optional[str] = None) -> DatasetQualityReport:
        """Perform comprehensive quality analysis on a pandas DataFrame."""
        if df.empty:
            raise ValidationError("Cannot analyze an empty DataFrame.")

        total_rows, total_cols = df.shape
        missing_counts = df.isnull().sum().to_dict()
        missing_ratios = {col: round(count / total_rows, 4) for col, count in missing_counts.items()}

        duplicates = int(df.duplicated().sum())
        duplicate_ratio = round(duplicates / total_rows, 4)

        class_dist: Dict[str, int] = {}
        class_ratios: Dict[str, float] = {}
        if target_column and target_column in df.columns:
            counts = df[target_column].value_counts().to_dict()
            class_dist = {str(k): int(v) for k, v in counts.items()}
            class_ratios = {str(k): round(int(v) / total_rows, 4) for k, v in counts.items()}

        # Detect potential data leakage columns (e.g. unique ID columns with near 1.0 cardinality)
        leakage_cols = []
        for col in df.columns:
            if col != target_column and df[col].nunique() == total_rows and total_rows > 10:
                leakage_cols.append(col)

        return DatasetQualityReport(
            total_rows=total_rows,
            total_columns=total_cols,
            missing_value_counts=missing_counts,
            missing_value_ratios=missing_ratios,
            duplicate_rows=duplicates,
            duplicate_ratio=duplicate_ratio,
            class_distribution=class_dist,
            class_ratios=class_ratios,
            potential_leakage_columns=leakage_cols,
        )

    @staticmethod
    def train_val_test_split(
        df: pd.DataFrame,
        target_column: str,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_seed: int = 42,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Perform reproducible train, validation, and test split."""
        if not np.isclose(train_ratio + val_ratio + test_ratio, 1.0):
            raise ValidationError("Split ratios must sum to 1.0.")

        if target_column not in df.columns:
            raise ValidationError(f"Target column '{target_column}' not found in DataFrame.")

        np.random.seed(random_seed)
        shuffled = df.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)

        n_total = len(shuffled)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)

        train_df = shuffled.iloc[:n_train].reset_index(drop=True)
        val_df = shuffled.iloc[n_train : n_train + n_val].reset_index(drop=True)
        test_df = shuffled.iloc[n_train + n_val :].reset_index(drop=True)

        logger.info(
            "Split dataset into Train (%d rows), Val (%d rows), Test (%d rows)",
            len(train_df),
            len(val_df),
            len(test_df),
        )
        return train_df, val_df, test_df
