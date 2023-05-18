import openai
from firestore_utils import firestore_save
from utils import generate_conversation_title, get_oauth_uid


def load_messages(st):
    conversation = st.session_state.get("conversation", {})
    default = [{"role": "system", "content": "You are a helpful assistant."}]

    return conversation.get("messages", default)


def get_content(st, response):
    # Handle the response from the API
    if "choices" in response and len(response["choices"]) > 0:
        choice = response["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            message_content = choice["message"]["content"]
            return message_content

    st.error(f"Error: {str(response)}")


def generate_response(st, prompt):
    model = st.session_state["model"]
    messages = load_messages(st)
    messages.append({"role": "user", "content": prompt})

    print("openai.ChatCompletion.create with")
    print("model: ", model)
    print("messages: ", messages)
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    response = get_content(st, completion)
    messages.append({"role": "assistant", "content": response})

    print("generate_response -> completion: ", completion)
    usage = completion.usage.to_dict()

    return messages, usage


def save_to_firestore(st, messages, usage=None):
    model = st.session_state["model"]
    if len(messages) > 0:
        conversation = st.session_state.get("conversation", {})
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
            "uid": uid,
        }

        cid = st.session_state.get("cid", None)

        # store conversations to firestore
        new_conversation = firestore_save(cid, conversation_record)
        print(new_conversation)
        return new_conversation


def render_chat_form(st):
    name = st.session_state.get("user_info", {}).get("name", "You")
    model = st.session_state["model"]

    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area(
            f"{name}:", key="text_area", height=20, label_visibility="collapsed"
        )
        submit_button = st.form_submit_button(label="Submit")

    if submit_button and user_input:
        messages, usage = generate_response(st, user_input)
        new_conversation = save_to_firestore(st, messages, usage)
        if new_conversation is not None:
            st.experimental_set_query_params(cid=new_conversation.id)
        st.experimental_rerun()

# see sample-stream.json to know how to parse it
def generate_stream(st, holder, user_input):
    model = st.session_state["model"]
    messages = load_messages(st)
    messages.append({"role": "user", "content": user_input})

    print("openai.ChatCompletion.create with", model, messages)
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=True,
    )

    # first chunk should be
    # {
    #     "choices": [
    #     {
    #         "delta": {
    #         "role": "assistant"
    #         },
    #         "finish_reason": null,
    #         "index": 0
    #     }
    #     ],
    #     "created": 1684389483,
    #     "id": "chatcmpl-7HQwF5QPvTrDtYPOvBZbzFfDb9tcI",
    #     "model": "gpt-3.5-turbo-0301",
    #     "object": "chat.completion.chunk"
    # }

    # middle chunks are content:
    content = ""
    for chunk in completion:
        delta = chunk["choices"][0]["delta"]
        if "content" in delta:
            content += delta["content"]
            holder.markdown(content)

    # last chunk should be
    # {
    #     "choices": [
    #     {
    #         "delta": {},
    #         "finish_reason": "stop",
    #         "index": 0
    #     }
    #     ],
    #     "created": 1684389483,
    #     "id": "chatcmpl-7HQwF5QPvTrDtYPOvBZbzFfDb9tcI",
    #     "model": "gpt-3.5-turbo-0301",
    #     "object": "chat.completion.chunk"
    # }

    messages.append({"role": "assistant", "content": content})

    # No usage info in stream mode yet
    # https://community.openai.com/t/usage-info-in-api-responses/18862

    return messages


def render_chat_stream(st):
    name = st.session_state.get("user_info", {}).get("name", "You")

    with st.form(key="chat_prompt", clear_on_submit=True):
        holder = st.empty()
        user_input = st.text_area(
            f"{name}:", key="text_area_stream", label_visibility="collapsed"
        )
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        messages = generate_stream(st, holder, user_input)
        # print("messages: ", messages)
        new_conversation = save_to_firestore(st, messages)
        if new_conversation is not None:
            st.experimental_set_query_params(cid=new_conversation.id)
        st.experimental_rerun()

