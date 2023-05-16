import os
import openai
import streamlit as st
from utils import link_button

from dotenv import load_dotenv
load_dotenv()

from render_conversation import render_conversation
from render_my_conversations import render_my_conversations
from render_chat_form import render_chat_form
from render_body import render_body

def init_values():
    openai.organization = os.environ["OPENAI_ORG_ID"]
    openai.api_key = os.environ["OPENAI_API_KEY"]
    st.session_state['total_cost'] = 0.0
    st.session_state['model'] = "gpt-3.5-turbo"

def render_new_chat(sidebar):
    link_button(sidebar, "New Chat", "/")


def render_history_menu(sidebar):
    sidebar.write("## Chat History")
    render_my_conversations(st, sidebar)

def render_total_cost(sidebar):
    counter_placeholder = st.sidebar.empty()
    if 'total_cost' in st.session_state:
        counter_placeholder.write(
        f"Total cost since page load: ${st.session_state.total_cost:.5f}")

def render_sidebar(sidebar):
    render_new_chat(sidebar)
    render_total_cost(sidebar)
    sidebar.divider()
    render_history_menu(sidebar)

def main():
    st.set_page_config(page_title="CoderGPT Chat",
                    page_icon=":robot_face:", layout="wide")
    init_values()
    render_sidebar(st.sidebar)
    render_body(st)

if __name__ == "__main__":
    main()