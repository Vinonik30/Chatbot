import streamlit as st
from huggingface_hub import InferenceClient

st.title("Mini ChatBot")

# Grab your key safely from the Streamlit vault
try:
    api_key = st.secrets["HF_TOKEN"]
except Exception:
    api_key = None

if api_key:
    # We connect directly to a completely open model that needs no license approval
    client = InferenceClient(
        model="Qwen/Qwen2.5-1.5B-Instruct",
        token=api_key
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a polite, helpful assistant Keep answers brief."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    if user_question := st.chat_input("Ask me anything! Required key is active."):
        with st.chat_message("user"):
            st.write(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.chat_message("assistant"):
            try:
                response = client.chat_completion(
                    messages=st.session_state.messages,
                    max_tokens=500
                )
                answer = response.choices.message.content
            except Exception as e:
                answer = "Error connecting: Please make sure your token in Streamlit secrets is a fresh Legacy Read key!"
                
            st.write(answer)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.warning("⚠️ Configuration Error: Please add your 'HF_TOKEN' to your Streamlit App Secrets Vault!")
