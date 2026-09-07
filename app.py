import streamlit as st
from huggingface_hub import InferenceClient

st.title("Mini ChatBot")

# --- FETCH HIDDEN KEY FROM STREAMLIT VAULT ---
try:
    api_key = st.secrets["HF_TOKEN"]
except Exception:
    api_key = None
# ---------------------------------------------

if api_key:
    client = InferenceClient(
        model="Qwen/Qwen2.5-72B-Instruct",
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
                answer = response.choices.message.content
            except Exception as e:
                answer = "Error connecting: Could not reach the model brain. Make sure your key is saved in Streamlit Secrets!"
                
            st.write(answer)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.warning("⚠️ Configuration Error: Please add your 'HF_TOKEN' to your Streamlit App Secrets Vault!")
