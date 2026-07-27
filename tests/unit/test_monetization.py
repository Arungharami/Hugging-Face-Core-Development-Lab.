"""
Unit tests for MonetizationEngine.
"""

import pytest

from hf_core_lab.exceptions import ValidationError
from hf_core_lab.models.monetization import MonetizationEngine


def test_validate_api_key():
    engine = MonetizationEngine()
    free_tier = engine.validate_api_key(None)
    assert free_tier.name == "Free Tier"
    assert free_tier.cost_per_request == 0.0

    pro_tier = engine.validate_api_key("hflab_pro_secret123")
    assert pro_tier.name == "Pro Tier"
    assert pro_tier.cost_per_request > 0.0


def test_process_request_free():
    engine = MonetizationEngine()
    report = engine.process_request(api_key=None, num_predictions=10)
    assert report.tier_name == "Free Tier"
    assert report.billable_requests == 0
    assert report.total_cost_usd == 0.0
    assert "Commercial API Billing Summary" in report.to_markdown()


def test_process_request_pro():
    engine = MonetizationEngine(price_per_1k_requests=5.00)
    report = engine.process_request(api_key="hflab_pro_secret123", num_predictions=1000)
    assert report.tier_name == "Pro Tier"
    assert report.billable_requests == 1000
    assert report.total_cost_usd == 5.00


def test_process_request_invalid_count():
    engine = MonetizationEngine()
    with pytest.raises(ValidationError):
        engine.process_request(api_key=None, num_predictions=0)


def test_estimate_cost():
    engine = MonetizationEngine(price_per_1k_requests=5.00)
    est = engine.estimate_cost(num_requests=2000)
    assert est["estimated_cost_usd"] == 10.00
    assert est["price_per_1k"] == 5.00
