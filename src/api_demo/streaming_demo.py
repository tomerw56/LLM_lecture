import ollama
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
console = Console()
OLLAMA_MODEL = "gemma3"
MARK_CHUNKS=False
PROMPT = "Tell me a short story about an adventurous cat who becomes a spaceship pilot."

def stream_ollama(prompt: str, model: str = OLLAMA_MODEL):
    """Stream tokens from Ollama as they arrive."""
    stream = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    content = ""
    with Live(Markdown(content), console=console, refresh_per_second=10) as live:
        counter=0
        for chunk in stream:
            # Each chunk is a dictionary with message data
            token = chunk.get("message", {}).get("content", "")
            if MARK_CHUNKS:
                token=f"<{counter}> {token} <{counter}>"
            counter+=1
            content += token

            live.update(Markdown(content))
        live.update(Markdown(content))  # final update

def main():
    console.rule("[bold cyan]Ollama Streaming Demo[/bold cyan]")
    console.print(f"[bold yellow]Prompt:[/bold yellow] {PROMPT}\n")

    try:
        stream_ollama(PROMPT)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    main()
