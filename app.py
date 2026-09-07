import streamlit as st
import subprocess
import os

st.title("Mini ChatBot")

# --- INITIALIZE A COMPLETELY FREE LOCAL BRAIN ---
@st.cache_resource
def launch_local_brain():
    # If the local AI system isn't running yet, turn it on in the background!
    try:
        # Download and run a super fast, completely free AI brain
        subprocess.Popen(["curl", "-fsSL", "https://ollama.com", "|", "sh"], shell=True)
        subprocess.Popen(["ollama", "run", "tinyllama"])
        return True
    except Exception:
        return False

brain_ready = launch_local_brain()
# ------------------------------------------------

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
            import ollama
            # Directly talk to your app's personal built-in brain!
            response = ollama.chat(
                model='tinyllama',
                messages=st.session_state.messages
            )
            answer = response['message']['content']
        except Exception as e:
            # If the background engine is still booting up on the first try, show a helpful hint
            answer = "I am waking up my built-in engine right now! Please type your message one more time in 10 seconds."
            
        st.write(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
