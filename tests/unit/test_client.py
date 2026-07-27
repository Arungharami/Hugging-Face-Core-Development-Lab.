"""
Unit tests for HfHubClient API wrapper with mocked network responses.
"""

from unittest.mock import MagicMock
import pytest
from huggingface_hub.utils import HfHubHTTPError
from requests.models import Response

from hf_core_lab.config import LabConfig
from hf_core_lab.exceptions import AuthenticationError, HubConnectionError
from hf_core_lab.hub.client import HfHubClient


def test_whoami_success():
    mock_api = MagicMock()
    mock_api.whoami.return_value = {"name": "arun-gharami", "type": "user", "fullname": "Arun Kumar Gharami"}

    config = LabConfig(token="hf_mock_token_123")
    client = HfHubClient(config=config, api=mock_api)

    info = client.whoami()
    assert info["name"] == "arun-gharami"
    mock_api.whoami.assert_called_once_with(token="hf_mock_token_123")


def test_whoami_unauthorized():
    mock_api = MagicMock()
    response = Response()
    response.status_code = 401
    mock_api.whoami.side_effect = HfHubHTTPError("401 Client Error: Unauthorized", response=response)

    config = LabConfig(token="hf_invalid_token")
    client = HfHubClient(config=config, api=mock_api)

    with pytest.raises(AuthenticationError):
        client.whoami()


def test_whoami_connection_error():
    mock_api = MagicMock()
    mock_api.whoami.side_effect = Exception("Connection Timeout")

    client = HfHubClient(api=mock_api)
    with pytest.raises(HubConnectionError):
        client.whoami()
