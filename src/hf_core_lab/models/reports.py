"""
Report generation utilities for export into JSON and Markdown formats.
"""

import json
from typing import Any

from hf_core_lab.models.metadata import (
    CardValidationResult,
    ModelMetadata,
)


class ReportGenerator:
    """Formatter for exporting discovery and validation outputs."""

    @staticmethod
    def to_json(data: list[Any] | Any, indent: int = 2) -> str:
        """Serialize metadata dataclass instances or dict lists into formatted JSON string."""
        if isinstance(data, list):
            serialized = [item.to_dict() if hasattr(item, "to_dict") else item for item in data]
        elif hasattr(data, "to_dict"):
            serialized = data.to_dict()
        else:
            serialized = data
        return json.dumps(serialized, indent=indent, default=str)

    @staticmethod
    def models_to_markdown(models: list[ModelMetadata], title: str = "Hub Model Discovery Report") -> str:
        """Format list of ModelMetadata into a markdown report table."""
        lines = [
            f"# {title}",
            "",
            f"**Total Models Discovered:** {len(models)}",
            "",
            "| Model ID | Author | Pipeline / Task | Downloads | Likes | License |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for m in models:
            author = m.author or "N/A"
            task = m.pipeline_tag or "N/A"
            license_str = m.license or "Unspecified"
            lines.append(f"| `{m.model_id}` | {author} | `{task}` | {m.downloads:,} | {m.likes:,} | {license_str} |")
        lines.append("")
        return "\n".join(lines)

    @staticmethod
    def validation_to_markdown(results: list[CardValidationResult], title: str = "Metadata Compliance Audit Report") -> str:
        """Format list of CardValidationResults into markdown report."""
        lines = [
            f"# {title}",
            "",
            f"**Total Cards Audited:** {len(results)}",
            "",
            "| Repo ID | Type | Status | Missing Fields | Warnings |",
            "| --- | --- | --- | --- | --- |",
        ]
        for r in results:
            status = "PASS :white_check_mark:" if r.is_valid else "FAIL :x:"
            missing = ", ".join(r.missing_fields) if r.missing_fields else "None"
            warnings = ", ".join(r.warnings) if r.warnings else "None"
            lines.append(f"| `{r.repo_id}` | `{r.repo_type}` | {status} | {missing} | {warnings} |")
        lines.append("")
        return "\n".join(lines)
