import streamlit as st
import requests
from huggingface_hub import InferenceClient

st.title("mini ChatBot")

# --- AUTO-LOAD THE KEY SAFELY ---
@st.cache_resource
def get_client():
    try:
        # Pulls your token securely from Streamlit's secrets box
        token = st.secrets["HF_TOKEN"]
        return InferenceClient(model="microsoft/Phi-3-mini-4k-instruct", token=token)
    except Exception:
        return None

client = get_client()
# ---------------------------------

if client:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a polite, helpful assistant Keep answers brief."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    if user_question := st.chat_input("Ask me anything, Dad!"):
        with st.chat_message("user"):
            st.write(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.chat_message("assistant"):
            try:
                response = client.chat_completion(
                    messages=st.session_state.messages,
                    max_tokens=500
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = "Error connecting: Could not reach the model brain. Let's fix your secret key format!"
                
            st.write(answer)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.warning("⚠️ Setup needed: Let's fix your token name format!")
    st.code('HF_TOKEN = "hf_your_actual_key_here"', language="toml")
