
import requests
import pandas as pd
from datetime import datetime, timedelta

TIINGO_API_KEY = "095183391b68605973586b38e9035cc188639e01"

def fetch_ohlcv(symbol: str, days: int = 100):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    url = f"https://api.tiingo.com/tiingo/fx/{symbol}/prices?startDate={start_date.date()}&resampleFreq=1hour&token={TIINGO_API_KEY}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df
