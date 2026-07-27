"""
Unit tests for file utility functions.
"""

from pathlib import Path
from hf_core_lab.utils.files import ensure_directory, write_report_to_file


def test_ensure_directory(tmp_path: Path):
    target_dir = tmp_path / "nested" / "dir"
    res = ensure_directory(target_dir)
    assert res.exists()
    assert res.is_dir()


def test_write_report_to_file(tmp_path: Path):
    target_file = tmp_path / "reports" / "summary.txt"
    content = "Sample Report Output"
    written_path = write_report_to_file(content, target_file)

    assert written_path.exists()
    assert written_path.read_text(encoding="utf-8") == content
