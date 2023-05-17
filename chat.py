from firestore_utils import load_conversation_by_id
from utils import get_key_from_params
from render_auth import render_auth
from render_body import render_body
from render_my_conversations import render_my_conversations
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "gpt-3.5-turbo"


def get_model_from_conversation(conversation: dict) -> str:
    """Extracts the model name from a conversation dictionary"""
    return conversation.get("model_name")


def load_and_store_conversation(st, cid: str):
    """Loads a conversation and stores it in the session state"""
    conversation = load_conversation_by_id(cid).to_dict()
    if conversation:
        st.session_state["conversation"] = conversation
        st.session_state["model"] = get_model_from_conversation(conversation)
    st.session_state["cid"] = cid


def controller():
    # TODO: display useful total cost in $
    st.session_state["total_cost"] = 0.0

    # set model in session if specified in params
    model_from_param = get_key_from_params(st, "model")
    if model_from_param:
        st.session_state["model"] = model_from_param

    # load conversation if cid is specified in params
    cid = get_key_from_params(st, "cid")
    if cid:
        load_and_store_conversation(st, cid)

    # set default model if no model specified
    if "model" not in st.session_state:
        st.session_state["model"] = DEFAULT_MODEL


DEFAULT_CONVERSATION = {}


def render_new_chat(sidebar):
    button_models = {"GPT-3.5 Chat": "gpt-3.5-turbo", "GPT-4 Chat": "gpt-4"}

    for button_text, model_type in button_models.items():
        if sidebar.button(
            button_text,
            key=f"button_{model_type}",
            use_container_width=True,
            type="primary",
        ):
            initialize_chat(model_type)


def initialize_chat(model: str):
    st.session_state["conversation"] = DEFAULT_CONVERSATION
    st.session_state["model"] = model
    st.session_state["cid"] = None
    st.experimental_set_query_params(model=model, cid="")
    st.experimental_rerun()


def render_history_menu(sidebar):
    sidebar.write("## Chat History")
    sidebar.markdown(
        """
        <style>
            a.link-row:hover div, a.selected div {
                background-color: #666;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    render_my_conversations(st, sidebar)


def render_sidebar(sidebar):
    render_new_chat(sidebar)
    render_auth(st)
    sidebar.divider()
    render_history_menu(sidebar)


def main():
    st.set_page_config(
        page_title="CoderGPT Chat", page_icon=":robot_face:", layout="wide"
    )
    controller()
    render_sidebar(st.sidebar)
    render_body(st)


if __name__ == "__main__":
    main()

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
