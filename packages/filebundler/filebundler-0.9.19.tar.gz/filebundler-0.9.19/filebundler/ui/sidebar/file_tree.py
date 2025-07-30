# filebundler/ui/sidebar/file_tree.py
import logging
import streamlit as st

from filebundler.models.FileItem import FileItem
from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.ui.sidebar.file_tree_buttons import render_file_tree_buttons

logger = logging.getLogger(__name__)


def render_file_tree(app: FileBundlerApp):
    """
    Render a file tree with checkboxes in the Streamlit UI

    Args:
        app: FileBundlerApp instance
    """

    st.subheader(
        f"Files ({app.selections.nr_of_selected_files}/{app.nr_of_files}) ({f'{app.root_item.tokens}'} tokens)"
    )

    def clear_search():
        st.session_state["file_tree_search"] = ""

    # Add search bar
    search_col1, search_col2 = st.columns([1, 1])
    with search_col1:
        search_term = st.text_input("🔍 Search files", key="file_tree_search")
    with search_col2:
        if search_term:
            if st.button("Clear Search", on_click=clear_search):
                st.rerun()

    render_file_tree_buttons(app)

    def matches_search(item: FileItem) -> bool:
        """Check if an item matches the search term"""
        if not search_term:
            return True
        search_lower = search_term.lower()
        return search_lower in item.name.lower()

    def has_matching_children(item: FileItem) -> bool:
        """Check if an item or any of its children match the search term"""
        if matches_search(item):
            return True
        return any(has_matching_children(child) for child in item.children)

    # Define recursive function to display directories and files
    def display_directory(file_item: FileItem, indent: int = 0):
        try:
            for child in file_item.children:
                # Skip if neither the item nor its children match the search
                if not has_matching_children(child):
                    continue

                checkbox_label = (
                    f"{'&nbsp;' * indent * 4}📁 **{child.name}** ({child.tokens} tokens)"
                    if child.is_dir
                    else f"{'&nbsp;' * indent * 4} {child.name} ({child.tokens} tokens)"
                )
                new_state = st.checkbox(
                    checkbox_label,
                    value=child.selected,
                    key=f"file_{child.path}",
                    help=f"Select {child.name} for bundling",
                )

                # Handle checkbox change
                if new_state != child.selected:
                    child.toggle_selected()
                    app.selections.save_selections()
                    st.rerun()

                if child.is_dir:
                    display_directory(child, indent + 1)

        except Exception as e:
            logger.error(f"Error displaying directory: {e}", exc_info=True)
            st.error(f"Error displaying directory: {str(e)}")

    try:
        # Display the file tree starting from root
        root_item = app.file_items[app.project_path]
        display_directory(root_item)
    except Exception as e:
        logger.error(f"Error rendering file tree: {e}", exc_info=True)
        st.error(f"Error rendering file tree: {str(e)}")
