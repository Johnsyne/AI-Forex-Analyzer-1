import pandas as pd
from datetime import datetime, timedelta
from fetch_tiingo_data import fetch_ohlcv
from indicators import compute_rsi, compute_macd, compute_ema, compute_bollinger
from pattern_detector import detect_doji, detect_engulfing
from signal_labeler import label_signal

symbols = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "USDCAD", "NZDUSD",
    "EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "CHFJPY", "USDSGD", "EURAUD", "GBPCHF"
]

start_date = (datetime.today() - timedelta(days=180)).strftime("%Y-%m-%d")
end_date = datetime.today().strftime("%Y-%m-%d")

all_data = []

for symbol in symbols:
    try:
        df = fetch_ohlcv(symbol, start_date, end_date)
        df["rsi"] = compute_rsi(df["close"])
        df["macd"], df["signal"] = compute_macd(df["close"])
        df["ema"] = compute_ema(df["close"])
        df["bb_upper"], df["bb_lower"] = compute_bollinger(df["close"])
        df["pattern"] = detect_engulfing(df).combine(detect_doji(df), lambda e, d: d if d else e)
        df["signal_label"] = df.apply(label_signal, axis=1)
        all_data.append(df)
    except Exception as e:
        print(f"Error with {symbol}: {e}")

result = pd.concat(all_data)
result.to_csv("training_data_full.csv", index=False)
print("Saved to training_data_full.csv")
