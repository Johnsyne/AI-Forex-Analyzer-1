from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from signal_endpoint import router as signal_router
from hybrid_signal import router as hybrid_router
from news_sentiment_endpoint import router as news_router
from subscribe_endpoint import router as subscribe_router
from apscheduler.schedulers.background import BackgroundScheduler
from tasks import send_hybrid_signals_to_subscribers
from news_sentiment_endpoint import router as news_sentiment_router


app = FastAPI(
    title="Forex Analyzer API",
    description="API backend for forex signals and news sentiment analysis.",
    version="1.0.0",
)

# ✅ Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root health check
@app.get("/")
def read_root():
    return {"message": "Forex Analyzer API is running"}

# ✅ Register all routers
app.include_router(signal_router, prefix="/api")
app.include_router(hybrid_router, prefix="/api")
app.include_router(news_router, prefix="/api")
app.include_router(subscribe_router, prefix="/api")
app.include_router(news_sentiment_router, prefix="/api")

# ✅ Start background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_hybrid_signals_to_subscribers, 'interval', hours=3)
scheduler.start()

# ✅ Create all tables
Base.metadata.create_all(bind=engine)
