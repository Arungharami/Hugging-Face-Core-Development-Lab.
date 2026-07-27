"""
Synthetic Financial Transaction Dataset Generator.

Generates audited, reproducible synthetic tabular data for financial fraud risk decision support.
"""

import numpy as np
import pandas as pd

from hf_core_lab.logging_config import setup_logger

logger = setup_logger("hf_core_lab.data.generator")


class SyntheticFraudDataGenerator:
    """Generator for synthetic financial transaction datasets."""

    @staticmethod
    def generate_dataset(num_samples: int = 1000, random_seed: int = 42) -> pd.DataFrame:
        """Generate reproducible synthetic DataFrame with transaction features and risk labels."""
        np.random.seed(random_seed)

        transaction_ids = [f"TX_{100000 + i}" for i in range(num_samples)]
        amounts = np.round(np.random.exponential(scale=150.0, size=num_samples) + 5.0, 2)
        # Inject occasional large transaction amounts
        large_indices = np.random.choice(num_samples, size=int(num_samples * 0.05), replace=False)
        amounts[large_indices] = np.round(np.random.uniform(3000.0, 15000.0, size=len(large_indices)), 2)

        is_foreign = np.random.binomial(n=1, p=0.15, size=num_samples)
        failed_pin = np.random.choice([0, 1, 2, 3], size=num_samples, p=[0.80, 0.12, 0.05, 0.03])
        account_age_days = np.random.randint(1, 1000, size=num_samples)
        channel = np.random.choice(["Online Web", "Mobile App", "POS Terminal", "ATM"], size=num_samples, p=[0.4, 0.35, 0.2, 0.05])

        # Generate synthetic target label (0 = Low/Normal Risk, 1 = Elevated Risk Pattern)
        risk_score = (
            (amounts / 10000.0) * 0.35
            + (is_foreign * 0.30)
            + (failed_pin / 3.0) * 0.25
            + np.where(account_age_days < 30, 0.10, 0.0)
            + np.random.normal(0, 0.05, size=num_samples)
        )
        is_high_risk = (risk_score >= 0.40).astype(int)

        df = pd.DataFrame({
            "transaction_id": transaction_ids,
            "transaction_amount": amounts,
            "is_foreign_country": is_foreign,
            "failed_pin_attempts": failed_pin,
            "account_age_days": account_age_days,
            "channel": channel,
            "is_high_risk": is_high_risk,
        })

        logger.info("Generated %d synthetic transactions (%d elevated risk instances).", num_samples, is_high_risk.sum())
        return df
