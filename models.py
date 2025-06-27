# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Subscriber(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, index=True)  # ✅ Add this line
    email = Column(String, unique=True, index=True)
