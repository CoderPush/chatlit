from conversation_component import load_history_items
from utils import link_button


def init_sidebar(st, db):
    link_button(st.sidebar, "New Chat", "/")

    st.sidebar.divider()
    st.sidebar.write("## Chat History")
    st.session_state["history_items"] = load_history_items(st, db)


def init_chat(st):
    # Initialise session state variables
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    if 'model_name' not in st.session_state:
        st.session_state['model_name'] = 'GPT-3.5'
    if 'cost' not in st.session_state:
        st.session_state['cost'] = []
    if 'total_tokens' not in st.session_state:
        st.session_state['total_tokens'] = []
    if 'total_cost' not in st.session_state:
        st.session_state['total_cost'] = 0.0
