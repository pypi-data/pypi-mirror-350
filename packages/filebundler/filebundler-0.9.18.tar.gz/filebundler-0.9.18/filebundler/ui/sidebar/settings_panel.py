# filebundler/ui/sidebar/settings_panel.py
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.ui.notification import show_temp_notification


def render_settings_panel(app: FileBundlerApp):
    if st.session_state.app:
        app.psm.project_settings.max_files = st.number_input(
            "Max files to display",
            min_value=10,
            value=app.psm.project_settings.max_files,
        )

        # Add sorting controls
        st.subheader("File Sorting")
        app.psm.project_settings.sort_files_first = st.checkbox(
            "Show files before folders",
            value=app.psm.project_settings.sort_files_first,
            help="When enabled, files will be displayed before folders in the file tree",
        )

        # Auto Bundle Settings
        st.subheader("Auto Bundle Settings")
        auto_settings = app.psm.project_settings.auto_bundle_settings

        auto_settings.auto_refresh_project_structure = st.checkbox(
            "Auto-refresh project structure",
            value=auto_settings.auto_refresh_project_structure,
            help="Automatically refresh the project structure when files change",
        )

        auto_settings.auto_include_bundle_files = st.checkbox(
            "Auto-include bundle files",
            value=auto_settings.auto_include_bundle_files,
            help="Automatically include relevant files in the bundle",
        )

        st.subheader("Ignore Patterns")
        st.write("Files matching these patterns will be ignored (glob syntax)")  # type: ignore

        with st.expander("Show/Hide Ignore Patterns", expanded=False):
            updated_patterns = st.text_area(
                "Edit ignore patterns",
                "\n".join(app.psm.project_settings.ignore_patterns),
            )

            if updated_patterns:
                app.psm.project_settings.ignore_patterns = updated_patterns.split("\n")

        # Save button for all settings
        if st.button("Save Settings"):
            success = app.psm.save_project_settings()

            if success:
                show_temp_notification("Settings saved", type="success")
            else:
                show_temp_notification("Error saving settings", type="error")
    else:
        st.info("Open a project to configure settings")
