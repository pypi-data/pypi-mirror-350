# filebundler/ui/sidebar/project_selection.py
import os
import logging
import streamlit as st

from pathlib import Path

from filebundler.constants import DISPLAY_NR_OF_RECENT_PROJECTS

from filebundler.ui.notification import show_temp_notification
from filebundler.services.project_structure import save_project_structure

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.models.GlobalSettings import GlobalSettings


logger = logging.getLogger(__name__)


def open_selected_project(project_path: str):
    """Load a project and its settings"""

    project_path_obj = Path(project_path)
    if not project_path_obj.exists() or not project_path_obj.is_dir():
        logger.error(f"Invalid directory path: {project_path}")
        show_temp_notification("Invalid directory path", type="error")
        return False

    try:
        # Load project settings BEFORE loading the project
        # This ensures ignore patterns are available when loading the file tree
        app = FileBundlerApp(project_path=project_path_obj)
        st.session_state.app = app

        # Add to recent projects
        st.session_state.global_settings_manager.add_recent_project(app.project_path)

        logger.info(f"Project loaded: {app.project_path}")
        show_temp_notification(f"Project loaded: {app.project_path}", type="success")

        save_project_structure(app)
        return True
    except Exception as e:
        logger.error(f"Error loading project: {e}", exc_info=True)
        show_temp_notification(f"Error loading project: {str(e)}", type="error")
        return False


def render_project_selection(global_settings: GlobalSettings):
    """Render the project selection section"""
    project_path = ""
    with st.expander("Select Project", expanded=not st.session_state.app):
        if global_settings.recent_projects:
            project_source = st.radio(
                "Choose project source:",
                options=["Select recent project", "Enter manually"],
            )

            if project_source == "Select recent project":
                selected_recent: str = st.selectbox(
                    "Recent projects:",
                    options=global_settings.recent_projects_str[
                        :DISPLAY_NR_OF_RECENT_PROJECTS
                    ],
                    format_func=lambda x: os.path.basename(x) + f" ({x})",
                )
                if selected_recent:
                    project_path = selected_recent
            else:
                explicit_project_path = st.text_input(
                    "Project Path",
                    value="",
                )
                if explicit_project_path:
                    project_path = explicit_project_path
        else:
            # No recent projects, just show the text input
            project_path_input = st.text_input(
                "Project Path",
                value="",
            )
            if project_path_input:
                project_path = project_path_input

        if st.button("Open Project") and project_path:
            open_selected_project(project_path)
            st.rerun()
