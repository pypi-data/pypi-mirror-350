import shutil
from pathlib import Path


EXAMPLE_TASK_FILE = Path(__file__).parent / "default-ignore-patterns.txt"


def copy_default_ignore_patterns(filebundler_dir: Path):
    ignore_patterns_file = filebundler_dir / "ignore-patterns.txt"
    if not ignore_patterns_file.exists():
        shutil.copy(EXAMPLE_TASK_FILE, ignore_patterns_file)
