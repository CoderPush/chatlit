import streamlit as st

# if 'disabled' not in st.session_state:
#     st.session_state.disabled = False
# if 'input' not in st.session_state:
#     st.session_state.input = ''


def disable():
    st.session_state.disabled = True
    st.session_state.input = st.session_state.text_area_stream
    st.session_state.text_area_stream = ""


def get_input():
    st.session_state.input = st.session_state.text_area_stream
    st.session_state.text_area_stream = ""


with st.container():
    # generate response stream here
    # user_input = st.text_area(
    #     f"You:", key="text_area_stream", label_visibility="collapsed", on_change=disable, disabled=st.session_state.disabled
    # )
    user_input = st.text_area(
        f"You:",
        key="text_area_stream",
        label_visibility="collapsed",
        on_change=get_input,
    )
    print("session:", st.session_state.text_area_stream)

if st.session_state.input:
    print("User pressed")
    print("saved variable:", st.session_state.input)
    print()
