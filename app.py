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
            # We use params={} instead of mash-ups so spaces are treated perfectly by the server!
            url = "https://text.pollinations.ai/"
            response = requests.get(
                f"{url}{requests.utils.quote(user_question)}", 
                timeout=10
            )
            
            if response.status_code == 200:
                answer = response.text
            else:
                answer = "The server is a bit busy right now. Please type your message one more time!"
        except Exception as e:
            answer = f"Connection failed to process. Let's make sure the text is clean!"
            
        st.write(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
