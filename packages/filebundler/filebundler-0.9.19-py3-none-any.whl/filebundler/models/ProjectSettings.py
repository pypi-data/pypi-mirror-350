# filebundler/models/ProjectSettings.py
from typing import List

from filebundler.utils import BaseModel
from filebundler.constants import DEFAULT_MAX_RENDER_FILES


class AutoBundleSettings(BaseModel):
    """Settings for the Auto-Bundle feature."""

    auto_refresh_project_structure: bool = True
    auto_include_bundle_files: bool = False
    user_prompt: str = "Given the TODOs in the project, select the files that are relevant to the tasks."


class ProjectSettings(BaseModel):
    ignore_patterns: List[str] = []
    max_files: int = DEFAULT_MAX_RENDER_FILES
    sort_files_first: bool = True
    # alphabetical_sort: Literal["asc", "desc"] = "asc"
    auto_bundle_settings: AutoBundleSettings = AutoBundleSettings()


__all__ = ["ProjectSettings"]
