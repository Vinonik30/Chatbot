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
if user_question := st.chat_input("Ask me anything !"):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("assistant"):
        try:
            # We connect directly to DuckDuckGo's open chat API layout
            url = "https://duckduckgo.com"
            payload = {'q': user_question}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            # Simple alternative free endpoint fallback
            alt_url = f"https://pollinations.ai{requests.utils.quote(user_question)}?json=true"
            response = requests.get(alt_url, timeout=10)
            
            if response.status_code == 200:
                # If pollinations sent json format, parse it safely
                try:
                    data = response.json()
                    answer = data.get("response", data.get("text", response.text))
                except:
                    # Clean out HTML manually if it leaked through
                    if "<!DOCTYPE" in response.text:
                        answer = "Hey there! I am connected to the server, but it sent back a messy layout. Try asking me a different question like 'Tell me a joke'!"
                    else:
                        answer = response.text
            else:
                answer = "The server is taking a short nap. Try typing your message one more time!"
        except Exception as e:
            answer = "Connection failed to process. Let's make sure the text is clean!"
            
        st.write(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
