from firestore_utils import get_firestore_db


def render_message(st, message, profile_url, role):
    user_message = ""
    if role == "user":
        user_message = f"""
            <div style="width: 80%; display:flex; justify-content: flex-end; margin-left: auto; background-color: rgba(146, 108, 5, 0.1); margin-bottom: 20px; border-radius: 4px; padding: 10px">
                <div style="margin-right: 10px"><p>{message}</p></div>
                <img src={profile_url} width=32 height=32 alt="Profile Picture">
            </div>
        """
    elif role == "assistant":
        user_message = f"""
            <div style="width: 80%; display:flex; background-color: rgba(28, 131, 225, 0.1); margin-bottom: 20px; border-radius: 4px; padding: 10px">
                <div style="width: 32px; height: 32px">🤖</div>
                <div style="margin-left: 10px; overflow: auto; max-width: 100%">{message}</div>
            </div>
        """

    st.markdown(user_message, unsafe_allow_html=True)


def render_messages(st, messages):
    user_picture_url = st.session_state.get("user_info", {}).get("picture", None)

    for _, message in enumerate(messages):
        message_content = message.get("content")
        if message.get("role") == "user":
            render_message(st, message_content, user_picture_url, "user")
        elif message.get("role") == "assistant":
            render_message(st, message_content, "", "assistant")
        elif message.get("role") == "system":
            # don't render system messages
            pass


def render_conversation(st, conversation):
    messages = conversation["messages"]
    render_messages(st, messages)
