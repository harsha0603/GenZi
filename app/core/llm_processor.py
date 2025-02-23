import os
import requests
from dotenv import load_dotenv

load_dotenv()

GPT4_API_URL = os.getenv("API_URL")
GPT4_API_KEY = os.getenv("API_KEY")

def generate_gpt4_response(prompt: str) -> str:
    """
    Sends a prompt to the GPT-4 chat completions API and returns the generated response text.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT4_API_KEY}",
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,     
        "temperature": 0.7,     
    }

    response = requests.post(GPT4_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        choices = result.get("choices", [])
        if choices:
            generated_text = choices[0].get("message", {}).get("content", "").strip()
            return generated_text if generated_text else "No response generated."
        else:
            return "No choices returned in response."
    else:
        return f"Error: {response.status_code} - {response.text}"
