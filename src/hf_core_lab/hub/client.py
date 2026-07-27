"""
Hugging Face Hub API Client Wrapper.
"""

from typing import Any, Dict, Optional
from huggingface_hub import HfApi
from huggingface_hub.utils import HfHubHTTPError

from hf_core_lab.config import LabConfig
from hf_core_lab.exceptions import AuthenticationError, HubConnectionError
from hf_core_lab.logging_config import setup_logger

logger = setup_logger("hf_core_lab.hub.client")


class HfHubClient:
    """Wrapper around huggingface_hub.HfApi providing error mapping and auth state."""

    def __init__(self, config: Optional[LabConfig] = None, api: Optional[HfApi] = None):
        self.config = config or LabConfig()
        self.api = api or HfApi(token=self.config.token)

    def whoami(self) -> Dict[str, Any]:
        """Verify current authentication status and user details."""
        if not self.config.token:
            logger.warning("No HF_TOKEN found in configuration; checking anonymous or cached token status.")

        try:
            user_info = self.api.whoami(token=self.config.token)
            logger.info("Successfully authenticated with Hugging Face Hub.")
            return user_info
        except HfHubHTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid or expired Hugging Face authentication token.") from e
            raise HubConnectionError(f"HTTP error during whoami lookup: {e}") from e
        except Exception as e:
            raise HubConnectionError(f"Failed to connect to Hugging Face Hub: {e}") from e
