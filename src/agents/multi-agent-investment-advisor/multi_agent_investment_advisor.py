import re
from typing import Optional

import pandas as pd
import streamlit as st

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph_swarm import create_handoff_tool, create_swarm


# --------------------------------------------------------
# MODEL
# --------------------------------------------------------
model = ChatOllama(model="llama3.1", temperature=0.1)


# --------------------------------------------------------
# HELPERS
# --------------------------------------------------------
def clean_text(text: str):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()



    # --------------------------------------------------------
# TOOLS
# --------------------------------------------------------
@tool
@st.cache_data
def fetch_stock_info(symbol: str):
    """Fetch stock financial + price data using Yahoo Finance."""
    print("Fetching stock info...")

    annual={"Total Revenue":[100,23,55], "Net Income":[56,12,40]}

    return {
        "symbol": symbol,
        "annual_financials": annual,
        "min_price_last_year": 9,
        "max_price_last_year": 23,
        "average_price_last_year": 10.4,
        "current_price": 12.4,
    }


@tool
@st.cache_data
def fetch_coin_info(coin_id: str):
    """Fetch cryptocurrency info + 1-year prices using CoinGecko."""

    return {
        "coin": coin_id,
        "description": "great value for money",
        "market_cap_usd": 100,
        "market_cap_rank": 125,
        "min_price_last_year": 20,
        "max_price_last_year": 35,
        "average_price_last_year": 30,
        "current_price": 22.5,
    }


# --------------------------------------------------------
# AGENTS
# --------------------------------------------------------
stock_advisor = create_agent(
    model=model,
    tools=[
        fetch_stock_info,
        create_handoff_tool(
            agent_name="crypto_advisor",
            description="Transfer to crypto advisor for crypto questions."
        )
    ],
    name="stock_advisor",
)

crypto_advisor = create_agent(
    model=model,
    tools=[
        fetch_coin_info,
        create_handoff_tool(
            agent_name="stock_advisor",
            description="Transfer to stock advisor for equity questions."
        )
    ],
    name="crypto_advisor",
)

# --------------------------------------------------------
# SWARM WORKFLOW
# --------------------------------------------------------
workflow = create_swarm(
    agents=[stock_advisor, crypto_advisor],
    default_active_agent="stock_advisor"
)

app = workflow.compile()


# --------------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------------
query = st.text_input("Enter your investment inquiry:")

if query:
    result = app.invoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        },
        config={"configurable": {"thread_id": "1"}}
    )

    # Print debug to console
    for msg in result["messages"]:
        print(msg)

    clean_response = clean_text(result["messages"][-1].content)
    st.markdown(clean_response)

#test with how is the bitcoin doing?"
