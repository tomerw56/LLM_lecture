import re
import streamlit as st
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver  # for fallback if needed
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent
import sqlite3

def clean_text(text: str):
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned_text.strip()

st.title("Agent with Persistent Memory (SQLite)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if "checkpointer" not in st.session_state:
    # Create (or open) SQLite for LangGraph checkpointing
    conn = sqlite3.connect("langgraph_memory.sqlite", check_same_thread=False)
    saver = SqliteSaver(conn)
    st.session_state.checkpointer = saver

model = ChatOllama(model="llama3.1")
chat_agent = create_react_agent(
    model=model,
    tools=[],
    name="chat_agent",
    checkpointer=st.session_state.checkpointer,
)

question = st.chat_input()

if question:
    st.session_state["messages"].append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    result = chat_agent.invoke(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        },
        config={"configurable": {"thread_id": "1"}}
    )

    response = clean_text(result["messages"][-1].content)

    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
