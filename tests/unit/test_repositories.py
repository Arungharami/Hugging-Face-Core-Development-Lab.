"""
Unit tests for RepositoryManager.
"""

from unittest.mock import MagicMock

import pytest

from hf_core_lab.exceptions import HubConnectionError
from hf_core_lab.hub.repositories import RepositoryManager


def test_create_repo_success():
    mock_api = MagicMock()
    mock_api.create_repo.return_value = "https://huggingface.co/arun-gharami/test-model"

    manager = RepositoryManager(api=mock_api)
    url = manager.create_repo("arun-gharami/test-model", repo_type="model", private=True)

    assert url == "https://huggingface.co/arun-gharami/test-model"
    mock_api.create_repo.assert_called_once_with(
        repo_id="arun-gharami/test-model", repo_type="model", private=True, exist_ok=True
    )


def test_create_repo_failure():
    mock_api = MagicMock()
    mock_api.create_repo.side_effect = Exception("Permission denied")

    manager = RepositoryManager(api=mock_api)
    with pytest.raises(HubConnectionError):
        manager.create_repo("invalid/repo")
