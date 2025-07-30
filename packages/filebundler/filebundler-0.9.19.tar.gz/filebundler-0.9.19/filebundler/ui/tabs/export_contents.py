# filebundler/ui/tabs/export_contents.py
import logging
import streamlit as st

from filebundler.constants import SELECTIONS_BUNDLE_NAME

from filebundler.models.Bundle import Bundle
from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.ui.notification import show_temp_notification
from filebundler.services.code_export_service import copy_code_from_bundle

logger = logging.getLogger(__name__)


def render_export_contents_tab(app: FileBundlerApp):
    if app.selections.nr_of_selected_files == 0:
        st.warning("No files selected. Please select files to export.")
        return

    st.write(f"{app.selections.nr_of_selected_files} files selected for export.")

    if st.button("Show Preview - Copy to Clipboard", use_container_width=True):
        if app.selections.nr_of_selected_files == 0:
            show_temp_notification(
                "No files selected. Please select files to bundle.",
                type="warning",
            )
            return

        try:
            bundle_to_export = (
                app.bundles.current_bundle
                if app.bundles.current_bundle
                else Bundle(
                    name=SELECTIONS_BUNDLE_NAME,
                    file_items=app.selections.selected_file_items,
                )
            )

        except Exception as e:
            logger.error(
                f"Error exporting bundle: {e}\n{app.selections.selected_file_items = }",
                exc_info=True,
            )
            show_temp_notification(f"Error creating bundle: {str(e)}", type="error")
            return

        if bundle_to_export:
            # copies the contents to clipboard and displays notification
            copy_code_from_bundle(bundle_to_export)
            st.subheader("Export Preview")
            preview_expander = st.expander("Expand preview")

            with preview_expander:
                try:
                    st.code(bundle_to_export.export_code(), language="xml")
                except Exception as e:
                    logger.error(f"Preview error: {e}", exc_info=True)
                    st.error(f"Error generating preview: {str(e)}")
