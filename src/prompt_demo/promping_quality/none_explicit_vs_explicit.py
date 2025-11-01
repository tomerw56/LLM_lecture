import ollama
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
OLLAMA_MODEL = "gemma3"
console = Console()

def ask_ollama(header:str,prompt:str,style:str):
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    reply=response["message"]["content"]
    formated_text=f"\n {prompt}:\n {reply}"
    console.print(Panel(formated_text, title=header, style=style))


# ❌ Bad prompt: vague and underspecified
bad_prompt = """
Write something about data. Make it short but detailed.
Maybe funny or not, up to you.
"""
ask_ollama(header="bad prompt",prompt=bad_prompt,style="red")


# ✅ Good prompt: explicit, structured, and context-rich
good_prompt = """
You are a data scientist writing a short LinkedIn post (under 100 words)
to explain to beginners what 'data cleaning' means.
Keep it clear, educational, and lightly humorous.
Structure:
- 1 sentence hook
- 2 bullet points explaining what it involves
- 1 short conclusion
"""
ask_ollama(header="good prompt",prompt=good_prompt,style="green")