from firestore_utils import get_firestore_db
from utils import get_cid_from_params
from streamlit_chat import message as chat_message


def render_messages(st, messages):
    user_picture_url = st.session_state.get("user_info", {}).get("picture", None)
    for i, message in enumerate(messages):
        if message.get("role") == "user":
            chat_message(
                message.get("content"),
                key=str(i) + "_user",
                is_user=True,
                logo=user_picture_url,
            )
        elif message.get("role") == "assistant":
            chat_message(
                message.get("content"),
                key=str(i) + "_assistant",
                allow_html=True,
                is_table=True,
            )
        elif message.get("role") == "system":
            # don't render system messages
            pass


def render_conversation(st, conversation):
    messages = conversation["messages"]
    render_messages(st, messages)
