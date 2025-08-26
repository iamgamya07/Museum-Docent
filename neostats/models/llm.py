import os
import requests
import json
from config.config import GROQ_API_KEY

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- UPDATED MODEL NAME ---
# Using a current and recommended model from Groq
DEFAULT_MODEL = "llama3-8b-8192"

def generate_llm(prompt: str, model: str = DEFAULT_MODEL, mode: str = "concise") -> str:
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
        
        # --- IMPROVED ERROR HANDLING ---
        # This will give a more detailed error message if something goes wrong
        response.raise_for_status() 
        
        result = response.json()
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as http_err:
        # Try to parse the error message from the API response
        try:
            error_details = response.json()
            return f"Error from LLM: {http_err} - Details: {error_details}"
        except json.JSONDecodeError:
            return f"Error from LLM: {http_err} - Could not parse error response."
            
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"