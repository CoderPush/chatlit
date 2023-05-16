from google_utils import auth_with_google, update_authentication_status

def render_auth(st):
  auth_with_google(st)
  update_authentication_status(st)
