import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.title("ChatGPT Clone")

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini-tts"   # use a modern default model

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user prompt
if prompt := st.chat_input("What is up?"):
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Display user bubble
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.messages
            ],
            stream=True,
        )

        response = st.write_stream(stream)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
