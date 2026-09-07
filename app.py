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
            # Connect directly through a stable public mirror using clean parameter tags
            url = "https://pollinations.ai"
            response = requests.get(
                url, 
                params={"prompt": user_question, "model": "openai"},
                timeout=15
            )
            
            if response.status_code == 200:
                answer = response.text
                # Clean up any rare raw code leaks automatically
                if "<!DOCTYPE" in answer:
                    answer = "I connected to the brain, but it's sending back messy server layout. Try asking me a different question like 'Tell me a joke'!"
            else:
                answer = "The server is a bit busy. Please try typing your message one more time!"
        except Exception:
            answer = "Connection failed to process. Let's try sending the message again!"
            
        st.write(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
