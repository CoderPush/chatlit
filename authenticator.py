from google_utils import auth_with_google, update_authentication_status

def authenticator_setup(st):
    auth_with_google(st)

    if st.session_state.get("authentication_status"):
        logout = st.sidebar.button(f'Logout *{st.session_state["name"]}*')
        if logout:
        # clear st.session_state
            st.session_state.clear()

    update_authentication_status(st)

    # only stop rendering if authentication_status is explicitly set to False
    if st.session_state.get("authentication_status") == False:
        st.stop()
