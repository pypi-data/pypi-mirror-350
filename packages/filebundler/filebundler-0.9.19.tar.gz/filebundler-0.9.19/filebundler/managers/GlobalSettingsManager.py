# filebundler/managers/GlobalSettingsManager.py
import logging

from pathlib import Path

from filebundler.utils import json_dump, read_file
from filebundler.models.GlobalSettings import GlobalSettings

logger = logging.getLogger(__name__)


class GlobalSettingsManager:
    def __init__(self):
        self.settings_dir = Path.home() / ".filebundler"
        self.settings_dir.mkdir(exist_ok=True)
        self.settings_file = self.settings_dir / "settings.json"
        self.settings = self._load_settings()

    def _load_settings(self):
        if self.settings_file.exists():
            try:
                file_data = read_file(self.settings_file)
                gsm = GlobalSettings.model_validate_json(file_data)
                # logger.info(f"Loaded global settings: {gsm}")
                return gsm
            except Exception:
                logger.error(
                    f"Error loading global settings from {self.settings_file}",
                    exc_info=True,
                )
        return GlobalSettings()

    def save_settings(self):
        try:
            with open(self.settings_file, "w") as f:
                json_dump(self.settings.model_dump(), f)
        except Exception as e:
            logger.error(f"Error saving global settings: {str(e)}")

    def add_recent_project(self, project_path: Path):
        if project_path in self.settings.recent_projects:
            self.settings.recent_projects.remove(project_path)
        else:
            logger.info(f"Adding recent project to global settings: {project_path}")
        self.settings.recent_projects.insert(0, project_path)
        self.save_settings()

    def get_recent_projects(self):
        existing = [p for p in self.settings.recent_projects if p.exists()]
        if len(existing) != len(self.settings.recent_projects):
            self.settings.recent_projects = existing
            self.save_settings()
        return self.settings.recent_projects
