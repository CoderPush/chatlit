import streamlit as st

def main():
    st.header("Ask a Question")

    if "last_query" not in st.session_state:
        st.session_state.last_query = ""

    with st.container():
        query = st.text_area("Ask a question here:", value=st.session_state.last_query, height=100, key="query_text")
        button = st.button("Submit", key="button")

        if button:
            print(query)

            # Clear the text_area after button click
            st.session_state.last_query = ""
        else:
            # Update the session state when the user types in the text area
            st.session_state.last_query = query

if __name__ == "__main__":
    main()