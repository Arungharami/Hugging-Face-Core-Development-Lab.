#!/usr/bin/env python3
"""
Example Script: Discovering Models on the Hugging Face Hub.

Usage:
    python examples/model_discovery.py --query text-classification --limit 5
"""

import argparse
import sys
from pathlib import Path

# Add src/ to path to enable local execution without prior installation
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hf_core_lab.config import LabConfig
from hf_core_lab.hub.discovery import HubDiscoveryEngine
from hf_core_lab.hub.validators import CardValidator
from hf_core_lab.models.reports import ReportGenerator
from hf_core_lab.utils.files import write_report_to_file


def main():
    parser = argparse.ArgumentParser(description="Discover Models on Hugging Face Hub")
    parser.add_argument("--query", "-q", type=str, default="text-classification", help="Search keyword")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of results")
    parser.add_argument("--output-dir", type=str, default="reports/models", help="Directory to save report")
    args = parser.parse_args()

    print("==================================================")
    print(" Hugging Face Core Lab - Model Discovery Tool ")
    print("==================================================\n")

    config = LabConfig()
    engine = HubDiscoveryEngine(config=config)

    print(f"Searching models matching: '{args.query}' (limit={args.limit})...\n")
    models = engine.search_models(query=args.query, limit=args.limit)

    if not models:
        print("No models found matching search criteria.")
        return

    print(f"Discovered {len(models)} model(s):")
    for m in models:
        print(f" - [{m.model_id}] Author: {m.author} | Downloads: {m.downloads:,} | Likes: {m.likes:,} | License: {m.license or 'N/A'}")

    # Validate metadata
    validation_results = [CardValidator.validate_model_metadata(m) for m in models]

    # Generate Markdown Report
    md_report = ReportGenerator.models_to_markdown(models, title=f"Model Discovery Report for '{args.query}'")
    md_report += "\n" + ReportGenerator.validation_to_markdown(validation_results)

    report_path = Path(args.output_dir) / "model_discovery_report.md"
    write_report_to_file(md_report, report_path)
    print(f"\n[SUCCESS] Discovery report exported to: {report_path}")


if __name__ == "__main__":
    main()
