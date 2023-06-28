import streamlit as st
from google_utils import decode_token_from_params
from debugger import debugger

def upload_image():
    uploaded_files = st.file_uploader("Choose a JPG/PNG file", type=['png','jpg'], accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()

def create_bot_form():
    with st.form("create_a_bot_form"):
        # Upload Image
        upload_image()
        # Bot Name
        st.text_input('Name')
        # Bot Description
        st.text_input('Description')
        # Model Name
        st.selectbox(
            "GPT model",
            ("GPT-4", "GPT-3.5")
        )
        # Prompt
        st.text_input('Prompt')

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Submitted")

def controller():
    create_bot_form()
    

def main():
    st.set_page_config(
        page_title="PushGPT Create Bot", page_icon=":robot_face:", layout="wide"
    )
    st.header("🤖 Create a Bot")
    controller()
    


if __name__ == "__main__":
    main()
    debugger()
