import pandas as pd
import numpy as np

def apply_strategies(df, short_window=20, long_window=50):
    """
    Applique les stratégies Buy & Hold et Momentum.
    """
    data = df.copy()
    
    # 1. Rendements quotidiens
    data['Returns'] = data['Close'].pct_change()
    
    # --- STRATÉGIE 1 : BUY & HOLD ---
    data['Buy_Hold_Cum'] = (1 + data['Returns']).cumprod() * 100
    
    # --- STRATÉGIE 2 : MOMENTUM ---
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    
    data['Signal'] = np.where(data['SMA_Short'] > data['SMA_Long'], 1, 0)
    data['Position'] = data['Signal'].shift(1)
    
    data['Strategy_Returns'] = data['Position'] * data['Returns']
    data['Momentum_Cum'] = (1 + data['Strategy_Returns']).cumprod() * 100
    
    return data.dropna()

def compute_performance_metrics(df):
    """
    Calcule le Ratio de Sharpe et le Max Drawdown.
    """
    volatility = df['Strategy_Returns'].std() * (252**0.5)
    
    if volatility == 0:
        sharpe_ratio = 0
    else:
        sharpe_ratio = (df['Strategy_Returns'].mean() * 252) / volatility
    
    cumulative = df['Momentum_Cum']
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return {
        "Sharpe Ratio": round(sharpe_ratio, 2),
        "Max Drawdown": f"{max_drawdown:.2%}",
        "Volatility": f"{volatility:.2%}"
    }