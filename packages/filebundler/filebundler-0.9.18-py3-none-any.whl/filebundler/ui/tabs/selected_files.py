# filebundler/ui/tabs/selected_files.py
import logging
import streamlit as st

from filebundler.models.Bundle import Bundle
from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.ui.notification import show_temp_notification
from filebundler.utils.language_formatting import set_language_from_filename

logger = logging.getLogger(__name__)


def render_selected_files_tab(app: FileBundlerApp):
    ocol1, ocol2 = st.columns([1, 1])
    with ocol1:
        st.subheader("Save Selected Files as a Bundle")
    with ocol2:
        # Add bundle name field for saving
        bundle_name = st.text_input(
            "Bundle name (lowercase, alphanumeric, with hyphens)",
            key="export_bundle_name",
            value=app.bundles.current_bundle.name if app.bundles.current_bundle else "",
            placeholder="my-bundle-name",
        )

        if st.button("Save Bundle", use_container_width=True, type="secondary"):
            try:
                if not bundle_name:
                    show_temp_notification(
                        "Please enter a bundle name to save the bundle.", type="warning"
                    )
                    return

                if not app.selections.selected_file_items:
                    show_temp_notification(
                        "No files selected. Please select files to bundle.",
                        type="warning",
                    )
                    return

                new_bundle = Bundle(
                    name=bundle_name, file_items=app.selections.selected_file_items
                )
                app.bundles.save_one_bundle(new_bundle)
                app.bundles.activate_bundle(new_bundle)

                show_temp_notification(
                    f"Bundle '{bundle_name}' saved with {len(new_bundle.file_items)} files.",
                    type="success",
                )

                st.rerun()
            except Exception as e:
                logger.error(f"Save bundle error: {e}", exc_info=True)
                show_temp_notification(f"Error saving bundle: {str(e)}", type="error")

    if app.selections.selected_file_items:
        st.text(
            "Click on a file to view its content. Click 'x' to remove a file from selection."
        )
        for file_item in app.selections.selected_file_items:
            relative_path = file_item.path.relative_to(app.project_path)

            # Create a row with file button and remove button
            col1, col2 = st.columns([10, 1])

            with col1:
                if st.button(
                    f"📄 {relative_path}",
                    key=f"selections_tab_{file_item.relative}",
                    use_container_width=True,
                ):
                    app.selections.selected_file = file_item.path
                    st.rerun()

            with col2:
                if st.button(
                    "❌",
                    key=f"remove_{file_item}",
                    help=f"Remove {file_item} from selection",
                ):
                    try:
                        file_item.toggle_selected()
                        show_temp_notification(
                            f"Removed {file_item.path.name} from selection",
                            type="info",
                        )
                        # If we were viewing this file, clear it
                        if app.selections.selected_file == file_item.path:
                            app.selections.selected_file = None

                        app.selections.save_selections()

                        st.rerun()
                    except Exception as e:
                        logger.error(
                            f"Error removing file from selection: {e}", exc_info=True
                        )
                        show_temp_notification(
                            f"Error removing file: {str(e)}", type="error"
                        )
    else:
        st.warning(
            "No files selected. Use the checkboxes in the file tree to select files."
        )

    # Show file content if a file is selected
    if app.selections.selected_file:
        st.subheader(f"File: {app.selections.selected_file.name}")

        language = set_language_from_filename(app.selections.selected_file)

        st.code(app.selections.selected_file_content, language=language)
