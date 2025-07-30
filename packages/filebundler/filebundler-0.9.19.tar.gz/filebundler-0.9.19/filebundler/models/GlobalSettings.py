# filebundler/models/GlobalSettings.py
import logging

from typing import List
from pathlib import Path

from pydantic import field_serializer, field_validator

from filebundler.utils import BaseModel
from filebundler.constants import DEFAULT_MAX_RENDER_FILES

logger = logging.getLogger(__name__)


class GlobalSettings(BaseModel):
    max_files: int = DEFAULT_MAX_RENDER_FILES
    recent_projects: List[Path] = []

    @field_validator("recent_projects")
    def recent_projects_validator(cls, value: List[Path]):
        for p in value:
            if not p.exists():
                logger.warning(f"Recent project {p} does not exist any more, removing")
                value.remove(p)
        return value

    @field_serializer("recent_projects")
    def recent_projects_serializer(self, value: List[Path]):
        return [p.as_posix() for p in value]

    @property
    def recent_projects_str(self):
        return [p.as_posix() for p in self.recent_projects]
