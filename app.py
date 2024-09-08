import streamlit as st
from openai import OpenAI
from coderag.config import OPENAI_API_KEY, OPENAI_CHAT_MODEL
from prompt_flow import execute_prompt_flow

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

st.title("Code RAG with OpenAI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about the codebase"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = execute_prompt_flow(prompt, project_path=".")  # Specify your project path here
            message_placeholder.markdown(response)
            full_response = response
        except Exception as e:
            error_message = f"Error with chat completion: {str(e)}"
            st.error(error_message)
            full_response = error_message

    st.session_state.messages.append({"role": "assistant", "content": full_response})