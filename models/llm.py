import os
import requests
from config.config import GROQ_API_KEY, LLM_MODEL

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_llm(prompt: str, model: str = LLM_MODEL, mode: str = "concise") -> str:
    """
    Generate a response using Groq API with the given prompt.
    Mode can be 'concise' or 'detailed'.
    """
    system_prompt = "You are a helpful and knowledgeable museum guide."

    if mode == "concise":
        system_prompt += " Respond concisely and clearly."
    elif mode == "detailed":
        system_prompt += " Provide detailed historical and artistic context."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with LLM API: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"