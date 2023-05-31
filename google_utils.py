import requests
import os
from streamlit_oauth import OAuth2Component
from firebase_utils import create_user_in_firebase_if_not_exists
from utils import get_key_from_params
import base64
import json
import time

from dotenv import load_dotenv

load_dotenv()


# Set environment variables
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"
SCOPE = "openid profile email"

CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

WHITELISTED_DOMAINS = os.getenv("WHITELISTED_DOMAINS", "coderpush.com")
WHITELISTED_DOMAINS_SET = set(WHITELISTED_DOMAINS.split(","))


def is_whitelisted_email_domain(email):
    return email.split("@")[1] in WHITELISTED_DOMAINS_SET


# convert json to base64 string
# INPUT:
# {
# "access_token": "",
# "expires_in": 3599,
# "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email openid",
# "token_type": "Bearer",
# "id_token": "",
# "expires_at": 1684836588
# }
# OUTPUT:
# eyJhY2Nlc3NfdG9rZW4iOiIiLCJleHBpcmVzX2luIjozNTk5LCJzY29wZSI6Imh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgvdXNlcm5hbWUucHJvZmlsZSBodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9hdXRoL3VzZXJpbmZvLmVtYWlsIG9wZW5pZCB0eXBlIjoiQmVhcmVyIiwiaWRfdG9rZW4iOiIiLCJleHBpcmVzX2F0IjoxNjg0ODM2NTg4fQ==
def dict_to_base64(token):
    json_data = json.dumps(token)
    encoded = base64.b64encode(json_data.encode("utf-8"))
    return encoded


def auth_with_google(st):
    # Create OAuth2Component instance
    oauth2 = OAuth2Component(
        CLIENT_ID,
        CLIENT_SECRET,
        AUTHORIZE_URL,
        TOKEN_URL,
        REFRESH_TOKEN_URL,
        REVOKE_TOKEN_URL,
    )

    sign_in_holder = st.empty()
    # Check if token exists in session state
    if "token" not in st.session_state:
        with sign_in_holder.container():
            # If not, show authorize button
            result = oauth2.authorize_button("Sign in with Google", REDIRECT_URI, SCOPE)
        if result and "token" in result:
            # If authorization successful, save token in session state
            token = result["token"]
            st.session_state["token"] = token
            base64_token = dict_to_base64(token)
            st.experimental_set_query_params(token=base64_token)
            sign_in_holder.empty()
    else:
        token = st.session_state["token"]
        expires_at = token.get("expires_at")
        if expires_at and expires_at < time.time():
            try:
                token = oauth2.refresh_token(token)
                st.session_state.token = token
                print.log("Refreshed token at ", expires_at)
                st.session_state.token = token
                st.experimental_rerun()
            except Exception as e:
                st.experimental_set_query_params()
                st.error(e)


def update_authentication_status(st):
    # get access_token from st.session_state["token"]["access_token"] with error handling
    try:
        access_token = st.session_state["token"]["access_token"]
        if access_token:
            user_info = get_user_info(access_token)

        if user_info and is_whitelisted_email_domain(user_info["email"]):
            create_user_in_firebase_if_not_exists(user_info)
            st.session_state["authentication_status"] = "Authenticated"
            st.session_state["name"] = user_info["name"]
            st.session_state["user_info"] = user_info

        else:
            st.experimental_set_query_params()

            message = "Failed to get user info. <a href='/' target='_self'>Reload?</a>"

            if not is_whitelisted_email_domain(user_info["email"]):
                message = "This site is limited to whitelisted domains. <a href='/' target='_self'>Reload?</a>"

            st.markdown(
                message,
                unsafe_allow_html=True,
            )
            del st.session_state["token"]
            st.session_state["authentication_status"] = "Not Authenticated"
    except KeyError:
        st.session_state["authentication_status"] = "Token Missing"


def get_user_info(access_token):
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        return None


# log out google using access_token
def sign_out_google(st, login_placeholder):
    access_token = st.session_state.get("token", {}).get("access_token")

    if not access_token:
        st.error("Error with access token")
        return

    response = requests.post(
        REVOKE_TOKEN_URL,
        params={"token": access_token},
    )

    if response.status_code == 200:
        login_placeholder.empty()
        st.sidebar.markdown(
            "Successfully logged out. <a href='/' target='_self'>Reload?</a>",
            unsafe_allow_html=True,
        )
    else:
        st.error("Failed to log out")
        print("Failed to log out:")
        print(response)


def decode_token_from_params(st, key):
    try:
        base64_token = get_key_from_params(st, key)
        if base64_token:
            # decode token
            str_data = base64.b64decode(base64_token.encode("utf-8")).decode("utf-8")
            # convert to dict
            dict_data = json.loads(str_data)
            return dict_data
    except UnicodeDecodeError as e:
        st.error(e)
