# filebundler/app.py
import sys
import logging
import logfire
import streamlit as st

from filebundler import constants

from filebundler.state import initialize_session_state

from filebundler.ui.tabs.debug import render_debug_tab
from filebundler.ui.tabs.manage_bundles import render_saved_bundles
from filebundler.ui.tabs.selected_files import render_selected_files_tab
from filebundler.ui.tabs.export_contents import render_export_contents_tab
from filebundler.ui.tabs.global_settings_panel import render_global_settings
from filebundler.ui.tabs.auto_bundler.render_auto_bundler import render_auto_bundler_tab

from filebundler.ui.sidebar.file_tree import render_file_tree
from filebundler.ui.sidebar.settings_panel import render_settings_panel
from filebundler.ui.sidebar.project_selection import render_project_selection

from filebundler.ui.notification import show_temp_notification

# NOTE we do this here because this is the entry point for the Streamlit app
env_settings = constants.get_env_settings()
LOG_LEVEL = logging._nameToLevel[env_settings.log_level.upper()]  # type: ignore

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def cleanup():
    """Perform any necessary cleanup operations before exit"""
    logger.info("FileBundler shutting down gracefully...")
    # NOTE we can add any cleanup code hereif we need it (close file handles, save state, etc.)


def main():
    logfire.configure(send_to_logfire="if-token-present")

    """The actual Streamlit application logic"""
    try:
        st.set_page_config(page_title="File Bundler", layout="wide")

        initialize_session_state()

        with st.sidebar:
            (tab1, tab2) = st.tabs(["Project", "Project Settings"])
            with tab1:
                render_project_selection(
                    st.session_state.global_settings_manager.settings
                )
                if st.session_state.app:
                    render_file_tree(st.session_state.app)

            with tab2:
                if st.session_state.app:
                    render_settings_panel(st.session_state.app)
                else:
                    st.warning("Please open a project to configure settings.")

        st.write(  # type: ignore
            "Bundle project files together for prompting, or estimating and optimizing token and context usage."
        )
        main_tab1, main_tab2, debug_tab = st.tabs(
            [
                "File Bundler",
                "Global Settings",
                "Debug" if env_settings.is_dev else "About",
            ]
        )
        with main_tab1:
            # Only show if project is loaded
            if st.session_state.app:
                tab1, tab2, tab3, tab4 = st.tabs(  # type: ignore
                    [
                        f"Selected Files ({st.session_state.app.selections.nr_of_selected_files})",
                        "Export Contents",
                        f"Manage Bundles ({st.session_state.app.bundles.nr_of_bundles})",
                        "Auto-Bundle",
                    ]
                )

                with tab1:
                    logging.info("Rendering selected files tab")
                    render_selected_files_tab(st.session_state.app)

                with tab2:
                    render_export_contents_tab(st.session_state.app)

                with tab3:
                    render_saved_bundles(st.session_state.app.bundles)

                with tab4:
                    render_auto_bundler_tab(st.session_state.app)
            else:
                # If no project loaded
                show_temp_notification(
                    "Please open a project to get started", type="info"
                )
        with main_tab2:
            render_global_settings(st.session_state.global_settings_manager)

        if env_settings.is_dev and st.session_state.app:
            with debug_tab:
                render_debug_tab()
    except KeyboardInterrupt:
        # This might not always be reached due to how Streamlit works
        logger.info("Keyboard interrupt detected")
        cleanup()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
