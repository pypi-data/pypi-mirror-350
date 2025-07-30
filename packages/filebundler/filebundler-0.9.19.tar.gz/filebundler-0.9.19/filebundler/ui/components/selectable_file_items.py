# filebundler/ui/components/selectable_file_items.py
import streamlit as st

from typing import List
from pathlib import Path

from filebundler.models.FileItem import FileItem
from filebundler.FileBundlerApp import FileBundlerApp


def render_selectable_file_items_list(
    app: FileBundlerApp,
    key_prefix: str,
    from_paths: List[Path] = [],
    from_items: List[FileItem] = [],
):
    file_items = app.paths_to_file_items(from_paths) if from_paths else from_items

    for file_item in file_items:
        selected = st.checkbox(
            label=str(file_item.relative),
            key=f"{key_prefix}_select_{file_item.path}",
            value=file_item.selected,
        )
        if selected != file_item.selected:
            file_item.toggle_selected()
            # BUG auto navigates away from the auto-bundle tab, also de-initializes the auto-bundle tab
            st.rerun()
