import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


# Load credentials from environment variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

def send_message(from_, to, body):
    """
    Send a WhatsApp message using Twilio.
    Args:
        from_ (str): The Twilio WhatsApp number (e.g., 'whatsapp:+14155238886')
        to (str): The recipient's WhatsApp number (e.g., 'whatsapp:+234...')
        body (str): The message body
    """
    try:
        message = client.messages.create(
            body=body,
            from_=from_,
            to=to
        )
        print('Message sent! SID:', message.sid)
    except Exception as e:
        print('Failed to send message:', e)
