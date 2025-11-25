
import requests


def answer_agent(question: str) -> str:
    prompt = f"Answer briefly:\n{question}"
    url = "http://localhost:11434/api/generate"
    payload = {"model": "llama3.1", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        return response.json()['response']


    except Exception as e:
        return "error"
    return "No answer"
