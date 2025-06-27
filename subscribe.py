# main.py or routes/subscribe.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI()

subscribers = set()  # In-memory storage (replace with DB if needed)

class SubscriptionRequest(BaseModel):
    email: EmailStr

@app.post("/api/subscribe")
async def subscribe_user(data: SubscriptionRequest):
    if data.email in subscribers:
        raise HTTPException(status_code=400, detail="Already subscribed")
    
    subscribers.add(data.email)
    
    # Optionally send welcome email or store to DB
    return {"message": "Subscription successful"}
