
from ohlcv_fetcher import fetch_ohlcv
from indicators import compute_rsi, compute_macd

def generate_signal(symbol: str):
    df = fetch_ohlcv(symbol)
    if df.empty:
        return {"symbol": symbol, "signal": "NO_DATA"}

    df['rsi'] = compute_rsi(df['close'])
    df['macd'], df['signal_line'] = compute_macd(df['close'])

    latest = df.iloc[-1]
    signal = "NEUTRAL"
    reason = []

    if latest['rsi'] < 30 and latest['macd'] > latest['signal_line']:
        signal = "BUY"
        reason.append("RSI oversold + MACD bullish crossover")
    elif latest['rsi'] > 70 and latest['macd'] < latest['signal_line']:
        signal = "SELL"
        reason.append("RSI overbought + MACD bearish crossover")
    else:
        reason.append("No strong indicator match")

    return {
        "symbol": symbol,
        "signal": signal,
        "reason": ", ".join(reason),
        "indicators": {
            "RSI": round(latest['rsi'], 2),
            "MACD": round(latest['macd'], 3),
            "Signal Line": round(latest['signal_line'], 3)
        }
    }
