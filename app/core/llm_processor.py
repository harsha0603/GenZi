import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GPT4_API_URL = os.getenv("API_URL")
GPT4_API_KEY = os.getenv("API_KEY")

def generate_gpt4_response(prompt: str) -> str:
    """
    Sends a prompt to GPT-4 and returns a free-text response.
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
                "content": "You are a friendly and knowledgeable real estate chatbot agent specializing in Singapore properties."
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
            return choices[0].get("message", {}).get("content", "").strip()
        else:
            return "No choices returned in response."
    else:
        return f"Error: {response.status_code} - {response.text}"

def extract_query_parameters(query: str) -> dict:
    """
    Extracts structured query parameters from a natural language input.
    The output JSON should have keys: property_type, min_rent, max_rent, building_name, and address.
    If a detail isn't provided, its value should be null.
    """
    prompt = (
        "Extract the following details from the user query in JSON format with these keys: "
        "property_type (e.g., apartment, villa, condo, etc.), "
        "min_rent, max_rent, building_name, and address. "
        "If a detail is not provided, set its value to null. "
        f"User query: \"{query}\""
    )
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT4_API_KEY}",
    }
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You extract structured query parameters for a real estate database."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,
        "temperature": 0.0,
    }
    
    response = requests.post(GPT4_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        try:
            json_str = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            params = json.loads(json_str)
            return params
        except json.JSONDecodeError:
            return {}
    else:
        return {"error": f"API error {response.status_code}: {response.text}"}
