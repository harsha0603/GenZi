from fastapi import APIRouter, Request
from app.logger import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/webhook")
async def webhook_listener(request: Request):
    try:
        logger.info("Webhook endpoint called.")
        
        data = await request.json()
        logger.debug(f"Received data: {data}")
        
        message = data.get("Body") or data.get("message")
        sender = data.get("From")
        
        logger.info(f"Received message from {sender}: {message}")
        
        response_text = "Received your message. Processing..."
        logger.info("Sending response back to Twilio.")
        
        return {"response": response_text}
    
    except Exception as e:
        logger.error("Error processing webhook request", exc_info=True)
        return {"error": str(e)}

