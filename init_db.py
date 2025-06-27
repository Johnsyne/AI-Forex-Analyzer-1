# init_db.py

from database import Base, engine
from models import Subscriber  # Add all models here

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully.")
