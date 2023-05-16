from render_conversation import render_conversation
from render_chat_form import render_chat_form
from firestore_utils import get_firestore_db
from utils import get_cid_from_params

def load_conversation(st):
    cid = get_cid_from_params(st)
    if cid:
        db = get_firestore_db()
        return db.collection("conversations").document(cid).get().to_dict()

    return {}

def get_expander_text(st):
    user = st.session_state.get('user_info', {}).get('name', None)
    model = st.session_state.get('model')
    if user:
        text = f"### {model} with {user}"
    else:
        text = f"### {model}"
    return text

def render_body(st):
    with st.expander(get_expander_text(st)):
        st.write(st.session_state.get('user_info'))

    conversation = load_conversation(st)
    if conversation:
        render_conversation(st, conversation)

    if st.session_state.get('user_info'):
        render_chat_form(st)
    else:
        st.write("Please sign in to use")

