# Guide de Déploiement - Plateforme Finance

Ce document détaille la configuration nécessaire pour faire fonctionner la plateforme sur un serveur Linux (Ubuntu) et automatiser les rapports quotidiens.

## 1. Automatisation (Point 6 - Daily Report)
Un script `daily_report.py` a été mis en place pour générer des métriques financières chaque soir.

### Configuration du Cron
Pour installer la tâche planifiée, exécutez `crontab -e` et ajoutez la ligne suivante en bas du fichier :

```bash
00 20 * * * /usr/bin/python3 /home/antoine/Projet-Git/daily_report.py >> /home/antoine/Projet-Git/cron_log.log 2>&1
