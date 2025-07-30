# filebundler/models/Bundle.py
import re
import logging
import logfire

from datetime import datetime
from typing import List, Optional

from pydantic import field_validator, Field, computed_field

from filebundler.models.FileItem import FileItem
from filebundler.models.BundleMetadata import BundleMetadata
from filebundler.models.BundleMetadata import format_datetime, format_file_size

from filebundler.utils import BaseModel, read_file

from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


class Bundle(BaseModel):
    name: str
    file_items: List[FileItem]
    metadata: BundleMetadata = Field(default_factory=BundleMetadata)

    @field_validator("name")
    def check_name(cls, value: str):
        assert re.fullmatch(r"[a-z0-9-]+", value), (
            "Bundle name must be lowercase, alphanumeric, and may include hyphens."
        )
        return value

    @field_validator("file_items")
    def check_file_items(cls, values: List[FileItem]):
        return [fi for fi in values if fi.path.exists() and not fi.is_dir]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def last_modified_date(self) -> Optional[datetime]:
        """Get the most recent modification date of any file in the bundle"""
        return max(
            datetime.fromtimestamp(fi.path.stat().st_mtime) for fi in self.file_items
        )

    @property
    def last_modified_date_str(self) -> str:
        return (
            format_datetime(self.last_modified_date)
            if self.last_modified_date
            else "Never"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def size_bytes(self) -> int:
        """Get the total size in bytes of all files in the bundle"""
        return sum(fi.path.stat().st_size for fi in self.file_items)

    @property
    def size_str(self) -> str:
        return format_file_size(self.size_bytes)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def tokens(self) -> int:
        """Get the total token count of all files in the bundle"""
        return sum(fi.tokens for fi in self.file_items)

    @property
    def is_stale(self) -> bool:
        """Check if bundle is stale (files modified after last export)"""
        if not self.metadata.export_stats.last_exported:
            return False  # Never exported, so not stale

        if not self.last_modified_date:
            return False  # No files with modification dates

        return self.last_modified_date > self.metadata.export_stats.last_exported

    def prune(self):
        """Remove files that no longer exist from a bundle"""
        with logfire.span("pruning bundle {name}", name=self.name):
            original_count = len(self.file_items)
            self.file_items = [fi for fi in self.file_items if fi.path.exists()]

            removed_count = original_count - len(self.file_items)
            if removed_count > 0:
                warning_msg = (
                    f"Removed {removed_count} missing files from bundle '{self.name}'"
                )
                logger.warning(warning_msg)
                show_temp_notification(warning_msg, type="warning")

    def export_code(self, further_documents: List[FileItem] = []) -> str:
        with logfire.span(
            "generating code_export for bundle {name}", name=self.name, _level="debug"
        ):
            all_items = set(self.file_items + further_documents)
            filtered_items = [fi for fi in all_items if not fi.is_dir]
            filtered_items_str = "\n".join(
                make_file_section(file_item, i)
                for i, file_item in enumerate(filtered_items)
            )
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<documents bundle-name="{self.name}" token-count="{self.tokens}">
{filtered_items_str}
</documents>"""


# REFERENCES
# https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
# https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips#example-multi-document-structure
def make_file_section(file_item: FileItem, index: int):
    return f"""    <document index="{index}">
        <source>
            {file_item}
        </source>
        <document_content>
{read_file(file_item.path)}
        </document_content>
    </document>"""
