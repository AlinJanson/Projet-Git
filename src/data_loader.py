import yfinance as yf
import pandas as pd

def get_financial_data(tickers, period="1mo", interval="5m"):
    """
    Récupère les données de marché. 
    Gère les erreurs pour éviter le crash de l'app[cite: 60].
    """
    try:
        data = yf.download(tickers, period=period, interval=interval)
        if data.empty:
            return None
        return data['Close']
    except Exception as e:
        print(f"Erreur lors de la récupération : {e}")
        return None