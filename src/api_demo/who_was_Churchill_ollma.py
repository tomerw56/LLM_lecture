import argparse
import ollama
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
OLLAMA_MODEL = "gemma3"
console = Console()

def stream_ollama(model: str, temperature: float):
    prompt = "Who was Churchill? Please answer very briefly."

    console.rule(f"[bold cyan]Ollama Streaming Demo[/bold cyan]")
    console.print(f"[bold yellow]Model:[/bold yellow] {model}")
    console.print(f"[bold yellow]Temperature:[/bold yellow] {temperature}\n")
    console.print(f"[bold yellow]Prompt:[/bold yellow] {prompt}\n")

    stream = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        options={
            "temperature": temperature,
            "num_predict": 60,  # keep it short
        },
    )

    content = ""
    with Live(Markdown(content), console=console, refresh_per_second=10) as live:
        for chunk in stream:
            token = chunk.get("message", {}).get("content", "")
            content += token
            live.update(Markdown(content))

def main():
    parser = argparse.ArgumentParser(description="Ollama streaming demo with temperature control.")

    parser.add_argument("--temp", type=float, default=0.7, help="Temperature (default: 0.7)")
    args = parser.parse_args()

    try:
        stream_ollama(model=OLLAMA_MODEL, temperature=args.temp)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    main()
