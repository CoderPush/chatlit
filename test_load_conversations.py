from firestore_utils import firestore_save, get_firestore_db

db = get_firestore_db()

collection_ref = db.collection("conversations")

cid = "ZwpCs09yX28DdSlLjLLX"
conversation = collection_ref.document(cid).get().to_dict()
# display conversation
print(conversation['messages'])

# Usage: python test_load_conversations.py
# ❯ python test_load_conversations.py
# [{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': 'tell me a joke'}, {'role': 'assistant', 'content': 'Why did the tomato turn red?\nBecause it saw the salad dressing!'}]
