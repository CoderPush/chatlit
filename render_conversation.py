from firestore_utils import get_firestore_db
import streamlit as st


def render_messages(st, messages):
    user_picture_url = st.session_state.get("user_info", {}).get("picture", None)
    for i, message in enumerate(messages):
        if message.get("role") == "user":
            st.text_area(
                label="User Message",
                value=message.get("content"),
                key=str(i) + "_user",
            )
        elif message.get("role") == "assistant":
            st.markdown(
                message.get("content"),
                key=str(i) + "_assistant",
                unsafe_allow_html=True,
            )
        elif message.get("role") == "system":
            # don't render system messages
            pass


def render_conversation(st, conversation):
    messages = conversation["messages"]
    render_messages(st, messages)
