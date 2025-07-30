import shutil
from pathlib import Path


TEMPLATES_DIR = Path(__file__).parent / "templates"
EXAMPLE_TASK_FILE = TEMPLATES_DIR / "example-task.md"
TASK_FILE_MGMT_GUIDE_FILE = TEMPLATES_DIR / "task-file-management.md"


def copy_templates(filebundler_dir: Path):
    tasks_dir = filebundler_dir / "tasks"
    tasks_dir.mkdir(exist_ok=True)
    shutil.copy(EXAMPLE_TASK_FILE, tasks_dir / "example-task.md")
    shutil.copy(TASK_FILE_MGMT_GUIDE_FILE, tasks_dir / "task-file-management.md")
