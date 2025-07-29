# filebundler/utils/project_utils.py
import fnmatch

from typing import List
from pathlib import Path

from filebundler.models.ProjectSettings import ProjectSettings


def sort_files(files: List[Path], ps: ProjectSettings):
    def sorting_key(p: Path):
        # Return a tuple where:
        # First element: False for files, True for directories (so files come first)
        # Second element: lowercase name for alphabetical sorting
        if ps.sort_files_first:
            return (p.is_dir(), p.name.lower())
        else:
            return (p.is_file(), p.name.lower())

    return sorted(
        files,
        key=sorting_key,
        # reverse=ps.alphabetical_sort == "desc",
    )


def invalid_path(relative_path: Path, ignore_patterns: List[str]):
    """Check if file matches any ignore patterns"""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(relative_path.as_posix(), pattern):
            return True
    return False
