import streamlit as st
from src.data_loader import get_financial_data
import time

# Configuration de la page
st.set_page_config(page_title="Finance Dashboard", layout="wide")

# 1. Gestion de l'actualisation automatique (toutes les 5 min) 
# Streamlit propose st.empty() ou un loop avec time.sleep, 
# mais la méthode moderne est le fragment ou l'auto-refresh.

st.title("📊 Plateforme de Recherche Quantitative")

# 2. Barre latérale pour la navigation [cite: 10]
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisir un module", ["Analyse Single Asset (Quant A)", "Analyse Portefeuille (Quant B)"])

# 3. Paramètres communs (Dates, Tickers)
st.sidebar.divider()
st.sidebar.subheader("Paramètres globaux")
refresh_rate = 300  # 5 minutes en secondes 

# 4. Affichage des modules
if page == "Analyse Single Asset (Quant A)":
    st.header("Analyse Univariée")
    # C'est ici que l'étudiant A importera et appellera sa fonction
    st.info("Module Quant A en attente d'intégration...")

else:
    st.header("Analyse de Portefeuille Multi-Actifs")
    # C'est ici que l'étudiant B importera et appellera sa fonction
    st.info("Module Quant B en attente d'intégration...")

# Logique de rafraîchissement simple
# st.rerun() peut être utilisé ici avec un timer