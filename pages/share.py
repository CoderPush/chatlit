import streamlit as st
from firestore_utils import load_conversation_by_id
from render_conversation import render_conversation


def main():
    try:
        queryStr = st.experimental_get_query_params()
        # get query cid from the queryStr
        cid = queryStr["cid"][0]
        # get the conversation from the cid
        conversation = load_conversation_by_id(cid).to_dict()
        st.title(conversation["title"])
        # show messages for the conversation
        render_conversation(st, conversation)
    except:
        st.title("Oops! Conversation not found")


main()
