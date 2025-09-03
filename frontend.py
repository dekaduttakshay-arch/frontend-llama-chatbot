import streamlit as st
import requests

# --- Streamlit page config ---
st.set_page_config(
    page_title="Chatbot",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("💬 CRM Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat Input ---
user_input = st.chat_input("Type your question...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Send request to backend
        response = requests.post(
            "http://localhost:8080/query/",
            data={"question": user_input}
        )
        response.raise_for_status()

        # ✅ Get only the answer string
        answer = response.json()["answer"]

    except Exception as e:
        answer = f"⚠️ Error: {e}"

    # Add bot reply
    st.session_state.messages.append({"role": "bot", "content": answer})

# --- Display Chat Messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
