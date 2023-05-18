from render_conversation import render_conversation
from render_chat_form import render_chat_form, render_chat_stream
from firestore_utils import get_firestore_db
from utils import get_cid_from_params
from firestore_utils import clear_user_history


def load_conversation(st):
    cid = get_cid_from_params(st)
    if cid:
        db = get_firestore_db()
        return db.collection("conversations").document(cid).get().to_dict()

    return {}


def get_expander_text(st):
    user = st.session_state.get("user_info", {}).get("name", None)
    model = st.session_state.get("model")
    if user:
        text = f"### {model} with {user}"
    else:
        text = f"### {model}"
    return text


def render_body(st):
    with st.expander(get_expander_text(st)):
        user_info = st.session_state.get("user_info")
        if user_info:
            st.write(f"Signed in as {user_info.get('email')}")
            st.image(user_info.get("picture"), width=50)
            signout = st.button("Sign out", key="button_signout", type="primary")
            if signout:
                st.session_state.clear()
                st.experimental_rerun()
            st.write(
                "While it's useful to resume past conversations, sometimes you may want to clear your chat history."
            )
            placeholder = st.empty()
            with placeholder:
                clear_history = st.button(
                    "Clear History", key="button_clear_history", type="primary"
                )
            if clear_history:
                clear_user_history(user_info["id"])
                placeholder.info("Chat history cleared", icon="✅")
                st.snow()

    conversation = load_conversation(st)
    if conversation:
        render_conversation(st, conversation)

    if st.session_state.get("user_info"):
        # render_chat_form(st)
        render_chat_stream(st)
    else:
        # load homepage.md into a string
        with open("content/overview.md", "r") as f:
            overview = f.read()
            st.write(overview)
