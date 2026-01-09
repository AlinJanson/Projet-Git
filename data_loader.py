import yfinance as yf
import pandas as pd

def fetch_data(tickers, interval="1d", period="1y"):
    if period in ["1y", "2y", "5y", "max"]:
        interval = "1d"

    try:
        data = yf.download(tickers, period=period, interval=interval, progress=False, auto_adjust=True)
        if data.empty:
            return None

        if isinstance(data.columns, pd.MultiIndex):
            data = data.xs(tickers, level=1, axis=1) if tickers in data.columns.levels[1] else data

        return data
    except Exception as e:
        print(f"Erreur API: {e}")
        return None