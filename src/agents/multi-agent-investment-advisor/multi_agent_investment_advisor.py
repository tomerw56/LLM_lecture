import re
from typing import Optional

import pandas as pd

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph_swarm import create_handoff_tool, create_swarm


# --------------------------------------------------------
# MODEL
# --------------------------------------------------------
model = ChatOllama(model="llama3.1")


stock_advisor_prompt = (
    "You are a stock investment advisor.\n\n"
    "INSTRUCTIONS:\n"
    "- Use the provided tools: fetch_stock_info"
    "- The input to these tools should be a stock symbol like 'AAPL' or 'GOOGL'.\n"
    "- When asked about a specific stock or company:\n"
    "  • Retrieve general information like its name, sector, and market cap.\n"
    "  • Analyze quarterly and annual financials (focus on Total Revenue and Net Income).\n"
    "  • Review price trends over the past year.\n"
    "- If the question is about **cats**  "
    "use the transfer tool to hand off to the cat advisor agent immediately.\n"
    "- Provide clear, objective, data-driven insights to support investment decisions.\n"
    "- Do NOT give disclaimers, speculation, or refer users to external sources.\n"
    "- Use ONLY the available tool outputs to form your response."
)

cat_advisor_prompt = (
    "You are the active cat agent.\n\n"
    "You have received a user query that is specifically about cats.\n"
    "Your job is to be supportive of cats.\n\n"
    "INSTRUCTIONS:\n"
    "- Use the provided tools: fetch_cat_info\n"
    "- When asked about a cats:\n"
    "  • say mewo 3 times.\n"
    "  • use fetch_cat_info.\n"
    "- If the question is about **stocks, ETFs, or traditional financial markets**, "
    "use the transfer tool to hand off to the stock advisor agent immediately.\n"
    "- Do NOT try to answer stock-related questions yourself.\n"
    "- Do NOT give disclaimers, opinions, or refer users elsewhere.\n"
    "- Base your entire response strictly on the data returned by the tools."
)
# --------------------------------------------------------
# HELPERS
# --------------------------------------------------------
def clean_text(text: str):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()



@tool
def fetch_cat_info():
    '''Return cat facts.'''
    print("Fetching cat info...")

    return {
        "only completely needy people do not like cats"
    }


@tool
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



# --------------------------------------------------------
# AGENTS
# --------------------------------------------------------
stock_advisor = create_agent(
    model=model,
    system_prompt=stock_advisor_prompt,
    tools=[
        fetch_stock_info,
        create_handoff_tool(
            agent_name="cat_advisor",
            description="Use this tool to transfer any queries about cats."
        )
    ],
    name="stock_advisor",
)

cat_advisor = create_agent(
    model=model,
    system_prompt=cat_advisor_prompt,
    tools=[
        fetch_cat_info,
        create_handoff_tool(
            agent_name="stock_advisor",
            description="Use this tool to transfer any queries about the stocks like Apple, Tesla, Microsoft, etc."

        )
    ],
    name="cat_advisor",
)

# --------------------------------------------------------
# SWARM WORKFLOW
# --------------------------------------------------------
workflow = create_swarm(
    agents=[stock_advisor, cat_advisor],
    default_active_agent="stock_advisor"
)

app = workflow.compile()


# --- Interactive loop ---
print("🔍 Enter your investment inquiry:")
print("Type a query, or 'exit' to quit.\n")

while True:
    query = input("You: ").strip()
    if query.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break
    if not query:
        continue

    result = app.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    research_result = clean_text(result["messages"][-1].content)
    print(f"\n🤖 Agent: {research_result}\n{'-'*60}\n")

