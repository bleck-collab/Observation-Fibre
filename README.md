# Observatoire de la Fibre Optique

## 📝 Présentation du projet
Cette application web a été développée pour superviser la qualité de la fibre optique. Elle permet de centraliser les données des fournisseurs d'accès, d'analyser les performances via un réseau de neurones (TensorFlow) et de générer des rapports automatiques. Elle intègre également un espace citoyen pour les retours utilisateurs et un système de gestion des signalements.

## ⚙️ Stack Technique
- **Framework Backend** : Django 5
- **Base de données** : SQLite
- **Intelligence Artificielle** : Réseau de neurones (Keras/TensorFlow), Pandas, Scikit-Learn
- **Interface** : HTML/CSS (Design sur mesure)

## 🚀 Guide d'installation
1. Cloner le projet : `git clone [LIEN_DU_REPO]`
2. Créer l'environnement : `python -m venv .venv`
3. Activer : `.venv\Scripts\activate` (Windows)
4. Installer : `pip install django tensorflow pandas openpyxl scikit-learn joblib`
5. Migrer : `python manage.py migrate`
6. Lancer : `python manage.py runserver`

## 👤 Accès
- **Interface publique** : `/` 
- **Console d'administration** : `/login/` ou `/admin/`