from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, ALERT_TO_NUMBER

def send_sms_twilio(text):
    """Send a plain SMS alert using Twilio REST API."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=text,
            from_=TWILIO_FROM_NUMBER,
            to=ALERT_TO_NUMBER
        )
        print(f"✅ SMS sent (sid={message.sid})")
    except Exception as e:
        print("❌ Failed to send SMS:", e)
