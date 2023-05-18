from render_conversation import render_conversation
from render_chat_form import render_chat_form, render_chat_stream
from firestore_utils import get_firestore_db
from utils import get_cid_from_params, get_expander_text


def load_conversation_from_db(st):
    cid = get_cid_from_params(st)
    if cid:
        db = get_firestore_db()
        return db.collection("conversations").document(cid).get().to_dict()

    return {}


def load_conversation_from_session_state(st):
    return st.session_state.get("conversation", {})


def render_body(st):
    messages_holder = st.expander(
        get_expander_text(st), expanded=st.session_state["conversation_expanded"]
    )
    with messages_holder:
        # load_conversation from session_state
        conversation = load_conversation_from_session_state(st)
        if conversation:
            render_conversation(st, conversation)

    if st.session_state.get("user_info"):
        with st.container():
            # render_chat_form(st)
            render_chat_stream(st)
    else:
        # load homepage.md into a string
        with open("content/overview.md", "r") as f:
            overview = f.read()
            st.write(overview)
