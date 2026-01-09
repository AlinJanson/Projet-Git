import yfinance as yf
import pandas as pd

def fetch_data(tickers, interval="1d", period="1y"):
    # Si la période est longue, force l'intervalle à 1 jour
    if period in ["1y", "2y", "5y", "max"]:
        interval = "1d"

    try:
        # Téléchargement des données
        # group_by='column' assure une structure compatible (Prix, Ticker)
        data = yf.download(tickers, period=period, interval=interval, 
                           progress=False, auto_adjust=True, group_by='column')
        
        if data is None or data.empty:
            print("Aucune donnée retournée par yfinance.")
            return None

        return data

    except Exception as e:
        print(f"Erreur API yfinance : {e}")
        return None