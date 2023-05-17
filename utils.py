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
        st.experimental_set_query_params(cid=cid)
        st.experimental_rerun()


def generate_conversation_title(openai, messages):
    user_messages = [m["content"] for m in messages if m["role"] == "user"]
    conversation = " ".join(user_messages)

    # Generate a prompt for the model
    prompt = f"""
    Based on the following user chat messages ---:

    ---
    {conversation}
    ---

    A title in 5 words or less, without quotation marks, for this conversation is:
    """

    # Use the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002", prompt=prompt, temperature=0.3, max_tokens=60
    )

    # Extract the generated title
    title = response["choices"][0]["text"].strip()

    return title


def get_key_from_params(st, key):
    params = st.experimental_get_query_params()
    if key in params:
        return params[key][0]
    else:
        return None


def get_cid_from_params(st):
    return get_key_from_params(st, "cid")


def get_oauth_uid(st):
    user_info = st.session_state.get("user_info", {})
    return user_info.get("id", None)
