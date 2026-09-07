import streamlit as st
import requests

st.title("Mini ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a polite, helpful assistant."}
    ]

# Display chat history on the screen
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
            # Send the text to a completely free, open AI server that needs no keys
            url = f"https://pollinations.ai{requests.utils.quote(user_question)}"
            response = requests.get(url, params={"system": "You are a polite, helpful assistant."})
            
            if response.status_code == 200:
                answer = response.text
            else:
                answer = "The server is a bit sleepy right now. Please try typing your message again!"
        except Exception:
            answer = "Connection failed. Please check your internet connection!"
            
        st.write(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
