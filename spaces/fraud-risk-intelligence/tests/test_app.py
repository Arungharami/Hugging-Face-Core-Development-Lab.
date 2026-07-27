"""
Unit tests for Gradio Space application processing functions.
"""

import sys
from pathlib import Path

# Add spaces/fraud-risk-intelligence to python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import evaluate_fraud_risk


def test_evaluate_fraud_risk_low():
    category, prob_str, explanation, breakdown = evaluate_fraud_risk(
        transaction_amount=45.50,
        is_foreign_country=False,
        failed_pin_attempts=0,
        account_age_days=365,
        channel="POS Terminal",
    )
    assert category == "Low Risk Tier"
    assert "Standard transaction patterns observed" in explanation
    assert "Transaction Amount" in breakdown


def test_evaluate_fraud_risk_high():
    category, prob_str, explanation, breakdown = evaluate_fraud_risk(
        transaction_amount=12500.0,
        is_foreign_country=True,
        failed_pin_attempts=3,
        account_age_days=7,
        channel="Mobile App",
    )
    assert category == "High Risk Tier"
    assert "elevated risk" in explanation
    assert float(prob_str.replace("%", "")) >= 70.0
