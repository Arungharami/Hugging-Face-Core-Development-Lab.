"""
Unit tests for DatasetAnalyzer, SyntheticFraudDataGenerator, and DatasetCardGenerator.
"""

import pandas as pd
import pytest

from hf_core_lab.data.analyzer import DatasetAnalyzer
from hf_core_lab.data.card_generator import DatasetCardGenerator
from hf_core_lab.data.generator import SyntheticFraudDataGenerator
from hf_core_lab.exceptions import ValidationError


def test_generate_synthetic_dataset():
    df = SyntheticFraudDataGenerator.generate_dataset(num_samples=100, random_seed=42)
    assert len(df) == 100
    assert "transaction_amount" in df.columns
    assert "is_high_risk" in df.columns


def test_dataset_analyzer_empty_df():
    with pytest.raises(ValidationError):
        DatasetAnalyzer.analyze(pd.DataFrame())


def test_dataset_analyzer_quality():
    df = SyntheticFraudDataGenerator.generate_dataset(num_samples=200, random_seed=42)
    report = DatasetAnalyzer.analyze(df, target_column="is_high_risk")

    assert report.total_rows == 200
    assert report.total_columns == 7
    assert report.duplicate_rows == 0
    assert "transaction_id" in report.potential_leakage_columns


def test_train_val_test_split_success():
    df = SyntheticFraudDataGenerator.generate_dataset(num_samples=100, random_seed=42)
    train_df, val_df, test_df = DatasetAnalyzer.train_val_test_split(df, target_column="is_high_risk")

    assert len(train_df) == 70
    assert len(val_df) == 15
    assert len(test_df) == 15


def test_train_val_test_split_invalid_ratios():
    df = SyntheticFraudDataGenerator.generate_dataset(num_samples=100)
    with pytest.raises(ValidationError):
        DatasetAnalyzer.train_val_test_split(df, target_column="is_high_risk", train_ratio=0.5, val_ratio=0.2, test_ratio=0.2)


def test_dataset_card_generator():
    df = SyntheticFraudDataGenerator.generate_dataset(num_samples=100, random_seed=42)
    report = DatasetAnalyzer.analyze(df, target_column="is_high_risk")
    card_md = DatasetCardGenerator.generate_card("test_dataset", report)

    assert "# Dataset Card for test_dataset" in card_md
    assert "## Ethical Use & Governance Specification" in card_md
