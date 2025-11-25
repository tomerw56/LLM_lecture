from acp_sdk.server import Server, Context, RunYield
from agents.answer_agent import answer_agent
from agents.joke_agent import joke_agent


app = Server()

@app.agent()
async def pipeline(ctx: Context):
    question = ctx[0]
    print(f"got ::: {question}")
    # --- Step 1: Answer
    answer_text = answer_agent(question)
    print(f"got from answer_agent::: {answer_text}")

    # --- Step 2: Joke about the answer
    joke = joke_agent(answer_text)
    print(f"got from joke_agent::: {joke}")
    yield joke

if __name__ == "__main__":
    app.run(port=8000)

#run server from venv and than test client
