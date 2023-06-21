from firestore_utils import get_firestore_db


def render_user_message(st, message, profile_url):
    user_message = f"""
        <div role="alert" data-baseweb="notification" class="st-ae st-af st-ag st-ah st-ai st-aj st-ak st-ee st-am st-ed st-an st-ao st-ap st-aq st-ar st-as st-ef st-au st-av st-aw st-ax st-ay st-bb st-b0 st-b1 st-b2 st-b3 st-b4 st-b5 st-b6 st-b7"><div class="st-b8 st-b9"><div class="css-17z2rne e13vu3m50"><div class="css-1w6rlcb e12sa3f30">
            <img src={profile_url} width=32 height=32 alt="Profile Picture">
            <div data-testid="stMarkdownContainer" class="css-nahz7x e16nr0p34">
                <p>{message}</p>
            </div>
        </div></div></div></div>
    """
    st.markdown(user_message, unsafe_allow_html=True)


def render_messages(st, messages):
    user_picture_url = st.session_state.get("user_info", {}).get("picture", None)
    for i, message in enumerate(messages):
        message_content = message.get("content")
        if message.get("role") == "user":
            render_user_message(st, message_content, user_picture_url)
        elif message.get("role") == "assistant":
            st.info(message.get("content"), icon="🤖")
        elif message.get("role") == "system":
            # don't render system messages
            pass


def render_conversation(st, conversation):
    messages = conversation["messages"]
    render_messages(st, messages)
