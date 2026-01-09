#Plateforme de Recherche Quantitative - Asset Management Paris

Ce projet est une plateforme de dashboarding financier interactive permettant de suivre des actifs en temps réel et d'analyser des stratégies de backtesting.

##Fonctionnalités Principales
* **Données en temps réel** : Récupération dynamique via API.
* **Analyse Univariée (Quant A)** : Backtesting de stratégies (Momentum, Buy & Hold).
* **Analyse de Portefeuille (Quant B)** : Simulation multi-actifs et matrices de corrélation.
* **Rapports Automatisés** : Génération quotidienne de métriques de risque.

## Automatisation et Rapports (Point 6) 

Un script de reporting quotidien est configuré sur le serveur Linux pour s'exécuter automatiquement via **cron**.

* **Description** : Le script `daily_report.py` récupère les données historiques, calcule la volatilité annualisée, les prix Open/Close et le Max Drawdown.
* **Commande Cron utilisée** :
  ```bash
  00 20 * * * /usr/bin/python3 /home/antoine/Projet-Git/daily_report.py >> /home/antoine/Projet-Git/cron_log.log 2>&1

first : pip install -r requirements.txt

then : streamlit run app.py
