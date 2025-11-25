from typing import Optional
import httpx
from typing import AsyncGenerator
import json
import requests

def joke_agent(answer_text: str) -> Optional[str]:
    prompt = f"""
    Turn the following answer into a silly joke.
    No need to be funny. Just output a 'joke version: ...'
    
    Answer:
    {answer_text}
    """
    url = "http://localhost:11434/api/generate"
    payload = {"model": "llama3.1", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        return response.json()['response']

    except Exception as e:
        return "error"
    return response
