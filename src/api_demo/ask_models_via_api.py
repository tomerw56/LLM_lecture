import requests
from rich.console import Console
from rich.panel import Panel
import ollama
import lmstudio as lms

console = Console()
OLLAMA_MODEL="gemma3"
PROMPT = "How are you and who are you?"

def ask_lmstudio_api(prompt: str):
    """Send a chat prompt to LM Studio's OpenAI-compatible API."""
    url = "http://localhost:1234/v1/chat/completions"
    payload = {
        "model": "lmstudio",  # use "lmstudio" or your actual model ID
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Error contacting LM Studio] {e}"

def ask_lmstudio_client(prompt: str):
    """Send a chat prompt to LM Studio's OpenAI-compatible API."""
    with lms.Client() as client:
        model = client.llm.model("uncategorized")
        result = model.respond(prompt)
        return result.content

def ask_ollama_api(prompt: str):
    """Send a prompt to Ollama's API."""
    url = "http://localhost:11434/api/generate"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()["response"]
    except Exception as e:
        return f"[Error contacting Ollama] {e}"

def ask_ollama_client(prompt: str):
    """Query Ollama using its official Python client."""
    try:
        response = ollama.chat(model=OLLAMA_MODEL,
                               messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        return f"[Error contacting Ollama] {e}"


def main():
    console.rule("[bold cyan]LLM Demo: LM Studio vs Ollama[/bold cyan]")

    lmstudio_reply = ask_lmstudio_api(PROMPT)
    console.print(Panel(lmstudio_reply, title="LM Studio Response-API", style="green"))

    lmstudio_reply = ask_lmstudio_client(PROMPT)
    console.print(Panel(lmstudio_reply, title="LM Studio Response-CLIENT", style="green"))

    ollama_reply = ask_ollama_api(PROMPT)
    console.print(Panel(ollama_reply, title="Ollama Response-API", style="magenta"))

    ollama_reply = ask_ollama_client(PROMPT)
    console.print(Panel(ollama_reply, title="Ollama Response-CLIENT", style="yellow"))

if __name__ == "__main__":
    main()
