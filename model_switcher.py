# define render_model_switcher function to be called in chat.py
#
def render_model_switcher(st, element):
    if "generated" in st.session_state and len(st.session_state["generated"]) > 0:
        lock_model = True
    else:
        lock_model = False

    model_index = 0 if st.session_state['model_name'] == "GPT-3.5" else 1
    model_name = element.radio("Choose a model:", ("GPT-3.5",
                                                   "GPT-4"), model_index, disabled=lock_model)
    return model_name
