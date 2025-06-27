from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

# In-memory storage for subscribers
subscribers = set()

class SubscribeRequest(BaseModel):
    email: EmailStr

# SMTP Config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "palmcreditinfo@gmail.com"
SMTP_PASSWORD = "bwfr cxea okkh chwl"

# Email Template
WELCOME_SUBJECT = "🎉 Welcome to Forex Analyzer"
WELCOME_BODY = """
Hi there,

Thanks for subscribing to Forex Analyzer! ✅

You'll receive powerful AI-driven hybrid signals every 3 hours straight to this inbox. 📊

Stay tuned and trade smart! 💹

— The Forex Analyzer Team
"""

def send_welcome_email(to_email: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email
        msg["Subject"] = WELCOME_SUBJECT
        msg.attach(MIMEText(WELCOME_BODY, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, msg.as_string())

    except Exception as e:
        print("❌ Failed to send welcome email:", e)

@router.post("/subscribe")
def subscribe(request: SubscribeRequest):
    if not request.email:
        raise HTTPException(status_code=400, detail="Email is required")

    if request.email in subscribers:
        raise HTTPException(status_code=400, detail="Email already subscribed")

    try:
        subscribers.add(request.email)
        send_welcome_email(request.email)
        return {"message": "Subscription successful, welcome email sent."}

    except Exception as e:
        print("⚠️ Subscription error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")