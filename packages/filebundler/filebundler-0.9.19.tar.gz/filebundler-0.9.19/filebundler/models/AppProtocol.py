# filebundler/models/AppProtocol.py
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

from filebundler.models.FileItem import FileItem
from filebundler.managers.ProjectSettingsManager import ProjectSettingsManager


@dataclass
class AppProtocol:
    project_path: Path
    file_items: Dict[Path, FileItem]
    psm: ProjectSettingsManager

    def paths_to_file_items(self, paths: List[Path]) -> List[FileItem]: ...
