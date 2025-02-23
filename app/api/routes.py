from fastapi import APIRouter, Request
from app.logger import logging
from utils.twilio_helper import send_whatsapp_message
from app.core.llm_processor import generate_gpt4_response
#from app.core.intent_classifier import classify_intent  # optional: for future use

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

        # (Optional) Intent classification can be added here later:
        # intent = classify_intent(message)

        prompt = message

        # Call GPT-4 API to generate a dynamic response
        gpt4_response = generate_gpt4_response(prompt)
        logging.info(f"GPT-4 generated response: {gpt4_response}")

        # Use Twilio to send the response back to the user
        twilio_sid = send_whatsapp_message(sender, gpt4_response)
        logging.info(f"Sent message via Twilio. SID: {twilio_sid}")

        return {"response": gpt4_response, "twilio_sid": twilio_sid}

    except Exception as e:
        logging.error("Error processing webhook request", exc_info=True)
        return {"error": str(e)}
