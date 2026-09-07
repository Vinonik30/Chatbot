import streamlit as st
from huggingface_hub import InferenceClient

st.title("Mini AI Chat Bot")

# --- YOUR KEY GOES HERE ---
# Paste your real hf_... key inside the quotation marks below!
api_key = "hf_YOUR_ACTUAL_KEY_HERE"
# --------------------------

if api_key and api_key != "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":
    # Set up a direct connection to a super smart free model
    client = InferenceClient(
        model="Qwen/Qwen2.5-72B-Instruct",
        token=api_key
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a polite, helpful assistant. Keep answers brief."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    if user_question := st.chat_input("Ask me anything!"):
        with st.chat_message("user"):
            st.write(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.chat_message("assistant"):
            try:
                # Direct message call to the brain
                response = client.chat_completion(
                    messages=st.session_state.messages,
                    max_tokens=500
                )
                answer = response.choices.message.content
            except Exception as e:
                answer = "Error connecting: Could not reach the model brain. Make sure your key is correct!"
                
            st.write(answer)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.warning("⚠️ Configuration Error: Please open app.py in Notepad and replace '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' with your real Hugging Face key!")
