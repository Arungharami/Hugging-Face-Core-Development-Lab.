#!/usr/bin/env python3
"""
Example Script: Discovering Gradio/Streamlit Spaces on the Hugging Face Hub.

Usage:
    python examples/space_discovery.py --query fraud --limit 5
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hf_core_lab.config import LabConfig
from hf_core_lab.hub.discovery import HubDiscoveryEngine


def main():
    parser = argparse.ArgumentParser(description="Discover Spaces on Hugging Face Hub")
    parser.add_argument("--query", "-q", type=str, default="fraud", help="Search keyword")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    print("==================================================")
    print(" Hugging Face Core Lab - Space Discovery Tool ")
    print("==================================================\n")

    config = LabConfig()
    engine = HubDiscoveryEngine(config=config)

    spaces = engine.search_spaces(query=args.query, limit=args.limit)
    print(f"Discovered {len(spaces)} Space(s):")
    for s in spaces:
        print(f" - [{s.space_id}] SDK: {s.sdk or 'unknown'} | Likes: {s.likes:,}")


if __name__ == "__main__":
    main()
