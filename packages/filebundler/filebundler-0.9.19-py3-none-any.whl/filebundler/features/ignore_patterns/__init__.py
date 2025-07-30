import shutil
import fnmatch

from typing import List
from pathlib import Path


EXAMPLE_TASK_FILE = Path(__file__).parent / "default-ignore-patterns.txt"


def copy_default_ignore_patterns(filebundler_dir: Path):
    ignore_patterns_file = filebundler_dir / "ignore-patterns.txt"
    if not ignore_patterns_file.exists():
        shutil.copy(EXAMPLE_TASK_FILE, ignore_patterns_file)


def invalid_path(relative_path: str, ignore_patterns: List[str]):
    """Check if file matches any ignore patterns"""
    if f"!{relative_path}" in ignore_patterns:
        return False
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(relative_path, pattern):
            return True
    return False