import streamlit as st
import requests

st.title("Mini ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a polite, helpful assistant Keep answers brief."}
    ]

# Display past text messages on the screen
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Wait for Dad to type a question
if user_question := st.chat_input("Ask me anything!"):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("assistant"):
        try:
            # We pass the prompt clean as a simple web payload to avoid formatting crashes!
            url = f"https://pollinations.ai{requests.utils.quote(user_question)}"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                answer = response.text
                # If a messy website layout leaks through, clean it out
                if "<!DOCTYPE" in answer or "<html" in answer:
                    answer = "Hi! I connected to the server, but it sent back a messy website layout. Try typing your message one more time!"
            else:
                answer = f"The server is a bit busy (Code {response.status_code}). Please type your message again!"
        except Exception as e:
            answer = "Connection failed to process. Let's try sending the message again!"
            
        st.write(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
