from utils import link_button


def render_conversations(st, sidebar):
    if "history_items" in st.session_state:
        for (m, title, cid) in st.session_state["history_items"]:
            link_button(sidebar, f"{m} {title}",
                        f"?cid={cid}")


def load_history_items(st, db):
    collection_ref = db.collection("conversations")
    result = []
    for c in collection_ref.stream():
        cid = c.id
        cdict = c.to_dict()
        if "title" in cdict:
            title = cdict["title"]
        else:
            title = cid
        if "model_name" in cdict:
            model_name = cdict["model_name"]
        else:
            model_name = "GPT-3.5"

        if model_name == "GPT-3.5":
            m = "③"
        elif model_name == "GPT-4":
            m = "④"
        else:
            m = "💬"

        result.append((m, title, cid))
    return result


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
        model_name = conversation.get("model_name", "GPT-3.5")
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
