# filebundler/ui/tabs/auto_bundler/render_auto_bundler.py
import streamlit as st
from typing import Optional

from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.models.Bundle import Bundle
from filebundler.models.llm.AutoBundleResponse import AutoBundleResponse

from filebundler.ui.notification import show_temp_notification
from filebundler.ui.components.selectable_file_items import (
    render_selectable_file_items_list,
)

from filebundler.ui.tabs.auto_bundler.before_submit import (
    render_auto_bundler_before_submit_tab,
)


def render_auto_bundler_tab(app: FileBundlerApp):
    """Render the Auto-Bundle tab."""
    auto_bundle_response: Optional[AutoBundleResponse] = st.session_state.get(
        "auto_bundle_response", None
    )
    if auto_bundle_response is None:
        render_auto_bundler_before_submit_tab(app)
    else:
        # LLM suggestions header
        headercol1, headercol2 = st.columns([1, 1])
        with headercol1:
            st.write("The LLM suggested this bundle:")
        with headercol2:
            if st.button("Start over", help="Clear the current auto-bundle response"):
                st.session_state["auto_bundle_response"] = None
                # NOTE we should not need to reset this but because if the user does click the disabled button the lag may cause this to stay True
                st.session_state["submitting_to_llm"] = False
                st.rerun()
        # LLM suggestions
        if auto_bundle_response.message:
            with st.expander("LLM Message:", expanded=True):
                st.markdown(
                    """
<style>
    pre {
        white-space : pre-wrap !important;
        word-break: break-word;
    }
</style>""",
                    unsafe_allow_html=True,
                )
                st.markdown(f"""```\n{auto_bundle_response.message}\n```""")
                # st.markdown("""</code>""", unsafe_allow_html=True)

        if auto_bundle_response.code:
            with st.expander("Code:", expanded=True):
                st.markdown(f"""```\n{auto_bundle_response.code}\n```""")
        with st.expander("Very Likely Useful Files:", expanded=True):
            render_selectable_file_items_list(
                app,
                key_prefix="auto_bundle",
                from_paths=auto_bundle_response.files.very_likely_useful,
            )
            st.markdown("---")
        with st.expander("Probably Useful Files:", expanded=True):
            render_selectable_file_items_list(
                app,
                key_prefix="auto_bundle",
                from_paths=auto_bundle_response.files.probably_useful,
            )
        st.write(
            "Select the files you want to bundle. You may also select files from the file tree."
        )
        col1, col2 = st.columns([1, 1])
        with col1:
            new_bundle_name = st.text_input(
                "Enter a name for the new bundle",
                value=auto_bundle_response.name,
            )
        with col2:
            if st.button(
                "When you're done, click here to save the bundle",
                disabled=not new_bundle_name,
            ):
                new_bundle = Bundle(
                    name=new_bundle_name,
                    file_items=app.selections.selected_file_items,
                )
                app.bundles.save_one_bundle(new_bundle)
                show_temp_notification(
                    f"Bundle saved: {new_bundle.name}", type="success"
                )
                st.rerun()
