from firestore_utils import get_firestore_db
from utils import link_row, get_cid_from_params

def render_my_conversations(st, sidebar):
    db = get_firestore_db()
    # TODO: load only conversations that belong to the user
    conversations = db.collection("conversations").stream()

    cid_from_params = get_cid_from_params(st)

    for c in conversations:
      selected = c.id == cid_from_params
      title = c.to_dict().get("title", c.id)
      link_row(sidebar, title, f"?cid={c.id}", selected=selected)
