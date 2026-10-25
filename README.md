# Observatoire de la Fibre Optique

## 📝 Présentation du projet
Cette application web a été développée pour superviser la qualité de la fibre optique. Elle permet de centraliser les données des fournisseurs d'accès, d'analyser les performances via un réseau de neurones (TensorFlow) et de générer des rapports automatiques. Elle intègre également un espace citoyen pour les retours utilisateurs et un système de gestion des signalements.

## ⚙️ Stack Technique
- **Framework Backend** : Django 5
- **Base de données** : SQLite
- **Intelligence Artificielle** : Réseau de neurones (Keras/TensorFlow), Pandas, Scikit-Learn
- **Interface** : HTML/CSS (Design sur mesure)

## 🚀 Guide d'installation
1. Cloner le projet : `git clone https://github.com/bleck-collab/Observation-Fibre.git`
2. Créer l'environnement : `python -m venv .venv`
3. Activer : `.venv\Scripts\activate` (Windows)
4. Installer : `pip install django tensorflow pandas openpyxl scikit-learn joblib`
5. (Optionnel) Migrer : `python manage.py migrate`
6. Lancer : `python manage.py runserver`

## 👤 Accès
- **Interface publique** : `/` 
- **Console d'administration** : `/login/` ou `/admin/`

## 🔑 Comptes de test (Déjà configurés dans la base de données)

Pour faciliter la correction, la base de données est déjà fournie avec des comptes prêts à l'emploi. **Vous n'avez pas besoin de créer un compte administrateur ni de faire de migrations.**

Voici les identifiants pour tester la plateforme (allez sur `/login/`) :

*   **Compte ARTEC (Régulateur) :**
    *   Nom d'utilisateur : `admin_nyaina` (remplace par le vrai nom que tu as créé)
    *   Mot de passe : `admin1234` (remplace par le vrai mot de passe)

*   **Compte Opérateur (ex: YAS) :**
    *   Nom d'utilisateur : `yas` (remplace par le vrai nom que tu as créé)
    *   Mot de passe : `ya12345678` (remplace par le vrai mot de passe)