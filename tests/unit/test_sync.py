"""
Unit tests for HubSyncManager with mocked HfApi calls.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from hf_core_lab.exceptions import HubConnectionError
from hf_core_lab.hub.sync import HubSyncManager


def test_sync_directory_non_existent():
    manager = HubSyncManager()
    with pytest.raises(HubConnectionError):
        manager.sync_directory(local_dir="/non/existent/path/xyz", repo_id="test/repo")


def test_sync_directory_success(tmp_path: Path):
    mock_api = MagicMock()
    mock_api.upload_folder.return_value = "https://huggingface.co/spaces/arun-gharami/test-space"

    test_dir = tmp_path / "sample_space"
    test_dir.mkdir()
    (test_dir / "app.py").write_text("# sample app")

    manager = HubSyncManager(api=mock_api)
    url = manager.sync_directory(local_dir=test_dir, repo_id="arun-gharami/test-space", repo_type="space")

    assert url == "https://huggingface.co/spaces/arun-gharami/test-space"
    mock_api.create_repo.assert_called_once_with(repo_id="arun-gharami/test-space", repo_type="space", exist_ok=True)
    mock_api.upload_folder.assert_called_once()
