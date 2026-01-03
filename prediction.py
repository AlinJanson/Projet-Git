import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_linear_regression(df, days_to_predict=30):
    """
    Entraîne un modèle de régression linéaire sur l'historique récent
    et prédit les prix futurs.
    """
    # On travaille sur une copie pour ne pas toucher aux données brutes
    data = df.copy()

    # On se concentre sur les 6 derniers mois
    lookback = 126
    if len(data) > lookback:
        data = data.iloc[-lookback:]

    # Préparation des features (X)
    data['Date_Ordinal'] = pd.to_datetime(data.index).map(pd.Timestamp.toordinal)

    X = data['Date_Ordinal'].values.reshape(-1, 1)
    y = data['Close'].values

    # Entraînement
    model = LinearRegression()
    model.fit(X, y)

    # --- PRÉDICTION FUTURE ---
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=days_to_predict + 1)[1:]

    future_X = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    predicted_prices = model.predict(future_X)

    df_future = pd.DataFrame(index=future_dates)
    df_future['Predicted_Close'] = predicted_prices

    return df_future