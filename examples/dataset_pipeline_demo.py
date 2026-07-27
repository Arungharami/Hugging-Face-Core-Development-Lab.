#!/usr/bin/env python3
"""
Example Script: Reproducible Dataset Quality Pipeline & Card Generation.

Usage:
    python examples/dataset_pipeline_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hf_core_lab.data.analyzer import DatasetAnalyzer
from hf_core_lab.data.card_generator import DatasetCardGenerator
from hf_core_lab.data.generator import SyntheticFraudDataGenerator
from hf_core_lab.utils.files import write_report_to_file


def main():
    print("==================================================")
    print(" Hugging Face Core Lab - Dataset Pipeline Demo ")
    print("==================================================\n")

    # 1. Generate synthetic dataset
    print("1. Generating synthetic financial transaction dataset (N=1,000)...")
    df = SyntheticFraudDataGenerator.generate_dataset(num_samples=1000, random_seed=42)

    # 2. Analyze quality metrics
    print("\n2. Executing quality analysis (missing values, duplicates, class distribution)...")
    report = DatasetAnalyzer.analyze(df, target_column="is_high_risk")

    print(f" - Total Rows: {report.total_rows:,}")
    print(f" - Total Columns: {report.total_columns}")
    print(f" - Duplicates: {report.duplicate_rows} ({report.duplicate_ratio * 100:.2f}%)")
    print(f" - Class Distribution: {report.class_distribution}")

    # 3. Train, Validation, Test Split
    print("\n3. Splitting dataset into Train (70%), Val (15%), Test (15%)...")
    train_df, val_df, test_df = DatasetAnalyzer.train_val_test_split(df, target_column="is_high_risk")
    print(f" - Train: {len(train_df)} rows | Val: {len(val_df)} rows | Test: {len(test_df)} rows")

    # 4. Generate Hugging Face Dataset Card
    print("\n4. Generating Hugging Face Dataset Card...")
    card_md = DatasetCardGenerator.generate_card(
        dataset_name="financial_fraud_risk_synthetic",
        report=report,
        license_name="mit",
        author="Arun Kumar Gharami",
    )

    output_path = Path("reports/datasets/financial_fraud_dataset_card.md")
    write_report_to_file(card_md, output_path)
    print(f"\n[SUCCESS] Dataset card exported to: {output_path}")


if __name__ == "__main__":
    main()
