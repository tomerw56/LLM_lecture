import re
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

def clean_text(text: str):
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned_text.strip()

# initialize Ollama model (must be running locally)
model = ChatOllama(model="llama3.1")  # or llama3, phi3, etc.

# Agent prompts
query_refiner_prompt = (
    "You are a query refiner agent.\n\n"
    "INSTRUCTIONS:\n"
    "- Refine the user's query to make it more specific and actionable\n"
    "- Respond ONLY with the refined query."
)
research_prompt = (
    "You are a research agent.\n\n"
    "INSTRUCTIONS:\n"
    "- Use your tools to gather up-to-date information from the web.\n"
    "- Respond ONLY with a concise summary of your findings."
)
supervisor_prompt = (
    "You are a supervisor agent.\n\n"
    "INSTRUCTIONS:\n"
    "- Manage the flow between the Query Refiner and Research Agent.\n"
    "- Use the Query Refiner to improve the user's query.\n"
    "- Then send the refined query to the Research Agent.\n"
    "- Return ONLY the final summarized answer."
)

# define agents
query_refiner_agent = create_agent(
    model=model,
    tools=[],
    system_prompt=query_refiner_prompt,
    name="query_refiner_agent"
)
research_agent = create_agent(
    model=model,
    tools=[DuckDuckGoSearchRun()],
    system_prompt=research_prompt,
    name="research_agent"
)
supervisor_agent = create_supervisor(
    model=model,
    agents=[query_refiner_agent, research_agent],
    prompt=supervisor_prompt
)

app = supervisor_agent.compile()

# --- Interactive loop ---
print("🔍 Multi-Agent Research Assistant")
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


#ask about taylor's method for function solving