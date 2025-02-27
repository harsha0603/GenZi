import os
import requests
import json
import re
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
            {"role": "system", "content": "You are a real estate chatbot specializing in Singapore properties."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 250,
        "temperature": 0.0,
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
    Extracts structured query parameters from user input, handling comparative words (greater, lesser, nearby, etc.).
    """
    
    prompt = (
        "Extract structured parameters from the user query in JSON format with:\n"
        "- property_type (e.g., apartment, villa, condo, etc.)\n"
        "- min_rent, max_rent (integers)\n"
        "- building_name, address\n"
        "- furnishing (furnished, semi-furnished, unfurnished)\n"
        "- amenities (list of requested amenities such as pool, gym, parking, etc.)\n"
        "- num_bedrooms (integer)\n"
        "- num_bathrooms (integer)\n"
        "- location_preference (values: 'exact', 'nearby', 'within [X] km')\n"
        "- price_filter_type (values: 'greater_than', 'less_than', 'range', 'exact')\n\n"
        "Ensure that comparative words (greater than, below, nearby, within) are captured correctly.\n\n"
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
        "max_tokens": 250,
        "temperature": 0.0,
    }
    
    response = requests.post(GPT4_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        try:
            json_str = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            params = json.loads(json_str)
            
            # Detect missing details for follow-up
            missing_details = []
            if not params.get("property_type"):
                missing_details.append("property type (e.g., condo, apartment, villa)")
            if not params.get("min_rent") and not params.get("max_rent"):
                missing_details.append("budget range (minimum and maximum rent)")
            if not params.get("num_bedrooms"):
                missing_details.append("number of bedrooms")
            if not params.get("num_bathrooms"):
                missing_details.append("number of bathrooms")
            
            # Generate follow-up question if any key detail is missing
            if missing_details:
                follow_up_question = f"Could you please specify the {', '.join(missing_details)}?"
                params["follow_up_question"] = follow_up_question
            
            return params
        
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON from LLM response."}
    
    else:
        return {"error": f"API error {response.status_code}: {response.text}"}

