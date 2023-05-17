# Usage: python test_firestore.py
from firestore_utils import firestore_save
from dotenv import load_dotenv

load_dotenv()

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi, how can I help you?"},
    {"role": "user", "content": "I need help with my taxes."},
]
usage = {
    "model_name": "GPT-3.5",
    "total_tokens": 100,
    "prompt_tokens": 10,
    "completion_tokens": 90,
}
cid = "2ICFsbi1rR6iWEM3wjZ8"
conversation = {
    "messages": messages,
    "usage": usage,
}

result = firestore_save(cid, conversation)
