import streamlit as st

def debugger():
    with st.expander("Debug"):
        col1, col2 = st.columns(2)
        col1.write("Session State (w/o conversation, user_info))")
        # exclude conversation from session_state
        session_state = {
            k: v for k, v in st.session_state.items() if k != "conversation"
        }
        col1.write(session_state)
        col2.write("Conversation")
        col2.write(st.session_state.get("conversation"))