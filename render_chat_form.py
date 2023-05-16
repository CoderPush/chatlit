import openai
from firestore_utils import firestore_save
from utils import generate_conversation_title, get_oauth_uid

def load_messages(st):
    conversation = st.session_state.get('conversation', {})
    default = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    return conversation.get('messages', default)


def get_content(st, response):
    # Handle the response from the API
    if 'choices' in response and len(response['choices']) > 0:
        choice = response['choices'][0]
        if 'message' in choice and 'content' in choice['message']:
            message_content = choice['message']['content']
            return message_content

    st.error(f"Error: {str(response)}")


def generate_response(st, prompt, model):
    messages = load_messages(st)
    messages.append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    response = get_content(st, completion)
    messages.append({"role": "assistant", "content": response})

    usage = completion.usage.to_dict()

    return messages, usage

def save_to_firestore(st, messages, usage, model):
    conversation = st.session_state.get('conversation', {})
    if conversation and len(messages) > 0:
        title = conversation.get("title", None)
        if title is None:
            title = generate_conversation_title(openai, messages)
        # get google uid from user_info object
        uid = get_oauth_uid(st)

        conversation_record = {
            "messages": messages,
            "usage": usage,
            "model_name": model,
            "title": title,
            "uid": uid
        }

        cid = st.session_state.get('cid', None)

        # store conversations to firestore
        new_conversation = firestore_save(cid, conversation_record)
        return new_conversation

def render_chat_form(st):
    name = st.session_state.get('user_info', {}).get('name', 'You')
    model = st.session_state['model']

    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area(f"{name}:", key='text_area', height=20)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        messages, usage = generate_response(st, user_input, model)
        new_conversation = save_to_firestore(st, messages, usage, model)
        st.experimental_set_query_params(cid=new_conversation.id)
        st.experimental_rerun()

