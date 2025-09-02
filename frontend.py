import streamlit as st
import requests

# Streamlit page config for fullscreen look
st.set_page_config(page_title="Chatbot", layout="wide")

st.title("💬 Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Input box for user query
if prompt := st.chat_input("Type your message..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the API
    try:
        response = requests.post(
            "https://llama-chatbot-mnko.onrender.com/query/",
            json={"query": prompt},
            timeout=60
        )

        if response.status_code == 200:
            bot_reply = response.json().get("response", "⚠️ No response field found.")
        else:
            bot_reply = f"⚠️ Error {response.status_code}: {response.text}"

    except Exception as e:
        bot_reply = f"⚠️ API call failed: {str(e)}"

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
