from firestore_utils import get_firestore_db
from utils import button_row, get_cid_from_session, get_oauth_uid


def render_my_conversations(st, sidebar):
    db = get_firestore_db()
    uid = get_oauth_uid(st)
    cid_from_params = get_cid_from_session(st)
    model_name = st.session_state["model"]
    if uid:
        # load only conversations that belong to the user, newest first
        conversations = (
            db.collection("conversations")
            .where("uid", "==", uid)
            .where("model_name", "==", model_name)
            .order_by("created", direction="DESCENDING")
            .stream()
        )
    else:
        conversations = []

    for c in conversations:
        selected = c.id == cid_from_params
        conversation = c.to_dict()
        button_row(st, c.id, conversation, selected=selected)
