#!/usr/bin/env python3
"""
Example Script: Fraud Risk Model Training, Evaluation, Explainability & Latency Benchmark.

Usage:
    python examples/fraud_risk_model_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hf_core_lab.data.analyzer import DatasetAnalyzer
from hf_core_lab.data.generator import SyntheticFraudDataGenerator
from hf_core_lab.models.fraud_risk import FraudRiskClassifier
from hf_core_lab.utils.files import write_report_to_file


def main():
    print("==================================================")
    print(" Hugging Face Core Lab - Fraud Risk Model Demo ")
    print("==================================================\n")

    # 1. Generate & split dataset
    print("1. Preparing synthetic dataset for model training...")
    df = SyntheticFraudDataGenerator.generate_dataset(num_samples=1200, random_seed=42)
    train_df, val_df, test_df = DatasetAnalyzer.train_val_test_split(df, target_column="is_high_risk")

    # 2. Train model
    print("\n2. Training RandomForestFraudClassifier...")
    model = FraudRiskClassifier(random_seed=42)
    model.train(train_df, target_col="is_high_risk")

    # 3. Evaluate model metrics
    print("\n3. Evaluating model performance on held-out test dataset...")
    eval_report = model.evaluate(test_df, target_col="is_high_risk")

    print(f" - Accuracy: {eval_report.accuracy * 100:.2f}%")
    print(f" - Precision: {eval_report.precision * 100:.2f}%")
    print(f" - Recall: {eval_report.recall * 100:.2f}%")
    print(f" - F1 Score: {eval_report.f1 * 100:.2f}%")
    print(f" - ROC-AUC: {eval_report.roc_auc:.4f}")
    print(f" - CPU Inference Latency: {eval_report.inference_latency_ms:.3f} ms/item")

    # 4. Generate Explainable Prediction
    print("\n4. Predicting sample transaction & generating feature attributions...")
    sample_features = {
        "transaction_amount": 7500.0,
        "is_foreign_country": 1,
        "failed_pin_attempts": 2,
        "account_age_days": 12,
    }
    prob, explanation = model.predict_instance(sample_features)

    print("\n" + explanation.to_markdown())

    # 5. Export Report
    report_path = Path("reports/evaluations/fraud_risk_model_evaluation.md")
    report_content = eval_report.to_markdown() + "\n\n" + explanation.to_markdown()
    write_report_to_file(report_content, report_path)
    print(f"\n[SUCCESS] Model evaluation report exported to: {report_path}")


if __name__ == "__main__":
    main()
