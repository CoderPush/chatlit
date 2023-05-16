import openai
from firestore_utils import firestore_save
from utils import generate_conversation_title

def load_messages(conversation):
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


def generate_response(st, conversation, prompt, model):
    messages = load_messages(conversation)
    messages.append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    response = get_content(st, completion)
    usage = completion.usage.to_dict()

    messages.append(
        {"role": "assistant", "content": response})

    title = conversation.get("title", generate_conversation_title(openai, messages))

    conversation_record = {
        "messages": messages,
        "usage": usage,
        "model_name": model,
        "title": title
    }

    cid = st.session_state.get('cid', None)

    # store conversations to firestore
    new_conversation = firestore_save(cid, conversation_record)
    return new_conversation, response, usage



def render_chat_form(st, conversation):
    name = st.session_state.get('name', 'You')
    model = st.session_state['model']

    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area(f"{name}:", key='input', height=50)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        new_conversation, output, usage = generate_response(st, conversation, user_input, model)
        st.experimental_set_query_params(cid=new_conversation.id)
        st.experimental_rerun()

