def label_signal(row):
    score = 0

    # RSI signals
    if row['rsi'] < 30:
        score += 1  # bullish
    elif row['rsi'] > 70:
        score -= 1  # bearish

    # MACD
    if row['macd'] > row['signal']:
        score += 1  # bullish
    elif row['macd'] < row['signal']:
        score -= 1  # bearish

    # EMA
    if row['close'] > row['ema']:
        score += 1  # bullish
    elif row['close'] < row['ema']:
        score -= 1  # bearish

    # Bollinger Bands
    if row['close'] < row['bb_lower']:
        score += 1  # bullish reversal
    elif row['close'] > row['bb_upper']:
        score -= 1  # bearish reversal

    # Candlestick Pattern (already True/False or string)
    if str(row['pattern']).lower() in ['bullish engulfing', 'doji']:
        score += 1
    elif str(row['pattern']).lower() in ['bearish engulfing']:
        score -= 1

    # Label based on score
    if score >= 2:
        return 'BUY'
    elif score <= -2:
        return 'SELL'
    else:
        return 'NEUTRAL'
