from sqlalchemy.orm import Session
from database import SessionLocal
from models import Subscriber
import smtplib
from email.mime.text import MIMEText
import requests

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "palmcreditinfo@gmail.com"
SMTP_PASSWORD = "bwfr cxea okkh chwl"

SIGNAL_ENDPOINT = "http://localhost:8000/api/hybrid"  # Adjust if deployed

EMAIL_SUBJECT = "📊 Forex Analyzer: Your 3hr Hybrid Signal Report"

SIGNAL_HEADER = """
Hi Trader 👋,

Here are your latest hybrid signals based on technical + news sentiment intelligence:

🔽🔼 = Direction
📈 = Confidence Level
📌 = Entry/TP/SL
"""

SIGNAL_FOOTER = """
---
⏱ Delivered every 3 hours by Forex Analyzer
🚀 Trade wisely, win consistently.
"""

def send_hybrid_signals_to_subscribers():
    db: Session = SessionLocal()
    subscribers = db.query(Subscriber).all()

    try:
        res = requests.get(SIGNAL_ENDPOINT)
        hybrid_signals = res.json()
    except Exception as e:
        print("❌ Failed to fetch signals:", e)
        db.close()
        return

    # Format signal details
    lines = []
    for sig in hybrid_signals:
        symbol = sig['symbol']
        signal = sig['signal']
        confidence = sig.get('confidence', '?')
        entry = sig.get('entry', '-')
        tp = sig.get('take_profit', '-')
        sl = sig.get('stop_loss', '-')

        emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"
        lines.append(f"{emoji} {symbol} — {signal} ({confidence}%)\n📌 Entry: {entry} | TP: {tp} | SL: {sl}\n")

    full_message = SIGNAL_HEADER + "\n\n" + "\n".join(lines) + "\n\n" + SIGNAL_FOOTER

    for sub in subscribers:
        try:
            msg = MIMEText(full_message)
            msg['Subject'] = EMAIL_SUBJECT
            msg['From'] = SMTP_USERNAME
            msg['To'] = sub.email

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
                print(f"✅ Sent to {sub.email}")
        except Exception as e:
            print(f"❌ Failed to send to {sub.email}:", e)

    db.close()
