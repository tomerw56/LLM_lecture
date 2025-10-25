import requests

def list_lmstudio_models():
    try:
        r = requests.get("http://localhost:1234/v1/models", timeout=2)
        data = r.json()
        models = [m["id"] for m in data.get("data", [])]
        print("LM Studio models:", models)
    except Exception as e:
        print("LM Studio not reachable:", e)

def list_ollama_models():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        data = r.json()
        models = [m["name"] for m in data.get("models", [])]
        print("Ollama models:", models)
    except Exception as e:
        print("Ollama not reachable:", e)

list_lmstudio_models()
list_ollama_models()
