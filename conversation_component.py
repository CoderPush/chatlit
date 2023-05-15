
def render_conversations(st, sidebar):
    if "history_items" in st.session_state:
        for conversation_id in st.session_state["history_items"]:
            sidebar.write(f"[{conversation_id}](?cid={conversation_id})")


def load_history_items(st, db):
    collection_ref = db.collection("conversations")
    return [conversation.id for conversation in collection_ref.stream()]


def load_conversations(st, db):
    params = st.experimental_get_query_params()
    collection_ref = db.collection("conversations")

    if "cid" in params:
        cid = params["cid"][0]
        st.session_state["cid"] = cid
        # get conversation fromm cid
        conversation = collection_ref.document(cid).get().to_dict()
        if conversation is None:
            st.write("Invalid conversation ID. Start a [New Chat](?)")
            st.stop()

        messages = conversation["messages"]
        st.session_state["messages"] = messages
        # loop through messages:
        #   - if role is user, add to past in session state
        #   - if role is assistant, add to generated in session state
        st.session_state["past"] = []
        st.session_state["generated"] = []
        for message in messages:
            if message["role"] == "user":
                st.session_state["past"].append(message["content"])
            elif message["role"] == "assistant":
                st.session_state["generated"].append(message["content"])

        usage = conversation["usage"]
        model_name = conversation["model_name"]
        total_tokens = usage["total_tokens"]
        prompt_tokens = usage["prompt_tokens"]
        completion_tokens = usage["completion_tokens"]
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state["model_name"] = model_name
        st.session_state["total_tokens"] = total_tokens
        st.session_state["cost"] = cost
        st.session_state["total_cost"] += cost
