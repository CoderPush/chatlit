import streamlit as st
from firestore_utils import load_conversation_by_id
from render_conversation import render_conversation
from render_auth import render_auth
from render_chat_form import render_chat_stream, save_messages_to_firestore
from google_utils import decode_token_from_params
from render_body import render_body
from debugger import debugger
import time


def is_authenticated(st):
    if "token" not in st.session_state:
        return False
    else:
        token = st.session_state["token"]
        expires_at = token.get("expires_at")
        if expires_at and expires_at < time.time():
            return False
        else:
            return True


def controller():
    st.session_state["conversation_expanded"] = True

    token_dict = decode_token_from_params(st, "token")
    if token_dict:
        st.session_state["token"] = token_dict


def show_readonly_shared_conversation(st, cid, model):
    # get the conversation from the cid
    conversation = load_conversation_by_id(cid).to_dict()
    st.title(conversation["title"])
    # show messages for the conversation
    render_conversation(st, conversation)

    continue_convo_holder = st.empty()
    continue_convo_btn = continue_convo_holder.button("Continue the chat")
    if continue_convo_btn:
        if not is_authenticated(st):
            continue_convo_holder.write(
                "You must be logged in to continue the conversation"
            )
        else:
            continue_convo_holder.empty()
            with st.container():
                # Save conversation to firestore
                st.session_state["messages"] = conversation["messages"]
                st.session_state["model"] = model
                st.session_state["conversation"] = conversation
                # save the state
                st.session_state[f"edit_shared_conversation_{cid}"] = True
                # rerun the app
                st.experimental_rerun()


def main():
    st.set_page_config(
        page_title="PushGPT Share", page_icon=":robot_face:", layout="wide"
    )
    controller()
    try:
        # get query cid from the queryStr
        queryStr = st.experimental_get_query_params()
        cid = queryStr["cid"][0]
        model = queryStr["model"][0]

        # render auth
        render_auth(st)

        # render body
        isEdit = st.session_state.get(f"edit_shared_conversation_{cid}", False)
        if not isEdit:
            show_readonly_shared_conversation(st, cid, model)
        else:
            render_body(st)

    except Exception as e:
        st.title("No conversation found")


if __name__ == "__main__":
    main()
    debugger()
