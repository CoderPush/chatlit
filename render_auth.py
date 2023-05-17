from google_utils import auth_with_google, update_authentication_status
from firebase_utils import firebase_init


def render_auth(st):
    firebase_init()
    auth_with_google(st)
    update_authentication_status(st)
