import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

# define authenticator_setup function to be called in chat.py


def authenticator_setup(st):
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name, authentication_status, username = authenticator.login(
        'Login', 'sidebar')
    st.session_state["authentication_status"] = authentication_status
    st.session_state["name"] = name
    st.session_state["username"] = username

    if st.session_state["authentication_status"]:
        authenticator.logout(f'Logout *{st.session_state["name"]}*', 'sidebar')

    return authenticator
