# filebundler/utils/filepath_checker.py
import logging
import argparse

from typing import List
from pathlib import Path

logger = logging.getLogger(__name__)


def validate_first_line(filepath: Path):
    """Checks that the first line of a file is a comment with the relative file path"""
    with open(filepath, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()

    if not first_line.startswith("# "):
        logger.warning(f"File does not start with a comment: {filepath}")
        return False

    if not first_line.endswith(filepath.as_posix()):
        logger.warning(
            f"File path does not match comment: {filepath = }, {first_line = }"
        )
        return False

    return True


def validate_files(directory: Path):
    """Validates all python files in a directory"""
    invalid_files: List[Path] = []
    valid_files: List[Path] = []

    for file_path in directory.glob("**/*.py"):
        if validate_first_line(file_path):
            valid_files.append(file_path)
        else:
            invalid_files.append(file_path)

    return valid_files, invalid_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate Python files in a directory."
    )
    parser.add_argument("directory", type=str, help="Directory to validate files")
    args = parser.parse_args()

    directory_path = Path(args.directory)
    valid_files, invalid_files = validate_files(directory_path)

    if invalid_files:
        print("# Invalid Files")
        print("\n".join([f.as_posix() for f in invalid_files]))
    else:
        print("All files are valid.")
        print(f"Total files: {len(valid_files)}")

# usage: python filebundler/utils/filepath_checker.py filebundler
