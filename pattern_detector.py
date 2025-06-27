
import pandas as pd

def detect_doji(df):
    body = abs(df['close'] - df['open'])
    range_ = df['high'] - df['low']
    return (body / range_) < 0.1

def detect_engulfing(df):
    prev = df.shift(1)
    bull = (df['close'] > df['open']) & (prev['close'] < prev['open']) & (df['open'] < prev['close']) & (df['close'] > prev['open'])
    bear = (df['close'] < df['open']) & (prev['close'] > prev['open']) & (df['open'] > prev['close']) & (df['close'] < prev['open'])
    return bull.astype(str).replace('True', 'Bullish Engulfing').replace('False', '').combine(
           bear.astype(str).replace('True', 'Bearish Engulfing'), lambda b, br: b or br)
