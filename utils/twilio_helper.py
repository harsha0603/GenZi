from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

def send_whatsapp_message(to_number: str, body: str) -> str:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=twilio_whatsapp_number,
        body=body,
        to=to_number
    )
    return message.sid
