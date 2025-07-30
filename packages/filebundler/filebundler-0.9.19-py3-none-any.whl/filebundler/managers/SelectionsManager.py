# filebundler/managers/SelectionsManager.py
import logging
import logfire

from pathlib import Path
from typing import Any, List, Optional

from filebundler.models.AppProtocol import AppProtocol

from filebundler.utils import json_dump, json_load, read_file
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


class SelectionsManager:
    """
    Manages the state of selected files and file selections persistence
    """

    def __init__(self, app: AppProtocol):
        self.app = app
        self.selected_file: Optional[Path] = None
        self.selections_file = self.app.psm.filebundler_dir / "selections.json"
        self.load_selections()

    def load_selections(self):
        with logfire.span(
            "loading selections for project {project}",
            project=self.app.project_path.name,
        ):
            logger.info(f"Loading selections for {self.app.project_path}")
            if not self.selections_file.exists():
                logger.warning(f"{self.selections_file = } hasn't been created yet")
                return

            with open(self.selections_file, "r") as f:
                selections_array: List[str] = json_load(f)

            if not selections_array:
                logger.warning("There were no selections to load")
                return

            selected_file_items = self.app.paths_to_file_items(
                [Path(p).resolve() for p in selections_array]
            )

            # Set selections
            for select_file_item in selected_file_items:
                select_file_item.selected = True

            logger.info(f"Loaded selections: {self.selected_file_items = }")

    @property
    def nr_of_selected_files(self):
        """Return the number of selected files"""
        return len(self.selected_file_items)

    @property
    def selected_file_items(self):
        """Return the selected file items - ONLY FILES"""
        return [v for v in self.app.file_items.values() if v.selected and not v.is_dir]

    @property
    def selected_file_content(self):
        """Return the contents of the selected files"""
        if not self.selected_file:
            return None
        return read_file(self.selected_file)

    def _persist_to_selections_file(self, data: Any):
        with open(self.selections_file, "w") as f:
            json_dump(data, f)

        logger.info(f"Saved {len(data)} selections to {self.selections_file}")

    def save_selections(self):
        """Save selected files to JSON file"""
        with logfire.span(
            "saving selections for project {project}",
            project=self.app.project_path.name,
        ):
            data = [file_item.path.as_posix() for file_item in self.selected_file_items]
            self._persist_to_selections_file(data)

    def select_all_files(self):
        """Select all files in the project"""
        with logfire.span(
            "selecting all files for project {project}",
            project=self.app.project_path.name,
        ):
            for file_item in self.app.file_items.values():
                # TODO we need to handle the cases when a dir is marked as selected, it should actually just mark its children
                if not file_item.is_dir:
                    file_item.selected = True

            self.save_selections()

            logger.info(f"Selected all {self.nr_of_selected_files} files")
            show_temp_notification(
                f"Selected all {self.nr_of_selected_files} files", type="success"
            )

    def clear_all_selections(self):
        """Clear all selected files"""
        try:
            with logfire.span(
                "clearing all selections for project {project}",
                project=self.app.project_path.name,
            ):
                nr_of_selected_files = self.nr_of_selected_files

                for file_item in self.app.file_items.values():
                    file_item.selected = False

                self.save_selections()

                logger.info(f"Unselected all {nr_of_selected_files} files")
                show_temp_notification(
                    f"Unselected all {len(self.app.file_items)} files", type="success"
                )
        except Exception as e:
            logger.error(f"Error unselecting all files: {e}", exc_info=True)
            show_temp_notification(
                f"Error unselecting all files: {str(e)}", type="error"
            )
