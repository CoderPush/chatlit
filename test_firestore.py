# Usage: python test_firestore.py
from firestore_utils import firestore_save, get_firestore_db
from dotenv import load_dotenv
load_dotenv()

db = get_firestore_db()
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi, how can I help you?"},
    {"role": "user", "content": "I need help with my taxes."}
]
usage = {
    "model_name": "GPT-3.5",
    "total_tokens": 100,
    "prompt_tokens": 10,
    "completion_tokens": 90
}
cid = None
conversation = {
    "messages": messages,
    "usage": usage,
}
firestore_save(db, cid, conversation)
