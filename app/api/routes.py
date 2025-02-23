from fastapi import APIRouter, Request
import logging
from utils.twilio_helper import send_whatsapp_message
from app.logger import logging
router = APIRouter()

@router.post("/webhook")
async def webhook_listener(request: Request):
    try:
        logging.info("Webhook endpoint called.")
        data = await request.form()
        logging.debug(f"Received data: {data}")
        
        message = data.get("Body") or data.get("message")
        sender = data.get("From")
        
        logging.info(f"Received message from {sender}: {message}")
        
        # Process the message and generate a response (for now, a static response)
        response_text = "Received your message. Processing..."
        logging.info("Sending response back via Twilio.")
        
        # Use Twilio to send the response message
        twilio_sid = send_whatsapp_message(sender, response_text)
        logging.info(f"Sent message via Twilio. SID: {twilio_sid}")
        
        return {"response": response_text, "twilio_sid": twilio_sid}
    
    except Exception as e:
        logging.error("Error processing webhook request", exc_info=True)
        return {"error": str(e)}
