from firestore_utils import delete_convo, edit_convo
from custom_js import render_copy_shared_convo_link
from constants import DEFAULT_CONVERSATION


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

    if "title_button" not in st.session_state:
        st.session_state["title_button"] = {}
    if cid not in st.session_state["title_button"]:
        st.session_state["title_button"][cid] = False

    with container:
        col1, col2, col3, col4 = st.columns([6, 1, 1, 1], gap="small")
        is_edit = st.session_state.get(f"edit_convo_button_{cid}", False)

        with col1:
            is_edit = st.session_state.get(f"edit_convo_button_{cid}", False)

            if is_edit:
                st.text_input(
                    "Edit Label",
                    title,
                    key=f"new_title_{cid}",
                    max_chars=30,
                    label_visibility="collapsed",
                )
            else:
                convo_button = st.button(
                    title,
                    key=f"title_{cid}",
                    disabled=selected,
                    use_container_width=True,
                )
                if convo_button:
                    for key in st.session_state["title_button"]:
                        st.session_state["title_button"][key] = False

                    st.session_state["title_button"][cid] = True
                    st.session_state["cid"] = cid
                    st.experimental_rerun()

            new_title = st.session_state.get(f"new_title_{cid}", "")
            if new_title and new_title != title:
                edit_convo(cid, new_label=new_title)
                st.session_state[f"new_title_{cid}"] = ""
                st.experimental_rerun()

        if st.session_state["title_button"][cid]:
            with col2:
                st.button(
                    ":outbox_tray:",
                    key=f"share_convo_button_{cid}",
                    disabled=False,
                    use_container_width=True,
                    on_click=lambda: render_copy_shared_convo_link(cid),
                )

            with col3:
                st.button(
                    ":pencil2:",
                    key=f"edit_convo_button_{cid}",
                    disabled=False,
                    use_container_width=True,
                )

            with col4:
                delete_button = st.button(
                    ":wastebasket:",
                    key=f"delete_convo_button_{cid}",
                    disabled=False,
                    use_container_width=True,
                )
                if delete_button:
                    delete_convo(cid)
                    st.session_state["cid"] = None
                    st.session_state["conversation"] = DEFAULT_CONVERSATION
                    st.experimental_rerun()
        else:
            with col4:
                open_button = st.button(
                    "📂", key=f"open_convo{cid}", use_container_width=True
                )
                if open_button:
                    st.session_state["cid"] = cid
                    st.experimental_rerun()

    css = """
        <style>
            div.css-ocqkz7.e1tzin5v3  {
                border: 1px solid #e6e6e6;
                border-radius: 4px;
                background-color: #fff;
            }
            div.css-ocqkz7.e1tzin5v3 .stButton > button {
                border: 1px solid transparent;
                background-color: #fff;
                align-items: center;
            }
            div.css-ocqkz7.e1tzin5v3 .stButton > button:hover {
                color: #6e6e6e;
            }
            div.css-ocqkz7.e1tzin5v3 [data-testid="column"]:first-child .stButton > button{
                justify-content: flex-start;
                width: 220px;
                overflow: hidden; 
                white-space: nowrap;
                position: relative;
                background: -webkit-linear-gradient(right, rgba(0,0,0,0), rgba(0,0,0,1));
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            div.css-ocqkz7.e1tzin5v3 [data-testid="column"]:nth-child(2) .stButton,
            div.css-ocqkz7.e1tzin5v3 [data-testid="column"]:nth-child(3) .stButton{
                position: relative;
            }
            div.css-ocqkz7.e1tzin5v3 [data-testid="column"]:nth-child(2) .stButton > button,
            div.css-ocqkz7.e1tzin5v3 [data-testid="column"]:nth-child(3) .stButton > button {
                position: absolute;
                top: 0;
            }
            div.css-ocqkz7.e1tzin5v3 [data-testid="column"]:nth-child(2) .stButton > button{
                right: -23px;
            }
            div.css-ocqkz7.e1tzin5v3 [data-testid="column"]:nth-child(3) .stButton > button{
                right: -15px;
            }
        </style>
        """

    st.sidebar.markdown(css, unsafe_allow_html=True)


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
