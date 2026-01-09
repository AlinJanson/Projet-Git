import pandas as pd
import yfinance as yf
from datetime import datetime
import os

# Configuration sécurisée des chemins pour Cron
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
TICKERS = ["AAPL", "BTC-USD", "EURUSD=X"]

def calculate_metrics(ticker):
    """Downloads data and calculates basic daily metrics."""
    try:
        data = yf.download(ticker, period="1y", interval="1d", progress=False)
        if data.empty:
            return None
            
        # Get scalar values correctly
        last_close = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        
        # If last_close is a Series (common in new yfinance), take the float value
        if isinstance(last_close, pd.Series):
            last_close = last_close.item()
            prev_close = prev_close.item()
            
        daily_return = (last_close - prev_close) / prev_close
        
        # Volatility
        returns = data['Close'].pct_change()
        volatility = returns.std() * (252**0.5)
        
        # Max Drawdown
        cum_ret = (1 + returns).cumprod()
        drawdown = (cum_ret - cum_ret.cummax()) / cum_ret.cummax()
        max_dd = drawdown.min()
        
        if isinstance(max_dd, pd.Series):
             max_dd = max_dd.item()
        if isinstance(volatility, pd.Series):
             volatility = volatility.item()

        return {
            "Ticker": ticker,
            "Price": round(last_close, 2),
            "Daily_Return": f"{daily_return:.2%}",
            "Volatility": f"{volatility:.2%}",
            "Max_Drawdown": f"{max_dd:.2%}"
        }
    except Exception as e:
        print(f"Error for {ticker}: {e}")
        return None


