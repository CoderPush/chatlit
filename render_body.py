from render_conversation import render_conversation
from render_chat_form import render_chat_form
from firestore_utils import get_firestore_db
from utils import get_cid_from_params

def load_conversation(st):
    cid = get_cid_from_params(st)
    if cid:
        db = get_firestore_db()
        return db.collection("conversations").document(cid).get().to_dict()


def render_body(st):
    conversation = load_conversation(st)

    if conversation is None:
        st.write("Invalid conversation ID. Start a [New Chat](?)")
        st.stop()
        return 

    render_conversation(st, conversation)
    render_chat_form(st, conversation)

