from fastapi import APIRouter
from news_sentiment import fetch_forex_news, analyze_sentiment

router = APIRouter()

@router.get("/news/sentiment")
def get_news_sentiment():
    news_data = fetch_forex_news()
    sentiment = analyze_sentiment(news_data)
    return {"results": sentiment}
