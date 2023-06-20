from firestore_utils import get_firestore_db


def render_user_message(st, message):
    user_message = f"""
        <div style="background-color: rgba(255, 227, 18, 0.2); \
                    color: rgb(255, 255, 194);
                    padding: 16px; \
                    border-radius: 0.25rem; \
                    line-height: 1.6; \
                    font-size: 1rem;" \
            >{message}</div>
    """
    st.markdown(user_message, unsafe_allow_html=True)

def render_messages(st, messages):
    for i, message in enumerate(messages):
        message_content = message.get("content")
        if message.get("role") == "user":
            st.warning(message.get("content"), icon="👤")
            render_user_message(st, message_content)
        elif message.get("role") == "assistant":
            st.info(message.get("content"), icon="🤖")
        elif message.get("role") == "system":
            # don't render system messages
            pass


def render_conversation(st, conversation):
    messages = conversation["messages"]
    render_messages(st, messages)
