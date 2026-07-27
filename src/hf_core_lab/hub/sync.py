"""
Automated Hugging Face Hub Synchronization Manager.

Syncs local model repositories, dataset folders, and Gradio Space apps
directly to Hugging Face Hub repositories using HfApi.upload_folder.
"""

from pathlib import Path

from huggingface_hub import HfApi

from hf_core_lab.config import LabConfig
from hf_core_lab.exceptions import HubConnectionError
from hf_core_lab.logging_config import setup_logger

logger = setup_logger("hf_core_lab.hub.sync")


class HubSyncManager:
    """Manager for synchronizing local directories to Hugging Face Hub repos."""

    def __init__(self, config: LabConfig | None = None, api: HfApi | None = None):
        self.config = config or LabConfig()
        self.api = api or HfApi(token=self.config.token)

    def sync_directory(
        self,
        local_dir: str | Path,
        repo_id: str,
        repo_type: str = "space",
        commit_message: str = "feat: automated sync from GitHub repository",
    ) -> str:
        """Upload and sync local directory files to a target Hugging Face Hub repository."""
        folder_path = Path(local_dir)
        if not folder_path.exists() or not folder_path.is_dir():
            raise HubConnectionError(f"Target local directory '{local_dir}' does not exist.")

        try:
            logger.info("Syncing %s directory '%s' to repo '%s'...", repo_type, local_dir, repo_id)
            # Create repository if it doesn't exist
            self.api.create_repo(repo_id=repo_id, repo_type=repo_type, exist_ok=True)

            url = self.api.upload_folder(
                folder_path=str(folder_path),
                repo_id=repo_id,
                repo_type=repo_type,
                commit_message=commit_message,
                ignore_patterns=["__pycache__/*", "*.pyc", ".venv/*", ".git/*"],
            )
            logger.info("[SUCCESS] Sync complete. Hub repository URL: %s", url)
            return str(url)
        except Exception as e:
            raise HubConnectionError(f"Failed to sync '{local_dir}' to '{repo_id}': {e}") from e

    def sync_space(self, space_id: str, local_space_dir: str = "spaces/fraud-risk-intelligence") -> str:
        """Sync Gradio Space application directory to Hugging Face Space repository."""
        return self.sync_directory(
            local_dir=local_space_dir,
            repo_id=space_id,
            repo_type="space",
            commit_message="feat: automated Space update from GitHub CI/CD",
        )
