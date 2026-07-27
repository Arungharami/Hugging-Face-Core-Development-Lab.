"""
Unit tests for FraudRiskClassifier and FeatureExplainer.
"""

import pytest
from hf_core_lab.data.analyzer import DatasetAnalyzer
from hf_core_lab.data.generator import SyntheticFraudDataGenerator
from hf_core_lab.exceptions import InferenceError, ValidationError
from hf_core_lab.models.explainability import FeatureExplainer
from hf_core_lab.models.fraud_risk import FraudRiskClassifier


def test_fraud_risk_classifier_train_and_evaluate():
    df = SyntheticFraudDataGenerator.generate_dataset(num_samples=300, random_seed=42)
    train_df, val_df, test_df = DatasetAnalyzer.train_val_test_split(df, target_column="is_high_risk")

    classifier = FraudRiskClassifier(random_seed=42)
    classifier.train(train_df, target_col="is_high_risk")

    assert classifier.is_trained is True

    report = classifier.evaluate(test_df, target_col="is_high_risk")
    assert report.accuracy > 0.5
    assert report.roc_auc >= 0.0
    assert report.inference_latency_ms >= 0.0
    assert "Model Evaluation Summary" in report.to_markdown()


def test_fraud_risk_classifier_evaluate_untrained():
    df = SyntheticFraudDataGenerator.generate_dataset(num_samples=50)
    classifier = FraudRiskClassifier()
    with pytest.raises(InferenceError):
        classifier.evaluate(df)


def test_fraud_risk_classifier_predict_instance():
    classifier = FraudRiskClassifier()
    sample = {
        "transaction_amount": 5000.0,
        "is_foreign_country": 1,
        "failed_pin_attempts": 2,
        "account_age_days": 10,
    }
    prob, exp = classifier.predict_instance(sample)
    assert 0.0 <= prob <= 1.0
    assert exp.risk_category in ["Low Risk Tier", "Medium Risk Tier", "High Risk Tier"]
    assert "Explainable Risk Advisory Report" in exp.to_markdown()


def test_feature_explainer():
    features = {"transaction_amount": 100.0, "is_foreign_country": 0}
    coeffs = {"transaction_amount": 0.5, "is_foreign_country": 0.5}

    exp = FeatureExplainer.explain_instance(features, coeffs, 0.20)
    assert exp.risk_category == "Low Risk Tier"
    assert exp.feature_attributions["transaction_amount"] == 100.0
