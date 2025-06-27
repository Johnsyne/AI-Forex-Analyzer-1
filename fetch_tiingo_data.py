import requests
import pandas as pd

TIINGO_API_KEY = "095183391b68605973586b38e9035cc188639e01"

def fetch_ohlcv(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    url = f"https://api.tiingo.com/tiingo/fx/{symbol}/prices"
    headers = {"Content-Type": "application/json"}
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "resampleFreq": "1Day",
        "token": TIINGO_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Check if data is empty
        if not isinstance(data, list) or len(data) == 0:
            print(f"❌ No data returned for {symbol}")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        if df.empty:
            print(f"❌ Empty DataFrame after conversion for {symbol}")
            return pd.DataFrame()

        df["symbol"] = symbol.upper()

        # Handle missing volume
        if "volume" not in df.columns:
            df["volume"] = 1000

        return df[["symbol", "date", "open", "high", "low", "close", "volume"]]
    
    except Exception as e:
        print(f"🚨 Failed to fetch or parse data for {symbol}: {e}")
        return pd.DataFrame()
