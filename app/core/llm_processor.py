import os
import requests
from dotenv import load_dotenv

load_dotenv()

GPT4_API_URL = os.getenv("API_URL")
GPT4_API_KEY = os.getenv("API_KEY")

def generate_gpt4_response(prompt: str) -> str:
    """
    Sends a prompt to the GPT-4 chat completions API and returns the generated response text,
    conditioning the response as a knowledgeable real estate chatbot agent.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT4_API_KEY}",
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "You are a friendly and knowledgeable real estate chatbot agent specializing in Singapore properties. Answer queries with clarity and in a professional tone, using real estate terminology where appropriate."
            },
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
