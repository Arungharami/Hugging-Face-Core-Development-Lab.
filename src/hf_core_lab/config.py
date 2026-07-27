"""
Configuration management for Hugging Face Core Development Lab.
"""

import os
from dataclasses import dataclass, field


@dataclass
class LabConfig:
    """Configuration settings for Hugging Face Core Development Lab operations."""

    token: str | None = field(
        default_factory=lambda: os.getenv("HF_TOKEN")
    )
    username: str = field(
        default_factory=lambda: os.getenv("HF_USERNAME", "arun-gharami")
    )
    env: str = field(
        default_factory=lambda: os.getenv("ENV", "development")
    )
    request_timeout: int = 30
    max_results_limit: int = 100
    cache_dir: str | None = field(
        default_factory=lambda: os.getenv("HF_HOME")
    )

    def is_authenticated(self) -> bool:
        """Check if an API token is configured in environment or settings."""
        return self.token is not None and len(self.token.strip()) > 0
