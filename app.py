import streamlit as st
import plotly.graph_objects as go
import time
# Assure-toi que les fichiers sont bien dans le dossier 'src'
from src.prediction import predict_linear_regression
from src.data_loader import fetch_data 
from src.quant_a import apply_strategies, compute_performance_metrics

# Configuration de la page
st.set_page_config(page_title="Finance Dashboard", layout="wide")
st.title("📊 Plateforme de Recherche Quantitative")

# 1. Barre latérale
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisir un module", ["Analyse Single Asset (Quant A)", "Analyse Portefeuille (Quant B)"])
st.sidebar.divider()
st.sidebar.subheader("Paramètres globaux")

# 2. Logique du Module Quant A
if page == "Analyse Single Asset (Quant A)":
    st.header("📈 Analyse Univariée (Single Asset)")

    # --- INPUTS (Ticker & Période) ---
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.selectbox(
            "Choisir l'actif", 
            ["EURUSD=X", "GC=F", "BTC-USD", "^GSPC", "ENGIE.PA", "AAPL"],
            index=2
        )
    with col2:
        period = st.selectbox(
            "Période historique", 
            ["3mo", "6mo", "1y", "2y", "5y", "max"], 
            index=2
        )

    # --- PARAMÈTRES STRATÉGIE ---
    with st.expander("⚙️ Paramètres de la Stratégie Momentum", expanded=True):
        col_a, col_b = st.columns(2)
        short_w = col_a.slider("Moyenne Mobile Courte", 5, 50, 20)
        long_w = col_b.slider("Moyenne Mobile Longue", 51, 200, 50)

    # --- RÉCUPÉRATION ET CALCULS ---
    with st.spinner('Chargement et analyse des données...'):
        df_raw = fetch_data(ticker, period=period)

    if df_raw is not None and not df_raw.empty:
        # Calcul de la stratégie
        df_analyzed = apply_strategies(df_raw, short_window=short_w, long_window=long_w)
        # Calcul des métriques
        metrics = compute_performance_metrics(df_analyzed)

        # --- 1. AFFICHAGE DES MÉTRIQUES ---
        st.markdown("### 📊 Performance de la Stratégie")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Sharpe Ratio", metrics["Sharpe Ratio"])
        kpi2.metric("Max Drawdown", metrics["Max Drawdown"], delta_color="inverse")
        kpi3.metric("Volatilité Annualisée", metrics["Volatility"])
        st.divider()

        # --- 2. GRAPHIQUE PRINCIPAL ---
        st.subheader(f"Comparaison : Prix vs Stratégie ({ticker})")
        fig = go.Figure()
        
        # Courbe Prix
        fig.add_trace(go.Scatter(
            x=df_analyzed.index, y=df_analyzed['Buy_Hold_Cum'], 
            name="Prix Actif (Buy & Hold)", line=dict(color='#1f77b4', width=2)
        ))
        
        # Courbe Stratégie
        fig.add_trace(go.Scatter(
            x=df_analyzed.index, y=df_analyzed['Momentum_Cum'], 
            name=f"Stratégie Momentum", line=dict(color='#ff7f0e', width=2)
        ))
        
        fig.update_layout(title="Performance Base 100", template="plotly_dark", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        # --- 3. BONUS : PRÉDICTION ML ---
        st.markdown("---")
        st.subheader("🤖 Prédiction de Tendance (Bonus ML)")
        
        if st.checkbox("Afficher la prédiction future (Régression Linéaire)"):
            days_pred = st.slider("Horizon de prévision (Jours)", 7, 90, 30)
            
            with st.spinner("Entraînement du modèle..."):
                df_pred = predict_linear_regression(df_raw, days_to_predict=days_pred)
                
                fig_pred = go.Figure()
                recent_data = df_raw.iloc[-180:] # Zoom sur les 6 derniers mois
                
                fig_pred.add_trace(go.Scatter(x=recent_data.index, y=recent_data['Close'], name="Historique Récent", line=dict(color='#1f77b4')))
                fig_pred.add_trace(go.Scatter(x=df_pred.index, y=df_pred['Predicted_Close'], name="Prévision", line=dict(color='#00CC96', width=3, dash='dot')))
                
                fig_pred.update_layout(title=f"Projection à {days_pred} jours", template="plotly_dark")
                st.plotly_chart(fig_pred, use_container_width=True)

    else:
        st.error(f"Impossible de récupérer les données pour {ticker}. Vérifiez votre connexion ou le ticker.")

# 3. Logique du Module Quant B (Placeholder)
else:
    st.header("Analyse de Portefeuille Multi-Actifs")
    st.info("Module Quant B (Multi-Asset) en attente d'intégration...")