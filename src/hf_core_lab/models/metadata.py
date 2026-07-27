"""
Dataclasses and schemas for Hub resources and search results.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModelMetadata:
    """Structured metadata for a Hugging Face Model repository."""

    model_id: str
    author: Optional[str] = None
    downloads: int = 0
    likes: int = 0
    tags: List[str] = field(default_factory=list)
    pipeline_tag: Optional[str] = None
    library_name: Optional[str] = None
    license: Optional[str] = None
    last_modified: Optional[str] = None
    sha: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary representation."""
        return {
            "model_id": self.model_id,
            "author": self.author,
            "downloads": self.downloads,
            "likes": self.likes,
            "tags": self.tags,
            "pipeline_tag": self.pipeline_tag,
            "library_name": self.library_name,
            "license": self.license,
            "last_modified": self.last_modified,
            "sha": self.sha,
        }


@dataclass
class DatasetMetadata:
    """Structured metadata for a Hugging Face Dataset repository."""

    dataset_id: str
    author: Optional[str] = None
    downloads: int = 0
    likes: int = 0
    tags: List[str] = field(default_factory=list)
    description: Optional[str] = None
    license: Optional[str] = None
    last_modified: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary representation."""
        return {
            "dataset_id": self.dataset_id,
            "author": self.author,
            "downloads": self.downloads,
            "likes": self.likes,
            "tags": self.tags,
            "description": self.description,
            "license": self.license,
            "last_modified": self.last_modified,
        }


@dataclass
class SpaceMetadata:
    """Structured metadata for a Hugging Face Space repository."""

    space_id: str
    author: Optional[str] = None
    sdk: Optional[str] = None
    likes: int = 0
    tags: List[str] = field(default_factory=list)
    last_modified: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary representation."""
        return {
            "space_id": self.space_id,
            "author": self.author,
            "sdk": self.sdk,
            "likes": self.likes,
            "tags": self.tags,
            "last_modified": self.last_modified,
        }


@dataclass
class CardValidationResult:
    """Result of ModelCard or DatasetCard quality validation check."""

    repo_id: str
    repo_type: str  # "model" or "dataset"
    is_valid: bool
    missing_fields: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert validation result to dictionary representation."""
        return {
            "repo_id": self.repo_id,
            "repo_type": self.repo_type,
            "is_valid": self.is_valid,
            "missing_fields": self.missing_fields,
            "warnings": self.warnings,
        }
