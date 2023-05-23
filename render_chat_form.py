from firestore_utils import firestore_save
from utils import get_oauth_uid
from chat_utils import generate_conversation_title, generate_stream


def save_messages_to_firestore(st, usage=None):
    messages = st.session_state["messages"]
    model = st.session_state["model"]

    if len(messages) > 0:
        conversation = st.session_state.get("conversation", {})
        title = conversation.get("title", None)
        if title is None:
            title = generate_conversation_title(messages)
        # get google uid from user_info object
        uid = get_oauth_uid(st)

        conversation_record = {
            "messages": messages,
            "usage": usage,
            "model_name": model,
            "title": title,
            "uid": uid,
        }

        cid = st.session_state.get("cid", None)

        # store conversations to firestore
        new_conversation = firestore_save(cid, conversation_record)
        print(new_conversation)
        return new_conversation


def render_chat_stream(st):
    with st.form(key="chat_prompt", clear_on_submit=True):
        stream_holder = st.empty()
        user_input = st.text_area(
            f"You:", key="text_area_stream", label_visibility="collapsed"
        )

        generating = st.session_state.get("generating", False)
        submit_button = st.form_submit_button(label="Send", disabled=generating)

    if submit_button and user_input:
        st.session_state["conversation_expanded"] = False
        st.session_state["generating"] = True
        generate_stream(st, stream_holder, user_input)
        st.session_state["generating"] = False
        new_conversation = save_messages_to_firestore(st)
        if new_conversation is not None:
            st.session_state["cid"] = new_conversation.id
            st.experimental_rerun()
