"""
Repository operations helper module.
"""

from typing import Optional
from huggingface_hub import HfApi

from hf_core_lab.config import LabConfig
from hf_core_lab.exceptions import HubConnectionError
from hf_core_lab.logging_config import setup_logger

logger = setup_logger("hf_core_lab.hub.repositories")


class RepositoryManager:
    """Manager for creating, downloading, and uploading repository files."""

    def __init__(self, config: Optional[LabConfig] = None, api: Optional[HfApi] = None):
        self.config = config or LabConfig()
        self.api = api or HfApi(token=self.config.token)

    def create_repo(self, repo_id: str, repo_type: str = "model", private: bool = False) -> str:
        """Create a new repository on Hugging Face Hub."""
        try:
            logger.info("Creating %s repo: %s (private=%s)", repo_type, repo_id, private)
            url = self.api.create_repo(repo_id=repo_id, repo_type=repo_type, private=private, exist_ok=True)
            return str(url)
        except Exception as e:
            raise HubConnectionError(f"Failed to create repo '{repo_id}': {e}") from e
