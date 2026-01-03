import pandas as pd
import yfinance as yf
from datetime import datetime
import os

# Configuration sécurisée des chemins pour Cron
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
TICKERS = ["AAPL", "BTC-USD", "EURUSD=X"]

# ... (Le reste de tes fonctions calculate_metrics reste identique) ...

def generate_report():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        
    date_str = datetime.now().strftime("%Y-%m-%d")
    report_file = os.path.join(REPORT_DIR, f"report_{date_str}.txt")
    
    # ... (Le reste de ton code d'écriture est bon) ...
    
    # Ajoute print pour le log Cron
    print(f"[{datetime.now()}] Rapport généré : {report_file}")

if __name__ == "__main__":
    generate_report()