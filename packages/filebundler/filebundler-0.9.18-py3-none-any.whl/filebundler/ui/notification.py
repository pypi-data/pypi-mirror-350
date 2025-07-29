# filebundler/ui/notification.py
import time
import random
import streamlit as st


def show_temp_notification(message: str, type="info", duration=3):
    """
    Show a temporary notification that automatically disappears.
    Notifications are stacked vertically with the newest at the bottom.

    Args:
        message: The message to display
        type: "info", "success", "warning", or "error"
        duration: Time in seconds before notification disappears
    """
    # Initialize notifications container in session state if it doesn't exist
    if "notifications" not in st.session_state:
        st.session_state.notifications = []

    # Create a unique key for this notification
    notification_id = (
        f"notification_{int(time.time() * 1000)}_{random.randint(0, 1000)}"
    )

    # Add notification to state with expiration time
    st.session_state.notifications.append(
        {
            "id": notification_id,
            "message": message,
            "type": type,
            "expires_at": time.time() + duration,
        }
    )

    # Remove expired notifications
    current_time = time.time()
    st.session_state.notifications = [
        n for n in st.session_state.notifications if n["expires_at"] > current_time
    ]

    # Create notification container and CSS for stacking
    st.markdown(
        """
        <style>
        .notification-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column-reverse;
            gap: 10px;
            max-height: 80vh;
            overflow-y: auto;
        }
        .notification {
            padding: 10px 20px;
            border-radius: 5px;
            color: white;
            opacity: 0;
            min-width: 200px;
            max-width: 300px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .notification-info {
            background-color: #0066cc;
        }
        .notification-success {
            background-color: #28a745;
        }
        .notification-warning {
            background-color: #ffc107;
            color: #212529;
        }
        .notification-error {
            background-color: #dc3545;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create HTML for all notifications
    notifications_html = '<div class="notification-container">'

    for notification in st.session_state.notifications:
        # Calculate remaining time for animation
        remaining_time = notification["expires_at"] - current_time
        notifications_html += f"""
        <div id="{notification["id"]}" 
             class="notification notification-{notification["type"]}"
             style="animation: fadeIn 0.3s ease forwards, fadeOut 0.5s ease forwards {max(0, remaining_time - 0.5)}s;">
            {notification["message"]}
        </div>
        """

    notifications_html += "</div>"

    # Add keyframe animations
    st.markdown(
        """
        <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes fadeOut {
            from { opacity: 1; transform: translateX(0); }
            to { opacity: 0; transform: translateX(20px); }
        }
        </style>
        """
        + notifications_html,
        unsafe_allow_html=True,
    )
