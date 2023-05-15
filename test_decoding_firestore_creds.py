import os
import base64
from dotenv import load_dotenv
load_dotenv()

# function to encode json to base64 string


def encode_firestore_credentials():
    # open json file
    with open('firestore-key.json') as f:
        data = f.read()
    # encode json to base64 string
    encoded = base64.b64encode(data.encode("utf-8"))
    print(encoded)


def decode_firestore_credentials():
    raw = os.environ['FIRESTORE_CREDENTIALS_BASE64']
    # decode base64 string to json
    firebase_credentials = base64.b64decode(raw).decode("utf-8")
    print(firebase_credentials)


if __name__ == "__main__":
    print("Test encoding:")
    encode_firestore_credentials()

    print("========================================")
    print("Test decoding from ENV variable:")
    decode_firestore_credentials()
