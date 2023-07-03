from firestore_utils import firestore_create_new_bot, firestore_get_all_bots, firestore_delete_all_bots
import streamlit as st
from google_utils import decode_token_from_params
from debugger import debugger

def list_bots():
    bots = firestore_get_all_bots()
    for b in bots:
        bot = b.to_dict()
        st.write(b.id, bot)

def render_bot_list():
    bots = firestore_get_all_bots()
    for b in bots:
        bot = b.to_dict()
        st.write(b.id, bot)

def create_bot_form():
    with st.form("create_a_bot_form"):
        # Bot Name
        name = st.text_input('Name')
        # Bot Description
        description = st.text_input('Description')
        # Model Name
        model = st.selectbox(
            "GPT model",
            ("gpt-3.5-turbo", "gpt-4")
        )
        # Prompt
        prompt = st.text_input('Prompt')

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            bot_info = {
                "name": name,
                "description": description,
                "model": model,
                "prompt": prompt
            }
            firestore_create_new_bot(bot_info)
            st.experimental_rerun()


def controller():
    create_bot_form()
    
def render_body():
    st.header("🤖 Create a Bot")
    controller()

def render_sidebar(sidebar):
    sidebar.divider()
    render_bot_list()

def main():
    st.set_page_config(
        page_title="PushGPT Create Bot", page_icon=":robot_face:", layout="wide"
    )
    render_sidebar(st.sidebar)
    st.header("🤖 Create a Bot")
    controller()
    


if __name__ == "__main__":
    main()
    debugger()
