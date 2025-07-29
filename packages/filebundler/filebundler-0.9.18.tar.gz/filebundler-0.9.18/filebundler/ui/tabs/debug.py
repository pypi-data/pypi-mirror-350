# filebundler/ui/tabs/debug.py
import streamlit as st

from filebundler.ui.notification import show_temp_notification


def render_debug_tab():
    st.subheader("Test Notifications")
    col1, col2 = st.columns(2)

    with col1:
        notification_type = st.selectbox(
            "Notification Type",
            ["info", "success", "warning", "error"],
            key="debug_notification_type",
        )
        duration = st.slider(
            "Duration (seconds)",
            min_value=1,
            max_value=10,
            value=3,
            key="debug_notification_duration",
        )

    with col2:
        if st.button("Test Single Notification"):
            show_temp_notification(
                f"This is a test {notification_type} notification",
                type=notification_type,
                duration=duration,
            )

        if st.button("Test Stacked Notifications"):
            show_temp_notification(
                "First notification",
                type=notification_type,
                duration=duration,
            )
            show_temp_notification(
                "Second notification",
                type="success" if notification_type != "success" else "info",
                duration=duration + 2,
            )

    # Original debug content
    with st.expander("Debug State"):
        with st.echo():
            st.session_state.app.selections.selected_file_items
            st.session_state.app.bundles.current_bundle
