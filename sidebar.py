from conversation_component import load_history_items


def init_sidebar(st, db):
    # write a link to visit ? to reset cid to null
    new_chat = st.sidebar.button("New Chat")
    if new_chat:
        st.sidebar.write("Click [New Tab](?) as a workaround.")

    st.sidebar.divider()
    load_history = st.sidebar.button("Chat History")
    if load_history:
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
