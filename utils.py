import base64
import json


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
    button = st.sidebar.button(
        title, key=f"button_{cid}", disabled=selected, use_container_width=True
    )
    if button:
        st.session_state["cid"] = cid
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


def decode_token_from_params(st, key):
    try:
        base64_token = get_key_from_params(st, key)
        if base64_token:
            # decode token
            str_data = base64.b64decode(base64_token.encode("utf-8")).decode("utf-8")
            # convert to dict
            dict_data = json.loads(str_data)

            print("decode_token_from_params", dict_data)
            return dict_data
    except UnicodeDecodeError as e:
        st.error(e)
