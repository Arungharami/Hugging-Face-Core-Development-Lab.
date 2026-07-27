"""
Unit tests for CardValidator.
"""

from hf_core_lab.hub.validators import CardValidator
from hf_core_lab.models.metadata import DatasetMetadata, ModelMetadata


def test_validate_model_metadata_valid():
    model = ModelMetadata(
        model_id="test/valid-model",
        author="test",
        license="mit",
        pipeline_tag="text-classification",
        tags=["transformers"],
    )
    result = CardValidator.validate_model_metadata(model)
    assert result.is_valid is True
    assert len(result.missing_fields) == 0


def test_validate_model_metadata_missing_license():
    model = ModelMetadata(
        model_id="test/invalid-model",
        author="test",
        license=None,
    )
    result = CardValidator.validate_model_metadata(model)
    assert result.is_valid is False
    assert "license" in result.missing_fields


def test_validate_dataset_metadata_valid():
    dataset = DatasetMetadata(
        dataset_id="test/valid-dataset",
        author="test",
        license="mit",
        description="A great dataset",
    )
    result = CardValidator.validate_dataset_metadata(dataset)
    assert result.is_valid is True
    assert len(result.missing_fields) == 0
