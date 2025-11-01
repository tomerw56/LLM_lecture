import pprint

import requests
from sqlalchemy import create_engine, text
import ast
import ollama
from connection import connection_str
import logging

import sys

OLLAMA_MODEL = "gemma3"

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def handle_model_output(output: str):
    try:
        tree = ast.parse(output.strip(), mode='exec')
        call = tree.body[0].value
        func_name = call.func.id
        kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}

        if func_name == "plot_sales_over_time":
            plot_sales_over_time(**kwargs)
        elif func_name == "run_sql_query":
            run_sql_query(**kwargs)
        else:
            print(f"❌ Unknown function: {func_name}")
    except Exception as e:
        print("❌ Error parsing model output:", e)


def plot_sales_over_time(start_date, end_date, group_by):
    print("📊 Plotting sales chart:")
    print(f"  Start: {start_date}, End: {end_date}, Grouped by: {group_by}")
    print("📈 (Pretend we just showed a nice plot...)")


def run_sql_query(query: str):
    # Config
    engine = create_engine(connection_str)
    with engine.connect() as conn:
        query_result = conn.execute(text(query))
        logging.info(pprint.pformat([dict(row._mapping) for row in query_result]))


# Load schema from file
with open("schema.sql", "r") as f:
    schema = f.read()

# Natural language query about the schema
user_queries = [
    "What was ordered from 'NY'",
    "Which clients placed orders in the last 12 days?",
    "Which client ordered the most products and their number of orders?",
    "Which was the last order placed?",
    "When was the product 'manager' ordered?",
    "Show me product sales by month for this year"]

# SEE alias use
for user_query in user_queries:
    logging.info(f'User query:{user_query}')
    # Build the prompt
    prompt = f"""You are a data assistant that can call tools to answer questions.
        
            Alias Definitions:
    - "NY" refers to the location "new york"
    - "CH" refers to the location "Choishire"
    
       Schema:
       {schema}


       You have access to the following tools:

       1. `run_sql_query(query: str)`
          - Executes the provided SQL query and returns the result.

       2. `plot_sales_over_time(start_date: str, end_date: str, group_by: str)`
          - Plots total product sales between two dates.
          - `group_by` can be "day", "week", or "month".

       Instructions:
       - When asked to execute a query, respond ONLY with a function call to `run_sql_query(...)`.
       - When asked to visualize product sales over time, respond ONLY with a call to `plot_sales_over_time(...)`.
       - Do not explain, only return the function call.

       Examples:

       User: Show product sales by month for this year  
       → `plot_sales_over_time(start_date="2025-01-01", end_date="2025-12-31", group_by="month")`

       User: Give me a list of clients from New York  
       → `run_sql_query(query = "SELECT * FROM clients WHERE location = 'New York';")`

       Now here is the actual user request:
       ---
       User: {user_query}
       """

    logging.debug(f'Prompt:{prompt}')

    # Make the request to local Ollama
    url = "http://localhost:11434/api/generate"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logging.debug(f'Response: {response.json()}')

    except Exception as e:
        logging.error(e)
        exit

    # Print the generated SQL
    if response.ok:
        result = response.json()
        output = result["response"]
        output = output.replace("\n", " ").replace("quert_text", "").replace("```", "").replace("`", "").replace(
            "tool_code", "")
        logging.info(f'Generated RESPONSE:{output}')
        handle_model_output(output=output)
    else:
        logging.error(f'Error:{response.status_code}, {response.text}')
