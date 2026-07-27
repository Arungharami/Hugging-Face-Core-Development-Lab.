"""
Unit tests for HubDiscoveryEngine.
"""

from unittest.mock import MagicMock

import pytest

from hf_core_lab.exceptions import DiscoveryError
from hf_core_lab.hub.discovery import HubDiscoveryEngine


def test_search_models_invalid_limit():
    engine = HubDiscoveryEngine()
    with pytest.raises(DiscoveryError):
        engine.search_models(limit=0)

    with pytest.raises(DiscoveryError):
        engine.search_models(limit=500)


def test_search_models_success():
    mock_api = MagicMock()
    mock_item = MagicMock()
    mock_item.id = "meta-llama/Llama-3.2-1B"
    mock_item.author = "meta-llama"
    mock_item.downloads = 50000
    mock_item.likes = 1200
    mock_item.tags = ["text-generation", "license:mit"]
    mock_item.pipeline_tag = "text-generation"
    mock_item.library_name = "transformers"
    mock_item.last_modified = "2026-01-01"
    mock_item.sha = "12345"

    mock_api.list_models.return_value = [mock_item]

    engine = HubDiscoveryEngine(api=mock_api)
    models = engine.search_models(query="llama", limit=5)

    assert len(models) == 1
    assert models[0].model_id == "meta-llama/Llama-3.2-1B"
    assert models[0].license == "mit"
    assert models[0].downloads == 50000


def test_search_datasets_success():
    mock_api = MagicMock()
    mock_item = MagicMock()
    mock_item.id = "financial_fraud_synthetic"
    mock_item.author = "arun-gharami"
    mock_item.downloads = 300
    mock_item.likes = 15
    mock_item.tags = ["license:cc-by-4.0"]
    mock_item.description = "Synthetic financial transactions dataset"
    mock_item.last_modified = "2026-02-01"

    mock_api.list_datasets.return_value = [mock_item]

    engine = HubDiscoveryEngine(api=mock_api)
    datasets = engine.search_datasets(query="finance", limit=5)

    assert len(datasets) == 1
    assert datasets[0].dataset_id == "financial_fraud_synthetic"
    assert datasets[0].license == "cc-by-4.0"


def test_search_spaces_success():
    mock_api = MagicMock()
    mock_item = MagicMock()
    mock_item.id = "arun-gharami/fraud-risk-intelligence"
    mock_item.author = "arun-gharami"
    mock_item.sdk = "gradio"
    mock_item.likes = 42
    mock_item.tags = ["fraud-risk"]
    mock_item.last_modified = "2026-03-01"

    mock_api.list_spaces.return_value = [mock_item]

    engine = HubDiscoveryEngine(api=mock_api)
    spaces = engine.search_spaces(query="fraud", limit=5)

    assert len(spaces) == 1
    assert spaces[0].space_id == "arun-gharami/fraud-risk-intelligence"
    assert spaces[0].sdk == "gradio"
