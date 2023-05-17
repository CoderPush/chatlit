from firebase_admin import auth, credentials, initialize_app
from firestore_utils import decode_firestore_credentials
import streamlit as st

@st.cache_resource
def firebase_init():
    json_content = decode_firestore_credentials()
    cred = credentials.Certificate(json_content)
    initialize_app(cred)

def create_user_in_firebase_if_not_exists(user_info):
    try:
        # Try to get the user by email
        user = auth.get_user_by_email(user_info['email'])
        print('User already exists: ', user.uid)
    except auth.UserNotFoundError:
        # If user does not exist, create a new one
        user = auth.create_user(
            uid=user_info['id'],
            email=user_info['email'],
            email_verified=user_info['verified_email'],
            display_name=user_info['name'],
            photo_url=user_info['picture'],
        )
        print('User created: ', user.uid)

def list_users():
    auth.list_users().iterate_all()

def list_users_by_page():
    page = auth.list_users()
    while page:
        for user in page.users:
            print('User: ', user.uid)
        # Get next batch of users.
        page = page.get_next_page()