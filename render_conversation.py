from firestore_utils import get_firestore_db

def render_messages(st, messages):
    for i, message in enumerate(messages):
        if message.get("role") == "user":
            st.warning(message.get("content"))
        elif message.get("role") == "assistant":
            st.info(message.get("content"))
        elif message.get("role") == "system":
            # don't render system messages
            pass


def render_conversation(st, conversation):
    messages = conversation["messages"]
    render_messages(st, messages)
