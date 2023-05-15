from google_utils import auth_with_google

# define authenticator_setup function to be called in chat.py


def authenticator_setup(st):
    auth_with_google(st)

    if st.session_state.get("authentication_status"):
        logout = st.sidebar.button(f'Logout *{st.session_state["name"]}*')
        if logout:
            # clear st.session_state
            st.session_state.clear()

    # stop if not authenticated
    if not st.session_state.get("authentication_status"):
        st.stop()
