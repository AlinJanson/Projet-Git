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

def compute_portfolio_kpis(df_result, weights):
    """
    Calculates key metrics (Sharpe, Volatility, Correlation).
    """
    returns = df_result.pct_change().dropna()
    
    # Correlation Matrix (Assets only)
    asset_cols = [c for c in returns.columns if c != 'Portfolio']
    asset_returns = returns[asset_cols]
    corr_matrix = asset_returns.corr()
    
    # Annualized Metrics
    annual_return = returns['Portfolio'].mean() * 252
    portfolio_volatility = returns['Portfolio'].std() * (252**0.5)
    
    # Diversification Effect
    weighted_volatility = 0
    for ticker, weight in weights.items():
        if ticker in returns.columns:
            asset_vol = returns[ticker].std() * (252**0.5)
            weighted_volatility += asset_vol * weight
        
    diversification_benefit = weighted_volatility - portfolio_volatility
    sharpe_ratio = annual_return / portfolio_volatility if portfolio_volatility != 0 else 0
    
    return {
        "correlation_matrix": corr_matrix,
        "annual_return": annual_return,
        "portfolio_volatility": portfolio_volatility,
        "weighted_volatility": weighted_volatility,
        "diversification_effect": diversification_benefit,
        "sharpe_ratio": sharpe_ratio
    }

def simulate_portfolio(df_closes, weights, rebalance_strategy="Buy & Hold"):
    """
    Simulates portfolio evolution based on strategy.
    """
    data = df_closes.copy()
    
    if rebalance_strategy == "Buy & Hold":
        # Normalize Base 100
        normalized = (data / data.iloc[0]) * 100
        
        # Apply initial weights
        weighted_cols = normalized.copy()
        for ticker, w in weights.items():
            weighted_cols[ticker] = normalized[ticker] * w
            
        data['Portfolio'] = weighted_cols.sum(axis=1)
        
        # Keep asset columns normalized for comparison chart
        for ticker in weights.keys():
            data[ticker] = normalized[ticker]
            
    else: # Rebalancement Quotidien (Constant Mix)
        returns = data.pct_change().dropna()
        
        portfolio_returns = 0
        for ticker, w in weights.items():
            portfolio_returns += returns[ticker] * w
            
        portfolio_curve = (1 + portfolio_returns).cumprod() * 100
        
        # Realign and normalize
        data = data.iloc[1:].copy() # Align with returns
        data['Portfolio'] = portfolio_curve
        
        # Normalize assets for display
        normalized_assets = (data[list(weights.keys())] / data[list(weights.keys())].iloc[0]) * 100
        data.update(normalized_assets)

    return data