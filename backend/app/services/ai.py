import httpx
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = "mistral:7b-instruct"

SYSTEM_PROMPT = """You are an English speaking practice assistant. For each user message:
1. If there are grammar errors, briefly note the correction.
2. Suggest one synonym for a key word if appropriate.
3. Then give a natural, conversational reply to continue the dialogue.
Keep your response concise (2-4 sentences)."""


def _build_messages(text: str, history: list[dict]) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": text})
    return messages


def process_text(text: str, history: list[dict]) -> str:
    messages = _build_messages(text, history)
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={"model": MODEL_NAME, "messages": messages, "stream": False},
        timeout=120.0,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]