import os
import openai
from streamlit_chat import message
from authenticator import authenticator_setup
from sidebar import init_sidebar, init_chat
from firestore_utils import firestore_save, get_firestore_db
from conversation_component import render_conversations, load_conversations
from model_switcher import render_model_switcher

import streamlit as st

# Set page title and header
st.set_page_config(page_title="CoderGPT", page_icon=":robot_face:")
st.sidebar.markdown("<h1 style='text-align: center;'>CoderGPT chat.</h1>",
                    unsafe_allow_html=True)

# Set org ID and API key from ENV variables
openai.organization = os.environ.get("OPENAI_ORG_ID")
openai.api_key = os.environ.get("OPENAI_API_KEY")

authenticator = authenticator_setup(st)


init_chat(st)

counter_placeholder = st.sidebar.empty()
counter_placeholder.write(
    f"Total cost since page load: ${st.session_state['total_cost']:.5f}")

st.sidebar.divider()
db = get_firestore_db()
init_sidebar(st, db)

history_container = st.sidebar.container()
render_conversations(st, history_container)

load_conversations(st, db)

model_selector = st.empty()
model_name = render_model_switcher(st, model_selector)


# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"


def get_content(response):
    # Handle the response from the API
    if 'choices' in response and len(response['choices']) > 0:
        choice = response['choices'][0]
        if 'message' in choice and 'content' in choice['message']:
            message_content = choice['message']['content']
            return message_content

    st.error(f"Error: {str(response)}")


def generate_response(prompt):
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages'],
    )

    response = get_content(completion)
    st.session_state['messages'].append(
        {"role": "assistant", "content": response})

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens

    conversation_record = {
        "messages": st.session_state['messages'],
        "usage": completion.usage.to_dict(),
        "model_name": model_name,
    }

    cid = st.session_state['cid'] if "cid" in st.session_state else None
    # store conversations to firestore
    firestore_save(
        db, cid, conversation_record)
    return response, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area(
            f"{st.session_state['name']}:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(
            user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'] = model_name
        st.session_state['total_tokens'] = total_tokens

        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state['cost'] = cost
        st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i],
                    is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i],
                    key=str(i), allow_html=True)
        st.write(
            f"Model used: {st.session_state['model_name']}; Number of tokens: {st.session_state['total_tokens']}; Cost: ${st.session_state['cost']:.5f}")
        counter_placeholder.write(
            f"Total cost of since page load: ${st.session_state['total_cost']:.5f}")
