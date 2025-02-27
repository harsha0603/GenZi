import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GPT4_API_URL = os.getenv("API_URL")
GPT4_API_KEY = os.getenv("API_KEY")

class ChatbotState:
    def __init__(self):
        self.last_intent = None

def classify_intent(message: str, state: ChatbotState) -> str:
    """
    Uses LLM to classify intent as "general_query" or "database_query".
    Handles vague follow-ups and ambiguous inputs intelligently.
    """
    prompt = (
        "You are an intelligent and friendly real estate chatbot specializing in Singapore properties. "
        "Your job is to classify user queries into two categories: \n"
        "1. 'database_query': If the user is asking about properties, rent, location, price, etc. \n"
        "2. 'general_query': If the user is making a greeting, asking about your capabilities, or other non-database-related topics. \n"
        "If the query is unclear, ask a clarifying question. \n"
        "If the user mixes a greeting with a database query, classify it as 'database_query' but also greet them. \n"
        "If the user follows up vaguely after a 'database_query', default to 'database_query'. \n"
        f"User message: \"{message}\""
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT4_API_KEY}",
    }
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a smart real estate chatbot for Singapore."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 50,
        "temperature": 0.2,
    }
    
    response = requests.post(GPT4_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        intent = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip().lower()
        if intent not in ["database_query", "general_query"]:
            return "ambiguous_input"
        state.last_intent = intent
        return intent
    else:
        return "error"
