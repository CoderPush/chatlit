import streamlit as st
import streamlit.components.v1 as components

def render_copy_shared_convo_link():
    shared_cid = st.session_state.get("shared_convo_cid", None)
    model = st.session_state.get("model", "gpt-3.5-turbo")

    if shared_cid and model:
        js = f"""
            <script>
                const shareUrl = window.parent.location.origin + "/share" + "?cid={shared_cid}&model={model}"
                window.parent.navigator.clipboard.writeText(shareUrl);
                window.parent.alert("Shared Link: " + shareUrl);
            </script>
            """

        components.html(js,width=0, height=0)

        st.session_state["shared_convo_cid"] = None
        
def render_custom_js():
    render_copy_shared_convo_link()

