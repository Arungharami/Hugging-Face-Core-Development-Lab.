"""
Model Monetization & Commercial API Billing Engine.

Manages API key quotas (Free vs Pro Tier), cost calculations ($5.00 / 1,000 predictions),
usage tracking, and Hugging Face Inference Endpoint payload integration.
"""

import hashlib
from dataclasses import dataclass
from typing import Any

from hf_core_lab.exceptions import ValidationError
from hf_core_lab.logging_config import setup_logger

logger = setup_logger("hf_core_lab.models.monetization")


@dataclass
class QuotaTier:
    """Definition of API usage quota tier."""

    name: str
    daily_limit: int
    cost_per_request: float
    requires_api_key: bool


@dataclass
class UsageBillingReport:
    """Billing summary report for API request consumption."""

    api_key_hash: str
    tier_name: str
    total_requests: int
    billable_requests: int
    total_cost_usd: float
    remaining_quota: int

    def to_markdown(self) -> str:
        """Format billing report as markdown summary."""
        return (
            f"### Commercial API Billing Summary\n"
            f"- **Quota Tier:** `{self.tier_name}`\n"
            f"- **Total Requests Processed:** `{self.total_requests:,}`\n"
            f"- **Billable Requests:** `{self.billable_requests:,}`\n"
            f"- **Calculated Usage Cost:** `${self.total_cost_usd:.4f} USD`\n"
            f"- **Remaining Daily Quota:** `{self.remaining_quota:,}`\n"
        )


class MonetizationEngine:
    """Commercial API quota and billing engine."""

    TIER_FREE = QuotaTier(name="Free Tier", daily_limit=100, cost_per_request=0.0, requires_api_key=False)
    TIER_PRO = QuotaTier(name="Pro Tier", daily_limit=100000, cost_per_request=0.005, requires_api_key=True)

    def __init__(self, price_per_1k_requests: float = 5.00):
        self.price_per_request = price_per_1k_requests / 1000.0
        self.usage_records: dict[str, int] = {}

    def validate_api_key(self, api_key: str | None) -> QuotaTier:
        """Validate provided API key and return corresponding QuotaTier."""
        if not api_key or not api_key.startswith("hflab_pro_"):
            return self.TIER_FREE
        return self.TIER_PRO

    def process_request(self, api_key: str | None, num_predictions: int = 1) -> UsageBillingReport:
        """Process API prediction request, track quota, and compute billing."""
        if num_predictions <= 0:
            raise ValidationError("Number of predictions must be greater than zero.")

        tier = self.validate_api_key(api_key)
        key_id = hashlib.sha256((api_key or "anonymous").encode()).hexdigest()[:12]

        current_usage = self.usage_records.get(key_id, 0)
        new_usage = current_usage + num_predictions

        if new_usage > tier.daily_limit:
            raise ValidationError(
                f"Daily request quota exceeded for {tier.name} ({current_usage}/{tier.daily_limit}). Upgrade to Pro Tier."
            )

        self.usage_records[key_id] = new_usage

        billable = num_predictions if tier.requires_api_key else 0
        total_cost = round(billable * self.price_per_request, 4)
        remaining = max(0, tier.daily_limit - new_usage)

        logger.info(
            "Processed %d predictions under %s (Cost: $%s USD).",
            num_predictions,
            tier.name,
            total_cost,
        )

        return UsageBillingReport(
            api_key_hash=key_id,
            tier_name=tier.name,
            total_requests=new_usage,
            billable_requests=billable,
            total_cost_usd=total_cost,
            remaining_quota=remaining,
        )

    def estimate_cost(self, num_requests: int) -> dict[str, Any]:
        """Estimate billing cost for a given volume of requests."""
        cost = round(num_requests * self.price_per_request, 2)
        return {
            "num_requests": num_requests,
            "cost_per_request": self.price_per_request,
            "estimated_cost_usd": cost,
            "price_per_1k": self.price_per_request * 1000,
        }
