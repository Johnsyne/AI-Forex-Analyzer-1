from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Subscriber

router = APIRouter()

# 📥 Get all subscribers
@router.get("/subscribers")
def get_subscribers(db: Session = Depends(get_db)):
    subscribers = db.query(Subscriber).all()
    return [{"email": s.email} for s in subscribers]

# ❌ Delete a subscriber
@router.delete("/subscribers/{email}")
def delete_subscriber(email: str, db: Session = Depends(get_db)):
    subscriber = db.query(Subscriber).filter_by(email=email).first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    db.delete(subscriber)
    db.commit()
    return {"message": f"Subscriber {email} deleted."}
