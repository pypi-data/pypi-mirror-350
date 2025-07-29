# filebundler/ui/tabs/global_settings_panel.py
import streamlit as st

from filebundler.ui.notification import show_temp_notification
from filebundler.managers.GlobalSettingsManager import GlobalSettingsManager


def render_global_settings(gsm: GlobalSettingsManager):
    """Render the global settings tab"""
    st.header("Global Settings")

    gsm.settings.max_files = st.number_input(
        "Default max files to display",
        min_value=10,
        value=gsm.settings.max_files,
    )

    st.subheader("Default Ignore Patterns")

    if st.button("Save Global Settings"):
        success = gsm.save_settings()
        if success:
            show_temp_notification("Global settings saved", type="success")
        else:
            show_temp_notification("Error saving global settings", type="error")
