#!/usr/bin/env python3
"""
Example Script: Discovering Datasets on the Hugging Face Hub.

Usage:
    python examples/dataset_discovery.py --query finance --limit 5
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hf_core_lab.config import LabConfig
from hf_core_lab.hub.discovery import HubDiscoveryEngine
from hf_core_lab.models.reports import ReportGenerator
from hf_core_lab.utils.files import write_report_to_file


def main():
    parser = argparse.ArgumentParser(description="Discover Datasets on Hugging Face Hub")
    parser.add_argument("--query", "-q", type=str, default="finance", help="Search keyword")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    print("==================================================")
    print(" Hugging Face Core Lab - Dataset Discovery Tool ")
    print("==================================================\n")

    config = LabConfig()
    engine = HubDiscoveryEngine(config=config)

    datasets = engine.search_datasets(query=args.query, limit=args.limit)
    print(f"Discovered {len(datasets)} dataset(s):")
    for d in datasets:
        print(f" - [{d.dataset_id}] Author: {d.author} | Downloads: {d.downloads:,} | Likes: {d.likes:,}")

    json_report = ReportGenerator.to_json(datasets)
    report_path = Path("reports/datasets/dataset_discovery_report.json")
    write_report_to_file(json_report, report_path)
    print(f"\n[SUCCESS] Report saved to: {report_path}")


if __name__ == "__main__":
    main()
