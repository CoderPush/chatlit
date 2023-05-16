from google.cloud import firestore
import os
import base64
import json
import streamlit as st

@st.cache_resource
def get_firestore_db():
    json_content = decode_firestore_credentials()
    db = firestore.Client.from_service_account_info(json_content)
    return db


def firestore_save(cid, conversation_record):
    db = get_firestore_db()
    if cid:
        # get conversation fromm cid
        conversation = db.collection("conversations").document(cid).get()
        # update conversation with the new messages and usage value
        conversation.reference.update(conversation_record)
    else:
        collection_ref = db.collection("conversations")
        collection_ref.add(conversation_record)


def decode_firestore_credentials():
    raw = os.environ['FIRESTORE_CREDENTIALS_BASE64']
    # decode base64 string to json
    firebase_credentials = base64.b64decode(raw).decode("utf-8")
    json_data = json.loads(firebase_credentials)
    return json_data
