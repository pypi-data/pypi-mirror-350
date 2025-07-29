# filebundler/ui/sidebar/file_tree_buttons.py
import logging
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.services.project_structure import (
    save_project_structure,
)
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


def render_file_tree_buttons(app: FileBundlerApp):
    col1, col2 = st.columns([1, 1])

    with col1:
        # this button has less text so it's smaller than the other ones
        # TODO make all buttons the same size
        if st.button("Select All", key="select_all", use_container_width=True):
            app.selections.select_all_files()
            st.rerun()

        if st.button(
            "Export Structure", key="export_structure", use_container_width=True
        ):
            try:
                output_file = save_project_structure(app)

                show_temp_notification(
                    f"Project structure exported to {output_file.relative_to(app.project_path)}",
                    type="success",
                )

                app.selections.selected_file = output_file

            except Exception as e:
                logger.error(f"Error exporting project structure: {e}", exc_info=True)
                show_temp_notification(
                    f"Error exporting project structure: {str(e)}", type="error"
                )

            st.rerun()

    with col2:
        if st.button("Unselect All", key="unselect_all", use_container_width=True):
            app.selections.clear_all_selections()
            st.rerun()

        if st.button(
            "Refresh Project", key="refresh_project", use_container_width=True
        ):
            if st.session_state.app:
                try:
                    st.session_state.app.refresh()
                    show_temp_notification("Project refreshed", type="success")
                except Exception as e:
                    logger.error(f"Error refreshing project: {e}", exc_info=True)
                    show_temp_notification(
                        f"Error refreshing project: {str(e)}", type="error"
                    )
            else:
                show_temp_notification("No project loaded", type="error")
