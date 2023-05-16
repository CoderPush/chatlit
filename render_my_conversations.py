from firestore_utils import get_firestore_db
from utils import button_row, get_cid_from_params

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
    # TODO: load only conversations that belong to the user
    conversations = db.collection("conversations").stream()

    cid_from_params = get_cid_from_params(st)

    for c in conversations:
      selected = c.id == cid_from_params
      conversation = c.to_dict()
      button_row(st, c.id, conversation, selected=selected)
