# hybrid_signal.py
from fastapi import APIRouter, Query
from signal_endpoint import get_model_prediction
from news_sentiment import fetch_forex_news, analyze_sentiment

router = APIRouter()

SYMBOLS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "USDCAD", "NZDUSD",
    "EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "CHFJPY", "USDSGD", "EURAUD", "GBPCHF"
]

@router.get("/hybrid_signal")
def get_hybrid_signal(symbol: str = Query(...)):
    try:
        tech_result = get_model_prediction(symbol)
        if "error" in tech_result:
            return tech_result

        raw_news = fetch_forex_news()
        sentiment_scores = analyze_sentiment(raw_news)
        symbol_data = sentiment_scores.get(symbol.upper(), {"score": 0})
        symbol_score = symbol_data["score"]

        # Combine logic
        ml_signal = tech_result["signal"]
        final_signal = ml_signal
        if symbol_score > 0.05:
            final_signal = "BUY"
        elif symbol_score < -0.05:
            final_signal = "SELL"

        tech_result["hybrid_signal"] = final_signal
        tech_result["sentiment_score"] = round(symbol_score, 4)
        tech_result["sentiment_signal"] = symbol_data.get("signal", "NEUTRAL")
        tech_result["headlines"] = symbol_data.get("headlines", [])

        return tech_result

    except Exception as e:
        return {"error": str(e)}
