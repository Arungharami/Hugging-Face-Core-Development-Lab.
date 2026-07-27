#!/usr/bin/env python3
"""
Example Script: Safe repository upload demonstration using modern hf SDK.

Usage:
    python examples/upload_example.py --repo-id arun-gharami/test-model
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hf_core_lab.config import LabConfig
from hf_core_lab.hub.repositories import RepositoryManager


def main():
    parser = argparse.ArgumentParser(description="Upload Example Demo")
    parser.add_argument("--repo-id", required=True, help="Target repository ID on HF Hub")
    args = parser.parse_args()

    config = LabConfig()
    if not config.is_authenticated():
        print("[ERROR] HF_TOKEN environment variable is not set. Aborting upload demo for security.")
        sys.exit(1)

    manager = RepositoryManager(config=config)
    print(f"Creating / verifying target repository '{args.repo_id}'...")
    url = manager.create_repo(repo_id=args.repo_id, repo_type="model", private=True)
    print(f"[SUCCESS] Repository ready at: {url}")


if __name__ == "__main__":
    main()
