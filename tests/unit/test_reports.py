"""
Unit tests for ReportGenerator.
"""

from hf_core_lab.models.metadata import CardValidationResult, DatasetMetadata, ModelMetadata, SpaceMetadata
from hf_core_lab.models.reports import ReportGenerator


def test_to_json():
    model = ModelMetadata(model_id="test/m1", author="test")
    json_str = ReportGenerator.to_json(model)
    assert '"model_id": "test/m1"' in json_str

    dataset = DatasetMetadata(dataset_id="test/d1", author="test")
    json_str_list = ReportGenerator.to_json([dataset])
    assert '"dataset_id": "test/d1"' in json_str_list

    space = SpaceMetadata(space_id="test/s1", author="test", sdk="gradio")
    assert '"space_id": "test/s1"' in ReportGenerator.to_json(space)


def test_models_to_markdown():
    model = ModelMetadata(
        model_id="meta-llama/Llama-3.2-1B",
        author="meta-llama",
        downloads=1000,
        likes=50,
        pipeline_tag="text-generation",
        license="mit",
    )
    md = ReportGenerator.models_to_markdown([model])
    assert "# Hub Model Discovery Report" in md
    assert "`meta-llama/Llama-3.2-1B`" in md


def test_validation_to_markdown():
    res = CardValidationResult(
        repo_id="test/m1",
        repo_type="model",
        is_valid=False,
        missing_fields=["license"],
        warnings=["missing_author"],
    )
    md = ReportGenerator.validation_to_markdown([res])
    assert "# Metadata Compliance Audit Report" in md
    assert "FAIL :x:" in md
    assert "license" in md
