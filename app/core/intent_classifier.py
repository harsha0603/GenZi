import joblib
import os

intent_model = joblib.load(r"intent_classification_model\intent_model.pkl")
tfidf_vectorizer = joblib.load(r"intent_classification_model\tfidf_vectorizer.pkl")

class ChatbotState:
    def __init__(self):
        self.last_intent = None

def classify_intent(message: str, state: ChatbotState) -> str:
    """
    Classify the intent of the message using a hybrid approach:
      1. Rule-based override for real estate-specific queries.
      2. Context-aware follow-up handling.
      3. Fall back to trained model (TF-IDF + Logistic Regression).
    
    Args:
        message: The user’s query.
        state: ChatbotState object to track conversation context.
    
    Returns:
        "general_query", "database_query", or "irrelevant"
    """
    message_lower = message.lower()
    real_estate_keywords = ["house", "rent", "price", "villa", "apartment", "residences", "heights", "park", "budget"]
    vague_phrases = ["more", "next", "what about", "tell me", "another"]

    if any(keyword in message_lower for keyword in real_estate_keywords):
        intent = "database_query"
    
    elif (state.last_intent == "database_query" and 
          any(phrase in message_lower for phrase in vague_phrases)):
        intent = "database_query"
    
    else:
        processed_message = tfidf_vectorizer.transform([message])
        intent = intent_model.predict(processed_message)[0]
    
    state.last_intent = intent
    return intent
