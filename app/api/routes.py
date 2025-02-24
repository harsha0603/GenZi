from fastapi import APIRouter, Request
from app.logger import logging
from utils.twilio_helper import send_whatsapp_message
from app.core.llm_processor import generate_gpt4_response
from app.core.intent_classifier import classify_intent, ChatbotState

router = APIRouter()
chatbot_state = ChatbotState()

@router.post("/webhook")
async def webhook_listener(request: Request):
    try:
        logging.info("Webhook endpoint called.")
        data = await request.form()
        logging.debug(f"Received data: {data}")
        
        # Extract the user's message and sender number from the form data
        message = data.get("Body") or data.get("message")
        sender = data.get("From")
        logging.info(f"Received message from {sender}: {message}")
        
        # Classify intent using our hybrid approach with state tracking
        intent = classify_intent(message, chatbot_state)
        logging.info(f"Predicted intent: {intent}")
        
        # Build prompt and determine response based on intent
        if intent == "irrelevant":
            response_text = "I'm here to help with real estate-related queries. Could you please specify what you're looking for?"
        else:
            # For both general_query and database_query, we call GPT-4 to generate a response.
            # (For database_query, you might later combine DB results with the prompt.)
            prompt = message  # You can later enhance this prompt with additional context if needed.
            response_text = generate_gpt4_response(prompt)
        
        logging.info(f"GPT-4 generated response: {response_text}")
        
        # Send the generated response via Twilio
        twilio_sid = send_whatsapp_message(sender, response_text)
        logging.info(f"Sent message via Twilio. SID: {twilio_sid}")
        
        return {"response": response_text, "twilio_sid": twilio_sid}
    
    except Exception as e:
        logging.error("Error processing webhook request", exc_info=True)
        return {"error": str(e)}
