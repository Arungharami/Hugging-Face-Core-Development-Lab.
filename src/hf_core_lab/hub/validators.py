"""
Card & Metadata Validators for ModelCards and DatasetCards.
"""

from hf_core_lab.models.metadata import CardValidationResult, DatasetMetadata, ModelMetadata


class CardValidator:
    """Quality and metadata compliance validator for Hugging Face repos."""

    @staticmethod
    def validate_model_metadata(model: ModelMetadata) -> CardValidationResult:
        """Validate metadata compliance for a ModelMetadata object."""
        missing: list[str] = []
        warnings: list[str] = []

        if not model.license:
            missing.append("license")
        if not model.pipeline_tag:
            warnings.append("missing_pipeline_tag")
        if not model.author:
            warnings.append("missing_author")
        if not model.tags:
            warnings.append("empty_tags")

        is_valid = len(missing) == 0
        return CardValidationResult(
            repo_id=model.model_id,
            repo_type="model",
            is_valid=is_valid,
            missing_fields=missing,
            warnings=warnings,
        )

    @staticmethod
    def validate_dataset_metadata(dataset: DatasetMetadata) -> CardValidationResult:
        """Validate metadata compliance for a DatasetMetadata object."""
        missing: list[str] = []
        warnings: list[str] = []

        if not dataset.license:
            missing.append("license")
        if not dataset.description:
            missing.append("description")
        if not dataset.author:
            warnings.append("missing_author")

        is_valid = len(missing) == 0
        return CardValidationResult(
            repo_id=dataset.dataset_id,
            repo_type="dataset",
            is_valid=is_valid,
            missing_fields=missing,
            warnings=warnings,
        )
