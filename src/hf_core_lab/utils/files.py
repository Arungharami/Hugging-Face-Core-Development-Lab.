"""
File system helper utilities.
"""

from pathlib import Path
from typing import Union


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure parent and target directory exist."""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def write_report_to_file(content: str, output_filepath: Union[str, Path]) -> Path:
    """Save report text to file, creating parent directories if needed."""
    file_path = Path(output_filepath)
    ensure_directory(file_path.parent)
    file_path.write_text(content, encoding="utf-8")
    return file_path
