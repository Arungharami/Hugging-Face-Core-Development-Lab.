"""
Unit tests for hf-core-lab CLI parser and subcommands.
"""

from unittest.mock import MagicMock, patch
from hf_core_lab.cli import build_parser, main
from hf_core_lab.models.metadata import CardValidationResult, DatasetMetadata, ModelMetadata, SpaceMetadata


def test_build_parser():
    parser = build_parser()
    assert parser.prog == "hf-core-lab"


def test_cli_no_args():
    assert main([]) == 0


@patch("hf_core_lab.cli.HfHubClient")
def test_cli_whoami_success(mock_client_cls):
    mock_client = mock_client_cls.return_value
    mock_client.whoami.return_value = {"name": "arun-gharami", "type": "user", "fullname": "Arun Kumar Gharami"}
    assert main(["whoami"]) == 0


@patch("hf_core_lab.cli.HfHubClient")
def test_cli_whoami_failure(mock_client_cls):
    mock_client = mock_client_cls.return_value
    mock_client.whoami.side_effect = Exception("Auth failed")
    assert main(["whoami"]) == 1


@patch("hf_core_lab.cli.HubDiscoveryEngine")
def test_cli_discover_models_json(mock_engine_cls, tmp_path):
    mock_engine = mock_engine_cls.return_value
    mock_engine.search_models.return_value = [ModelMetadata(model_id="test/m1", author="test")]

    out_file = tmp_path / "report.json"
    exit_code = main(["discover", "--type", "model", "--query", "text-classification", "--format", "json", "--output", str(out_file)])
    assert exit_code == 0
    assert out_file.exists()


@patch("hf_core_lab.cli.HubDiscoveryEngine")
def test_cli_discover_datasets(mock_engine_cls):
    mock_engine = mock_engine_cls.return_value
    mock_engine.search_datasets.return_value = [DatasetMetadata(dataset_id="test/d1", author="test")]
    assert main(["discover", "--type", "dataset", "--query", "finance"]) == 0


@patch("hf_core_lab.cli.HubDiscoveryEngine")
def test_cli_discover_spaces(mock_engine_cls):
    mock_engine = mock_engine_cls.return_value
    mock_engine.search_spaces.return_value = [SpaceMetadata(space_id="test/s1", author="test", sdk="gradio")]
    assert main(["discover", "--type", "space", "--query", "fraud"]) == 0


@patch("hf_core_lab.cli.HubDiscoveryEngine")
def test_cli_validate_model_valid(mock_engine_cls):
    mock_engine = mock_engine_cls.return_value
    mock_model = ModelMetadata(model_id="test/m1", author="test", license="mit")
    mock_engine.search_models.return_value = [mock_model]

    assert main(["validate", "--repo-id", "test/m1", "--type", "model"]) == 0


@patch("hf_core_lab.cli.HubDiscoveryEngine")
def test_cli_validate_dataset(mock_engine_cls):
    mock_engine = mock_engine_cls.return_value
    mock_dataset = DatasetMetadata(dataset_id="test/d1", author="test", license="mit", description="valid")
    mock_engine.search_datasets.return_value = [mock_dataset]

    assert main(["validate", "--repo-id", "test/d1", "--type", "dataset"]) == 0
