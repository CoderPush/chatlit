import streamlit as st
import streamlit.components.v1 as components
import time

def delayed_execution(delay, function):
    time.sleep(delay)
    function()

def render_copy_shared_convo_link(shared_cid=None):
    model = st.session_state.get("model", "gpt-3.5-turbo")

    if shared_cid is not None:
        js = f"""
            <script>
                window.parent.navigator.permissions.query({{ name: "write-on-clipboard" }}).then((result) => {{
                    if (result.state == "granted" || result.state == "prompt") {{
                        alert("Write access granted!");
                    }}
                }});
                const shareUrl = window.parent.location.origin + "/share" + "?cid={shared_cid}&model={model}"

                window.parent.navigator.clipboard.writeText(shareUrl).then(() => {{
                    window.parent.alert("Copied to clipboard: " + shareUrl);
                }});
            </script>
            """
        
        components.html(js, width=0, height=0)



