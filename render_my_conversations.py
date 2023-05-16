from firestore_utils import get_firestore_db
from utils import button_row, get_cid_from_params, get_oauth_uid

def hack_css(sidebar):
    sidebar.markdown("""
        <style>
            button[kind='secondary'] {
                display: inherit;
                text-align: left;
                border: 0;
            }
            button[kind='primary'] {
                background-color: inherit;
            }
        </style>
    """, unsafe_allow_html=True)

def render_my_conversations(st, sidebar):
    hack_css(sidebar)
    db = get_firestore_db()
    uid = get_oauth_uid(st)
    cid_from_params = get_cid_from_params(st)

    if uid:
        # load only conversations that belong to the user, newest first
        conversations = db.collection("conversations").where("uid", "==", uid).order_by("created", direction="DESCENDING").stream()
    else:
        conversations = []

    for c in conversations:
      selected = c.id == cid_from_params
      conversation = c.to_dict()
      button_row(st, c.id, conversation, selected=selected)
