from firestore_utils import delete_convo
from firestore_utils import update_conversation_name_by_id

def link_button(st, text, path):
    st.write(
        f"""
        <a target="_self" href="{path}">
            <button kind="secondary" class="css-w770g5 edgvbvh10">
                <div class="css-x78sv8 e16nr0p34">
                {text}
                </div>
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )


def link_row(st, text, path, selected=False):
    if selected:
        class_name = "selected link-row"
    else:
        class_name = "link-row"

    st.write(
        f"""

        <a target="_self" href="{path}" style="display: block; color: inherit; text-decoration: none;" class="{class_name}">
          <div style="width: 100%; height: 100%; transition: background-color 0.3s; padding: 5px;">
          {text}
          </div>
        </a>
        """,
        unsafe_allow_html=True,
    )


def button_row(st, cid, conversation, selected=False):
    title = conversation.get("title", cid)
    container = st.sidebar.container()
    with container:
        col_1, col_2, col_3 = st.columns([5, 1, 1])

        with col_1:
            convo_button = st.button(
                title, key=f"button_{cid}", disabled=selected, use_container_width=True
            )
            if convo_button:
                st.session_state["cid"] = cid
                st.experimental_rerun()

        with col_2:
            delete_button = st.button(
                "🗑️",
                key=f"delete_convo_button_{cid}",
                disabled=selected,
                use_container_width=True,
            )
            if delete_button:
                delete_convo(cid)
                st.experimental_rerun()

        with col_3:
            rename_button = st.button("🖊️", disabled=selected, use_container_width=True)
        
        if rename_button:
            st.text_input("New Conversation Name:", value=title, key=f"rename_input_{cid}")
            rename_input = st.session_state.get(f"rename_input_{cid}", "")
            if rename_input != title:
                update_conversation_name_by_id(cid, rename_input)
                st.experimental_rerun()

def get_key_from_params(st, key):
    params = st.experimental_get_query_params()
    if key in params:
        return params[key][0]
    else:
        return None


def get_cid_from_params(st):
    return get_key_from_params(st, "cid")


def get_cid_from_session(st):
    return st.session_state.get("cid", None)


def get_oauth_uid(st):
    user_info = st.session_state.get("user_info", {})
    return user_info.get("id", None)


def get_expander_text(st):
    user = st.session_state.get("user_info", {}).get("name", None)
    model = st.session_state.get("model")
    messages = st.session_state.get("conversation", {}).get("messages", [])
    user_messages = [m for m in messages if m.get("role") == "user"]
    if user:
        text = f"### {model} with {user}"
    else:
        text = f"### {model}"

    if len(messages) > 0:
        text += f" ({len(user_messages)} messages)"
    return text
