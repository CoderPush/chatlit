import requests
import os
from streamlit_oauth import OAuth2Component


# Set environment variables
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"
SCOPE = "openid profile email"

CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')


def auth_with_google(st):
    # Create OAuth2Component instance
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL,
                             TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

    # Check if token exists in session state
    if 'token' not in st.session_state:
        # If not, show authorize button
        result = oauth2.authorize_button(
            "Sign in with Google", REDIRECT_URI, SCOPE)
        if result and 'token' in result:
            # If authorization successful, save token in session state
            st.session_state['token'] = result.get('token')
            st.experimental_rerun()
    else:
        # If token exists in session state, show the token
        token = st.session_state['token']

        if st.sidebar.button("Refresh Token"):
            # If refresh token button is clicked, refresh the token
            token = oauth2.refresh_token(token)
            st.session_state.token = token
            st.experimental_rerun()

        access_token = token.get('access_token')
        if access_token:
            user_info = get_user_info(access_token)

        if user_info:
            st.session_state["authentication_status"] = True
            st.session_state["name"] = user_info["name"]
            st.session_state["user_info"] = user_info
        else:
            st.error("Failed to get user info.")


def get_user_info(access_token):
    response = requests.get(
        'https://www.googleapis.com/oauth2/v1/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        return None
