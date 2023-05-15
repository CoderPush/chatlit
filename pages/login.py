import streamlit as st
import streamlit_authenticator as stauth
from authenticator import authenticator

name, authentication_status, username = authenticator.login('Login', 'sidebar')
st.session_state["authentication_status"] = authentication_status
st.session_state["name"] = name
st.session_state["username"] = username

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
