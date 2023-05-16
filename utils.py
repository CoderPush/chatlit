
def link_button(st, text, path):
    st.write(
        f'''
        <a target="_self" href="{path}">
            <button kind="secondary" class="css-w770g5 edgvbvh10">
                <div class="css-x78sv8 e16nr0p34">
                {text}
                </div>
            </button>
        </a>
        ''',
        unsafe_allow_html=True
    )


def link_row(st, text, path, selected=False):
    if selected:
        class_name = "selected link-row"
    else:
        class_name = "link-row"

    st.write(
        f'''

        <a target="_self" href="{path}" style="display: block; color: inherit; text-decoration: none;" class="{class_name}">
          <div style="width: 100%; height: 100%; transition: background-color 0.3s; padding: 5px;">
          {text}
          </div>
        </a>
        ''',
        unsafe_allow_html=True
    )


def generate_conversation_title(openai, messages):
    user_messages = [m['content'] for m in messages if m['role'] == 'user']
    conversation = " ".join(user_messages)

    # Generate a prompt for the model
    prompt = f"""
    Based on the following user chat messages ---:

    ---
    {conversation}
    ---

    A title in 5 words or less for this conversation is:
    """

    # Use the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.3,
        max_tokens=60
    )

    # Extract the generated title
    title = response['choices'][0]['text'].strip()

    return title

def get_cid_from_params(st):
    params = st.experimental_get_query_params()
    if "cid" in params:
        cid = params["cid"][0]
        return cid
    else:
        return None

