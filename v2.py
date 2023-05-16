import os
import openai
import streamlit as st
from utils import link_button

from dotenv import load_dotenv
load_dotenv()

from render_conversation import render_conversation
from render_my_conversations import render_my_conversations
from render_body import render_body
from render_auth import render_auth
from utils import get_key_from_params
from firestore_utils import load_conversation_by_id

def controller():
    openai.organization = os.environ["OPENAI_ORG_ID"]
    openai.api_key = os.environ["OPENAI_API_KEY"]
    st.session_state['total_cost'] = 0.0
    st.session_state['model'] = get_key_from_params(st, 'model') or 'gpt-3.5-turbo'
    cid = get_key_from_params(st, 'cid')
    if cid:
        st.session_state['cid'] = cid
        conversation = load_conversation_by_id(cid)
        st.session_state['conversation'] = conversation.to_dict()


def render_new_chat(sidebar):
    b1 = sidebar.button("GPT-3.5 Chat", key="button_gpt-3.5-turbo", use_container_width=True, type='primary')
    b2 = sidebar.button("GPT-4 Chat", key="button_gpt-4", use_container_width=True, type='primary')
    if b1:
        st.experimental_set_query_params(model="gpt-3.5-turbo")
        st.experimental_rerun()
    if b2:
        st.experimental_set_query_params(model="gpt-4")
        st.experimental_rerun()


def render_history_menu(sidebar):
    sidebar.write("## Chat History")
    sidebar.markdown("""
        <style>
            a.link-row:hover div, a.selected div {
                background-color: #666;
            }
        </style>
    """, unsafe_allow_html=True)

    render_my_conversations(st, sidebar)


def render_sidebar(sidebar):
    render_new_chat(sidebar)
    render_auth(st)
    sidebar.divider()
    render_history_menu(sidebar)

def main():
    st.set_page_config(page_title="CoderGPT Chat",
                    page_icon=":robot_face:", layout="wide")
    controller()
    render_sidebar(st.sidebar)
    render_body(st)

if __name__ == "__main__":
    main()

    with st.expander("Debug"):
        col1, col2 = st.columns(2)
        col1.write("Session State (w/o conversation, user_info))")
        # exclude conversation from session_state
        session_state = {k: v for k, v in st.session_state.items() if k != 'conversation' and k != 'user_info'}
        col1.write(session_state)
        col2.write("Conversation")
        col2.write(st.session_state.get('conversation'))
