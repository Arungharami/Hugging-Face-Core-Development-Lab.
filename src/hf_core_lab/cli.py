"""
Command-Line Interface for Hugging Face Core Development Lab (`hf-core-lab`).
"""

import argparse
import sys
from typing import Optional

from hf_core_lab.config import LabConfig
from hf_core_lab.hub.client import HfHubClient
from hf_core_lab.hub.discovery import HubDiscoveryEngine
from hf_core_lab.hub.validators import CardValidator
from hf_core_lab.logging_config import setup_logger
from hf_core_lab.models.reports import ReportGenerator
from hf_core_lab.utils.files import write_report_to_file

logger = setup_logger("hf_core_lab.cli")


def build_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="hf-core-lab",
        description="Hugging Face Core Development Lab CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: whoami
    whoami_parser = subparsers.add_parser("whoami", help="Check Hugging Face Hub authentication status")

    # Command: discover
    discover_parser = subparsers.add_parser("discover", help="Search models, datasets, or Spaces on the Hub")
    discover_parser.add_argument("--type", choices=["model", "dataset", "space"], default="model", help="Resource type to search")
    discover_parser.add_argument("--query", "-q", type=str, default=None, help="Search query keyword")
    discover_parser.add_argument("--author", "-a", type=str, default=None, help="Filter by author / organization")
    discover_parser.add_argument("--task", "-t", type=str, default=None, help="Filter models by pipeline task")
    discover_parser.add_argument("--limit", "-l", type=int, default=5, help="Number of results (max 100)")
    discover_parser.add_argument("--format", choices=["text", "json", "markdown"], default="text", help="Output format")
    discover_parser.add_argument("--output", "-o", type=str, default=None, help="Output file path to save report")

    # Command: validate
    validate_parser = subparsers.add_parser("validate", help="Audit model card metadata compliance")
    validate_parser.add_argument("--repo-id", required=True, help="Model or dataset repo ID (e.g. meta-llama/Llama-3.2-1B)")
    validate_parser.add_argument("--type", choices=["model", "dataset"], default="model", help="Repository type")

    return parser


def main(args: Optional[list] = None) -> int:
    """Main CLI entrypoint."""
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 0

    config = LabConfig()
    client = HfHubClient(config=config)

    if parsed.command == "whoami":
        try:
            info = client.whoami()
            print(f"Authenticated as: {info.get('name', 'Unknown')} ({info.get('fullname', 'N/A')})")
            print(f"Type: {info.get('type', 'user')}")
            return 0
        except Exception as e:
            print(f"Authentication Check Failed: {e}", file=sys.stderr)
            return 1

    elif parsed.command == "discover":
        engine = HubDiscoveryEngine(config=config)
        if parsed.type == "model":
            results = engine.search_models(query=parsed.query, author=parsed.author, task=parsed.task, limit=parsed.limit)
            if parsed.format == "json":
                out = ReportGenerator.to_json(results)
            elif parsed.format == "markdown":
                out = ReportGenerator.models_to_markdown(results)
            else:
                out = f"Found {len(results)} model(s):\n" + "\n".join(f" - {m.model_id} (downloads={m.downloads:,})" for m in results)

        elif parsed.type == "dataset":
            results = engine.search_datasets(query=parsed.query, author=parsed.author, limit=parsed.limit)
            if parsed.format == "json":
                out = ReportGenerator.to_json(results)
            else:
                out = f"Found {len(results)} dataset(s):\n" + "\n".join(f" - {d.dataset_id} (downloads={d.downloads:,})" for d in results)

        elif parsed.type == "space":
            results = engine.search_spaces(query=parsed.query, author=parsed.author, limit=parsed.limit)
            if parsed.format == "json":
                out = ReportGenerator.to_json(results)
            else:
                out = f"Found {len(results)} space(s):\n" + "\n".join(f" - {s.space_id} (sdk={s.sdk})" for s in results)

        print(out)
        if parsed.output:
            write_report_to_file(out, parsed.output)
            print(f"\nReport written to: {parsed.output}")
        return 0

    elif parsed.command == "validate":
        engine = HubDiscoveryEngine(config=config)
        if parsed.type == "model":
            models = engine.search_models(query=parsed.repo_id, limit=1)
            if not models:
                print(f"Repository '{parsed.repo_id}' not found.", file=sys.stderr)
                return 1
            res = CardValidator.validate_model_metadata(models[0])
        else:
            datasets = engine.search_datasets(query=parsed.repo_id, limit=1)
            if not datasets:
                print(f"Dataset '{parsed.repo_id}' not found.", file=sys.stderr)
                return 1
            res = CardValidator.validate_dataset_metadata(datasets[0])

        print(f"Repo ID: {res.repo_id}")
        print(f"Type: {res.repo_type}")
        print(f"Status: {'VALID' if res.is_valid else 'INVALID'}")
        print(f"Missing Fields: {', '.join(res.missing_fields) if res.missing_fields else 'None'}")
        print(f"Warnings: {', '.join(res.warnings) if res.warnings else 'None'}")
        return 0 if res.is_valid else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
