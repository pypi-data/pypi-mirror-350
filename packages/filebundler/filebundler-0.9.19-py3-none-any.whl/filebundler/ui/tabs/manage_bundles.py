# filebundler/ui/tabs/manage_bundles.py
import logging
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.managers.BundleManager import BundleManager
from filebundler.models.Bundle import Bundle

from filebundler.ui.notification import show_temp_notification
from filebundler.services.code_export_service import copy_code_from_bundle

logger = logging.getLogger(__name__)


def activate_bundle(name: str):
    """Callback for loading a bundle"""
    try:
        app: FileBundlerApp = st.session_state.app
        bundle = app.bundles._find_bundle_by_name(name)

        if not bundle:
            show_temp_notification(f"Bundle '{name}' not found", type="error")
            return

        # Clear current selections
        app.selections.clear_all_selections()

        # Mark selected files
        loaded_count = 0
        for file_item in bundle.file_items:
            corresponding_file_item = app.file_items.get(file_item.path)
            if not corresponding_file_item:
                warning_msg = (
                    f"File item not found in this project: {file_item.path = }"
                )
                logger.warning(warning_msg)
                show_temp_notification(warning_msg, type="warning")
                continue
            else:
                corresponding_file_item.selected = True
                loaded_count += 1

        app.selections.save_selections()
        app.bundles.activate_bundle(bundle)

        show_temp_notification(
            f"Loaded {loaded_count} of {len(bundle.file_items)} files from bundle '{name}'",
            type="success",
        )
        st.rerun()
    except Exception as e:
        logger.error(f"Error loading bundle: {e}", exc_info=True)
        show_temp_notification(f"Error loading bundle: {str(e)}", type="error")


def render_bundle_metadata(bundle: Bundle):
    """Render bundle metadata details"""

    st.write("**Bundle Details:**")
    st.write(f"Created: {bundle.metadata.created_at_str}")
    st.write(f"Size: {bundle.size_str}")
    st.write(f"Token count: {bundle.tokens}")

    # Show last modification date if available
    if bundle.last_modified_date:
        st.write(f"Last file modification: {bundle.last_modified_date_str}")

    # Last exported time with warning if stale
    if bundle.metadata.export_stats.last_exported:
        last_exported = bundle.metadata.export_stats.last_exported_str
        if bundle.is_stale:
            st.markdown(
                f"<span style='color:orange'>Last exported: {last_exported}</span> "
                f"⚠️ Files modified since export",
                unsafe_allow_html=True,
            )
        else:
            st.write(f"Last exported: {last_exported}")

    st.write(f"Export count: {bundle.metadata.export_stats.export_count}")


def render_saved_bundles(bundle_manager: BundleManager):
    """
    Render the list of saved bundles with improved UI and border separation

    Args:
        bundles: List of Bundle objects
    """
    # Add custom CSS for bundle styling
    st.markdown(
        """
    <style>
    /* Bundle container with border and margin */
    .bundle-container {
        border: 1px solid rgba(128, 128, 128, 0.4);
        border-radius: 5px;
        margin-bottom: 15px;
        overflow-x: ellipsis;
    }
    
    /* Make bundle buttons the same size */
    .bundle-buttons button {
        min-width: 80px !important;
    }
    
    /* Stale bundle styling */
    .bundle-stale {
        background-color: orange;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Display each bundle with border
    for bundle in bundle_manager.bundles_dict.values():
        # Add stale class if bundle is stale
        stale_class = " bundle-stale" if bundle.is_stale else ""
        st.markdown(
            f'<div class="bundle-container{stale_class}">', unsafe_allow_html=True
        )

        bundle_is_active = bundle is bundle_manager.current_bundle
        checkmark = "✅" if bundle_is_active else None
        title = f'Files in "{bundle.name}" ({len(bundle.file_items)} files | {bundle.tokens} tokens | {bundle.size_str})'

        # Bundle dropdown with files
        with st.expander(
            title,
            expanded=bundle_is_active,
            icon=checkmark,
        ):
            col1, col2 = st.columns([3, 2])

            with col1:
                # Show files
                st.write("**Files in bundle:**")
                for file_item in bundle.file_items:
                    st.write(f"- {file_item}")

            with col2:
                render_bundle_metadata(bundle)

        # Bundle actions with equal-sized buttons
        button_col1, button_col2, button_col3 = st.columns(3)
        with button_col1:
            activate_bundle_help = """Activating a bundle will select the files in the bundle.
Selecting new files will not automatically add them to the bundle. 
You must manually save the bundle again if you want to add them.
"""
            if st.button(
                "Activate",
                key=f"activate_{bundle.name}",
                use_container_width=True,
                help=activate_bundle_help,
            ):
                activate_bundle(bundle.name)
        with button_col2:
            if st.button(
                "Copy to Clipboard",
                key=f"create_{bundle.name}",
                use_container_width=True,
                help="Copies the exported contents to clipboard without activating the bundle.",
            ):
                # copies the contents to clipboard and displays notification
                copy_code_from_bundle(bundle)
                # Update the bundle in the manager to persist the export record
                bundle_manager._save_bundle_to_disk(bundle)
        with button_col3:
            if st.button(
                "Delete", key=f"delete_{bundle.name}", use_container_width=True
            ):
                delete_bundle(bundle_manager, bundle.name)

        st.markdown("</div>", unsafe_allow_html=True)
    if not bundle_manager.bundles_dict:
        st.warning("No saved bundles to display.")


def delete_bundle(bundle_manager: BundleManager, name: str):
    """Callback for deleting a bundle"""
    # FUTURE: Add confirmation dialog
    try:
        bundle = bundle_manager._find_bundle_by_name(name)
        if not bundle:
            show_temp_notification(f"Bundle '{name}' not found", type="error")
            return
        if bundle is bundle_manager.current_bundle:
            bundle_manager.current_bundle = None
        bundle_manager.delete_bundle(bundle)
        st.rerun()
    except Exception as e:
        logger.error(f"Error deleting bundle: {e}", exc_info=True)
        show_temp_notification(f"Error deleting bundle: {str(e)}", type="error")
