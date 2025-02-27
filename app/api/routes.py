from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.logger import logging
from utils.twilio_helper import send_whatsapp_message
from app.core.llm_processor import generate_gpt4_response, extract_query_parameters
from app.core.intent_classifier import classify_intent, ChatbotState
from app.core.query_builder import build_property_query
from app.db.database import Property, Room, Washroom 
from app.db.connection import get_db  
 
router = APIRouter()
chatbot_state = ChatbotState()
 
@router.post("/webhook")
async def webhook_listener(request: Request, db: Session = Depends(get_db)):
    try:
        logging.info("Webhook endpoint called.")
        data = await request.form()
        logging.debug(f"Received data: {data}")
        
        message = data.get("Body") or data.get("message")
        sender = data.get("From")
        
        if not message or not sender:
            logging.warning("Missing required fields in request data.")
            return {"error": "Invalid request: Missing message or sender."}
        
        logging.info(f"Received message from {sender}: {message}")
        
        # Only two intents: general queries and database queries
        intent = classify_intent(message, chatbot_state)
        logging.info(f"Predicted intent: {intent}")
        
        response_text = ""
        if intent == "database_query":
            params = extract_query_parameters(message)
            logging.info(f"Extracted query parameters: {params}")
            
            properties = build_property_query(db, params)
            logging.info(f"Found {len(properties)} properties matching the query.")
            
            if properties:
                summary = "Here are some matching properties:\n"
                # Use attribute names as defined in your models (e.g., buildingname, propertytype, rent_price)
                for prop in properties[:3]:
                    summary += f"- {prop.buildingname} ({prop.propertytype}): Rent ₹{prop.rent_price}\n"
            else:
                summary = "No matching properties were found."
            
            prompt = f"{message}\n\nDatabase results:\n{summary}"
            response_text = generate_gpt4_response(prompt)
        else:
            response_text = generate_gpt4_response(message)
        
        logging.info(f"GPT-4 generated response: {response_text}")
        twilio_sid = send_whatsapp_message(sender, response_text)
        logging.info(f"Sent message via Twilio. SID: {twilio_sid}")
        
        return {"response": response_text, "twilio_sid": twilio_sid}
    
    except Exception as e:
        logging.error("Error processing webhook request", exc_info=True)
        return {"error": str(e)}
