import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.title("ChatGPT Clone")

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Set default text model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user prompt
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )

        response = st.write_stream(stream)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
