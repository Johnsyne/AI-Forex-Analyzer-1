from fastapi import APIRouter, Query
import pandas as pd
import numpy as np
import requests
import joblib
from datetime import datetime, timedelta
from indicators import compute_rsi, compute_macd, compute_ema, compute_bollinger

router = APIRouter()

# Load model and label encoder globally so it's loaded once
model = joblib.load("signal_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")
TIINGO_TOKEN = "095183391b68605973586b38e9035cc188639e01"

def get_live_quotes(symbol):
    try:
        res = requests.get(
            f"https://api.tiingo.com/tiingo/fx/top?tickers={symbol}",
            headers={"Content-Type": "application/json"},
            params={"token": TIINGO_TOKEN}
        )
        res.raise_for_status()
        data = res.json()
        if not data or not isinstance(data, list):
            return None
        quote = data[0]
        return {
            "bid": quote.get("bidPrice"),
            "ask": quote.get("askPrice"),
            "mid": quote.get("midPrice")
        }
    except Exception:
        return None

def get_model_prediction(symbol):
    try:
        end = datetime.today()
        start = end - timedelta(days=50)

        url = f"https://api.tiingo.com/tiingo/fx/{symbol}/prices"
        params = {
            "startDate": start.strftime("%Y-%m-%d"),
            "endDate": end.strftime("%Y-%m-%d"),
            "resampleFreq": "1Day",
            "token": TIINGO_TOKEN,
        }

        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        df = pd.DataFrame(data)
        if df.empty:
            return {"error": f"No historical data returned for {symbol}"}

        df.rename(columns={
            "openPrice": "open",
            "highPrice": "high",
            "lowPrice": "low",
            "closePrice": "close"
        }, inplace=True)

        df["volume"] = df.get("volumeNotional", 1000)
        df["rsi"] = compute_rsi(df["close"])
        df["macd"], df["signal_line"] = compute_macd(df["close"])
        df["ema"] = compute_ema(df["close"])
        df["bb_upper"], df["bb_lower"] = compute_bollinger(df["close"])

        latest = df.iloc[-1]
        features = pd.DataFrame([{
            "open": latest["open"],
            "high": latest["high"],
            "low": latest["low"],
            "close": latest["close"],
            "volume": latest["volume"],
            "rsi": latest["rsi"],
            "macd": latest["macd"],
            "signal": latest["signal_line"],
            "ema": latest["ema"],
            "bb_upper": latest["bb_upper"],
            "bb_lower": latest["bb_lower"],
        }])

        probs = model.predict_proba(features)[0]
        pred_index = int(np.argmax(probs))
        pred_label = label_encoder.inverse_transform([pred_index])[0]
        confidence = round(float(probs[pred_index]) * 100, 2)

        quotes = get_live_quotes(symbol.upper())
        if not quotes or "ask" not in quotes:
            return {"error": "Failed to fetch real-time ask price"}

        entry = round(float(quotes["ask"]), 5)
        sl = round(entry * 0.995, 5)
        tp = round(entry * 1.005, 5)
        if pred_label == "SELL":
            sl, tp = tp, sl

        return {
            "symbol": symbol.upper(),
            "signal": pred_label,
            "confidence": confidence,
            "entry": entry,
            "stop_loss": sl,
            "take_profit": tp,
            "live_prices": {
                "bid": quotes["bid"],
                "ask": quotes["ask"],
                "mid": quotes["mid"]
            }
        }

    except Exception as e:
        return {"error": str(e)}

@router.get("/signal")
def signal_api(symbol: str = Query(...)):
    return get_model_prediction(symbol)
