from firebase_utils import list_users_by_page, firebase_init
from dotenv import load_dotenv

load_dotenv()

firebase_init()

list_users_by_page()
