import requests
from typing import List, Dict, Optional

BASE_URL = "http://localhost:11434"

def chat(messages: List[Dict[str, str]],
         model: str = "qwen2.5:3b",
         temperature: float = 0.0,
         max_tokens: Optional[int] = None,
         timeout: int = 60) -> str:
    """
    Send chat-style messages to Ollama and return the assistant reply.
    messages: list of {"role": "system|user|assistant", "content": "..."}
    """
    url = f"{BASE_URL}/api/chat"
    payload = {
    "model": model,
    "messages": messages,
    "stream": False,   # 👈 THIS IS CRITICAL
    "options": {
        "temperature": temperature
    }
}
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens

    resp = requests.post(url, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    # Return first assistant content
    return data["message"]["content"]