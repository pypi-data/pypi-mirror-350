# filebundler/models/BundleMetadata.py
import logging

from typing import Optional
from datetime import datetime
from pydantic import Field, ConfigDict

from filebundler.utils import BaseModel, format_datetime

logger = logging.getLogger(__name__)


class ExportStats(BaseModel):
    """Statistics related to bundle exports"""

    last_exported: Optional[datetime] = None
    export_count: int = 0

    def record_export(self) -> None:
        """Record a new export event"""
        self.last_exported = datetime.now()
        self.export_count += 1

    @property
    def last_exported_str(self):
        return format_datetime(self.last_exported)


def format_file_size(size_bytes: int) -> str:
    """Format file size for display"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


class BundleMetadata(BaseModel):
    """Metadata for a bundle including export statistics and file information"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    created_at: datetime = Field(default_factory=datetime.now)
    export_stats: ExportStats = Field(default_factory=ExportStats)

    @property
    def created_at_str(self):
        """Get created_at as string"""
        return format_datetime(self.created_at)
