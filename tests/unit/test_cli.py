"""
Unit tests for hf-core-lab CLI parser and subcommands.
"""

from unittest.mock import patch
from hf_core_lab.cli import build_parser, main


def test_build_parser():
    parser = build_parser()
    assert parser.prog == "hf-core-lab"


@patch("hf_core_lab.cli.HubDiscoveryEngine")
def test_cli_discover_models(mock_engine_cls):
    mock_engine = mock_engine_cls.return_value
    mock_engine.search_models.return_value = []

    exit_code = main(["discover", "--type", "model", "--query", "text-classification", "--limit", "2"])
    assert exit_code == 0
    mock_engine.search_models.assert_called_once()
