"""
Unit tests wrapper for Gradio Space application logic.
"""

import sys
from pathlib import Path

space_path = Path(__file__).parent.parent.parent / "spaces" / "fraud-risk-intelligence"
sys.path.insert(0, str(space_path))

from app import evaluate_fraud_risk


def test_space_processing_function_low_risk():
    category, prob_str, explanation, breakdown = evaluate_fraud_risk(
        transaction_amount=50.0,
        is_foreign_country=False,
        failed_pin_attempts=0,
        account_age_days=180,
        channel="POS Terminal",
    )
    assert category == "Low Risk Tier"
    assert "Transaction Amount" in breakdown


def test_space_processing_function_high_risk():
    category, prob_str, explanation, breakdown = evaluate_fraud_risk(
        transaction_amount=15000.0,
        is_foreign_country=True,
        failed_pin_attempts=3,
        account_age_days=5,
        channel="Online Web",
    )
    assert category == "High Risk Tier"
    assert "elevated risk" in explanation
