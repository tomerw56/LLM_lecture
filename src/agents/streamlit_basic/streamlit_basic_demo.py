import streamlit as st
import requests
import json

st.set_page_config(page_title="Ollama Chat", page_icon="💬", layout="wide")

st.sidebar.title("🧠 Ollama Agent")
model = st.sidebar.text_input("Model name", "gemma3")
api_url = "http://localhost:11434/api/chat"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("💬 Chat with Ollama")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User input ---
if prompt := st.chat_input("Ask something..."):
    print(f"prompt:{prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {"model": model, "messages": st.session_state.messages}
    response = requests.post(api_url, json=payload, stream=True)
    print(f"{response.text}\n")
    st.session_state.messages = []
    full_reply = ""
    with st.chat_message("assistant"):
        chat_placeholder = st.empty()

        for line in response.iter_lines():
            if not line:
                continue
            if line.startswith(b"data: "):
                line = line[len(b"data: "):]
            try:
                data = json.loads(line.decode("utf-8"))
                if "message" in data and "content" in data["message"]:
                    token = data["message"]["content"]
                    full_reply += token
                    chat_placeholder.markdown(full_reply)
                if data.get("done"):
                    break
            except json.JSONDecodeError:
                continue

    st.session_state.messages.append({"role": "assistant", "content": full_reply})
