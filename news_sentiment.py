# news_sentiment.py
import requests
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

NEWS_API_KEY = "pub_a25e220567754f3697655337096c3680"
SYMBOLS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "USDCAD", "NZDUSD",
    "EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "CHFJPY", "USDSGD", "EURAUD", "GBPCHF"
]

analyzer = SentimentIntensityAnalyzer()
_cache = {"timestamp": 0, "data": {}}

def get_symbol_keywords():
    return {
        "EURUSD": ["eurusd", "euro", "usd", "eur", "us dollar"],
        "GBPUSD": ["gbpusd", "pound", "sterling", "gbp", "usd"],
        "USDJPY": ["usdjpy", "yen", "jpy", "japanese yen", "usd"],
        "AUDUSD": ["audusd", "australian dollar", "aud", "usd"],
        "USDCHF": ["usdchf", "swiss franc", "chf", "usd"],
        "USDCAD": ["usdcad", "canadian dollar", "cad", "usd"],
        "NZDUSD": ["nzdusd", "nzd", "kiwi", "usd"],
        "EURGBP": ["eurgbp", "euro", "pound", "gbp"],
        "EURJPY": ["eurjpy", "euro", "yen", "jpy"],
        "GBPJPY": ["gbpjpy", "pound", "yen", "gbp", "jpy"],
        "AUDJPY": ["audjpy", "australian dollar", "yen", "aud", "jpy"],
        "CHFJPY": ["chfjpy", "swiss franc", "yen", "chf", "jpy"],
        "USDSGD": ["usdsgd", "singapore dollar", "sgd", "usd"],
        "EURAUD": ["euraud", "euro", "australian dollar", "eur", "aud"],
        "GBPCHF": ["gbpchf", "pound", "swiss franc", "gbp", "chf"]
    }

def fetch_forex_news():
    now = time.time()
    if now - _cache["timestamp"] < 1800:
        return _cache["data"]

    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q=forex&language=en&category=business,top"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json().get("results", [])
        _cache["data"] = data
        _cache["timestamp"] = now
        return data
    except Exception as e:
        print("❌ News API error:", e)
        return []

def analyze_sentiment(news_data):
    keyword_map = get_symbol_keywords()
    result = {}

    for symbol in SYMBOLS:
        matched = []
        for article in news_data:
            title = article.get("title", "")
            link = article.get("link", "")
            content = article.get("content", "") or ""
            full_text = (title + " " + content).lower()

            if any(k in full_text for k in keyword_map[symbol]):
                sentiment = analyzer.polarity_scores(title)
                score = sentiment["compound"]
                confidence = round(abs(score) * 100, 1)

                matched.append({
                    "title": title,
                    "link": link,
                    "score": round(score, 4),
                    "confidence": confidence,
                })

        bullish = sorted([x for x in matched if x["score"] > 0.05], key=lambda x: -x["score"])[:2]
        bearish = sorted([x for x in matched if x["score"] < -0.05], key=lambda x: x["score"])[:2]

        avg_score = sum([x["score"] for x in matched]) / len(matched) if matched else 0.0
        signal = "BUY" if avg_score > 0.05 else "SELL" if avg_score < -0.05 else "NEUTRAL"
        confidence = f"{round(abs(avg_score) * 100, 1)}%"

        summary = (
            f"Recent news suggests a {signal.lower()} bias for {symbol}. "
            f"Confidence is moderate based on {len(matched)} articles."
        )

        result[symbol] = {
            "signal": signal,
            "confidence": confidence,
            "summary": summary,
            "top_bullish": bullish,
            "top_bearish": bearish
        }

    return result
