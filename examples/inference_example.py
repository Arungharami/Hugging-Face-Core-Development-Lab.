#!/usr/bin/env python3
"""
Example Script: Performing local batch inference and measuring execution latency.

Usage:
    python examples/inference_example.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hf_core_lab.logging_config import setup_logger

logger = setup_logger("examples.inference_example")


def mock_tabular_inference(input_features: dict) -> dict:
    """Mock rule/ML model predicting fraud risk score."""
    amount = input_features.get("transaction_amount", 0.0)
    is_foreign = input_features.get("is_foreign_country", 0)
    failed_attempts = input_features.get("failed_pin_attempts", 0)

    # Simple heuristic risk calculation for baseline demonstration
    risk_score = min(1.0, (amount / 10000.0) * 0.4 + (is_foreign * 0.35) + (failed_attempts * 0.25))

    if risk_score < 0.35:
        category = "Low Risk"
        advisory = "Standard transaction processing."
    elif risk_score < 0.70:
        category = "Medium Risk"
        advisory = "Pattern presents moderate risk. Flagged for secondary verification."
    else:
        category = "High Risk"
        advisory = "This transaction presents patterns associated with elevated risk and should be reviewed by an authorized human analyst."

    return {
        "risk_probability": round(risk_score, 4),
        "risk_category": category,
        "advisory": advisory,
    }


def main():
    print("==================================================")
    print(" Hugging Face Core Lab - Baseline Inference Demo ")
    print("==================================================\n")

    sample_transactions = [
        {"transaction_id": "TX1001", "transaction_amount": 45.50, "is_foreign_country": 0, "failed_pin_attempts": 0},
        {"transaction_id": "TX1002", "transaction_amount": 4500.00, "is_foreign_country": 1, "failed_pin_attempts": 1},
        {"transaction_id": "TX1003", "transaction_amount": 12500.00, "is_foreign_country": 1, "failed_pin_attempts": 3},
    ]

    start_time = time.perf_counter()
    for tx in sample_transactions:
        res = mock_tabular_inference(tx)
        print(f"ID: {tx['transaction_id']} | Amount: ${tx['transaction_amount']:,.2f}")
        print(f" -> Category: {res['risk_category']} (Score: {res['risk_probability']})")
        print(f" -> Advisory: {res['advisory']}\n")

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    print(f"Total Batch Inference Latency: {elapsed_ms:.2f} ms ({elapsed_ms / len(sample_transactions):.2f} ms/item)")


if __name__ == "__main__":
    main()
