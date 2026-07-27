"""
Hub Discovery Engine for searching models, datasets, and Spaces.
"""


from huggingface_hub import HfApi

from hf_core_lab.config import LabConfig
from hf_core_lab.exceptions import DiscoveryError
from hf_core_lab.logging_config import setup_logger
from hf_core_lab.models.metadata import DatasetMetadata, ModelMetadata, SpaceMetadata

logger = setup_logger("hf_core_lab.hub.discovery")


class HubDiscoveryEngine:
    """Engine for searching models, datasets, and Spaces on Hugging Face Hub."""

    def __init__(self, config: LabConfig | None = None, api: HfApi | None = None):
        self.config = config or LabConfig()
        self.api = api or HfApi(token=self.config.token)

    def search_models(
        self,
        query: str | None = None,
        author: str | None = None,
        task: str | None = None,
        limit: int = 10,
        sort: str = "downloads",
        direction: int = -1,
    ) -> list[ModelMetadata]:
        """Search models on the Hub matching parameters."""
        if limit <= 0 or limit > self.config.max_results_limit:
            raise DiscoveryError(f"Limit must be between 1 and {self.config.max_results_limit}.")

        try:
            logger.info("Querying Hub models (query=%s, author=%s, task=%s, limit=%d)...", query, author, task, limit)
            raw_models = self.api.list_models(
                search=query,
                author=author,
                pipeline_tag=task,
                limit=limit,
                sort=sort,
                full=False,
            )

            results: list[ModelMetadata] = []
            for item in raw_models:
                tags = getattr(item, "tags", []) or []
                results.append(
                    ModelMetadata(
                        model_id=item.id,
                        author=getattr(item, "author", None) or (item.id.split("/")[0] if "/" in item.id else None),
                        downloads=getattr(item, "downloads", 0) or 0,
                        likes=getattr(item, "likes", 0) or 0,
                        tags=tags,
                        pipeline_tag=getattr(item, "pipeline_tag", None),
                        library_name=getattr(item, "library_name", None),
                        license=next((t.replace("license:", "") for t in tags if t.startswith("license:")), None),
                        last_modified=str(getattr(item, "last_modified", "")) if getattr(item, "last_modified", None) else None,
                        sha=getattr(item, "sha", None),
                    )
                )
            return results
        except Exception as e:
            raise DiscoveryError(f"Model search failed: {e}") from e

    def search_datasets(
        self,
        query: str | None = None,
        author: str | None = None,
        limit: int = 10,
    ) -> list[DatasetMetadata]:
        """Search datasets on the Hub matching parameters."""
        if limit <= 0 or limit > self.config.max_results_limit:
            raise DiscoveryError(f"Limit must be between 1 and {self.config.max_results_limit}.")

        try:
            logger.info("Querying Hub datasets (query=%s, author=%s, limit=%d)...", query, author, limit)
            raw_datasets = self.api.list_datasets(
                search=query,
                author=author,
                limit=limit,
                full=False,
            )

            results: list[DatasetMetadata] = []
            for item in raw_datasets:
                tags = getattr(item, "tags", []) or []
                results.append(
                    DatasetMetadata(
                        dataset_id=item.id,
                        author=getattr(item, "author", None) or (item.id.split("/")[0] if "/" in item.id else None),
                        downloads=getattr(item, "downloads", 0) or 0,
                        likes=getattr(item, "likes", 0) or 0,
                        tags=tags,
                        description=getattr(item, "description", None),
                        license=next((t.replace("license:", "") for t in tags if t.startswith("license:")), None),
                        last_modified=str(getattr(item, "last_modified", "")) if getattr(item, "last_modified", None) else None,
                    )
                )
            return results
        except Exception as e:
            raise DiscoveryError(f"Dataset search failed: {e}") from e

    def search_spaces(
        self,
        query: str | None = None,
        author: str | None = None,
        limit: int = 10,
    ) -> list[SpaceMetadata]:
        """Search Spaces on the Hub matching parameters."""
        if limit <= 0 or limit > self.config.max_results_limit:
            raise DiscoveryError(f"Limit must be between 1 and {self.config.max_results_limit}.")

        try:
            logger.info("Querying Hub Spaces (query=%s, author=%s, limit=%d)...", query, author, limit)
            raw_spaces = self.api.list_spaces(
                search=query,
                author=author,
                limit=limit,
            )

            results: list[SpaceMetadata] = []
            for item in raw_spaces:
                tags = getattr(item, "tags", []) or []
                results.append(
                    SpaceMetadata(
                        space_id=item.id,
                        author=getattr(item, "author", None) or (item.id.split("/")[0] if "/" in item.id else None),
                        sdk=getattr(item, "sdk", None),
                        likes=getattr(item, "likes", 0) or 0,
                        tags=tags,
                        last_modified=str(getattr(item, "last_modified", "")) if getattr(item, "last_modified", None) else None,
                    )
                )
            return results
        except Exception as e:
            raise DiscoveryError(f"Space search failed: {e}") from e
