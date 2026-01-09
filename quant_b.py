import pandas as pd
import numpy as np

def clean_data_for_portfolio(df_raw, tickers):
    """
    Extracts 'Close' prices and handles MultiIndex structures.
    """
    data = pd.DataFrame()
    
    # Handle MultiIndex (multiple tickers)
    if isinstance(df_raw.columns, pd.MultiIndex):
        for ticker in tickers:
            try:
                # Check level 0 or level 1 depending on yfinance version/structure
                if ticker in df_raw.columns.levels[0]: 
                     data[ticker] = df_raw[ticker]['Close']
                elif 'Close' in df_raw.columns.levels[0]:
                     data[ticker] = df_raw['Close'][ticker]
            except KeyError:
                continue
    # Handle Single Index (single ticker treated as list)
    else:
        # If it's a simple dataframe, the column might be 'Close' or the ticker name
        if 'Close' in df_raw.columns:
            data[tickers[0]] = df_raw['Close']
        else:
            # Fallback
            data = df_raw
            
    return data.ffill().dropna()

