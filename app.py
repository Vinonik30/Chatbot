import streamlit as st
import requests

st.title("🤖 Dad's Personal Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a polite, helpful assistant built for my dad. Keep answers brief."}
    ]

# Display past text messages on the screen
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Wait for Dad to type a question
if user_question := st.chat_input("Ask me anything, Dad!"):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("assistant"):
        try:
            # Connect directly to a completely open public AI pipeline that requires no keys!
            url = f"https://pollinations.ai{requests.utils.quote(user_question)}?json=true"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                # Safely extract the raw AI response text block
                answer = data.get("response", data.get("text", "Hello! I am ready to help."))
            else:
                answer = "The server is a bit busy right now. Please type your message one more time!"
        except Exception as e:
            answer = "Connection failed to process. Let's try sending the message again!"
            
        st.write(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
