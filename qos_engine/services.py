import os
import pandas as pd
import numpy as np
import joblib
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import MeanSquaredError
from .models import QoSMetric, SanctionRecompense

def traiter_dataset(dataset):
    """Analyse le fichier importé et génère les alertes associées"""
    try:
        # 1. Initialisation du modèle TensorFlow et du scaler
        dossier_ml = os.path.join(settings.BASE_DIR, 'ml_models')
        chemin_modele = os.path.join(dossier_ml, 'modele_qos.h5')
        chemin_scaler = os.path.join(dossier_ml, 'scaler_qos.pkl')
        
        reseau_ia = load_model(chemin_modele, custom_objects={'mse': MeanSquaredError()})
        normaliseur = joblib.load(chemin_scaler)

        # 2. Importation des données (CSV ou Excel)
        chemin_fichier = dataset.fichier.path
        if chemin_fichier.endswith('.csv'):
            donnees = pd.read_csv(chemin_fichier)
        else:
            donnees = pd.read_excel(chemin_fichier)

        # 3. Contrôle de la structure du fichier
        colonnes_attendues = ['csr', 'debit', 'latence', 'disponibilite']
        for col in colonnes_attendues:
            if col not in donnees.columns:
                return False, f"Erreur de format : La colonne '{col}' est absente."

        # 4. Traitement des lignes du fichier
        for index, ligne in donnees.iterrows():
            valeurs = np.array([[ligne['csr'], ligne['debit'], ligne['latence'], ligne['disponibilite']]])
            valeurs_normalisees = normaliseur.transform(valeurs)
            
            # Prédiction IA
            score_ia = float(reseau_ia.predict(valeurs_normalisees, verbose=0).ravel()[0])
            score_ia = np.clip(score_ia, 0, 100) # Bornage entre 0 et 100

            # Définition du niveau de qualité
            if score_ia <= 40: 
                niveau = "Critique"
            elif score_ia <= 70: 
                niveau = "Moyen"
            elif score_ia <= 90: 
                niveau = "Satisfaisant"
            else: 
                niveau = "Excellent"

            # Enregistrement dans la base de données
            QoSMetric.objects.create(
                dataset=dataset, 
                csr=ligne['csr'], 
                debit=ligne['debit'],
                latence=ligne['latence'], 
                disponibilite=ligne['disponibilite'],
                score_qos=score_ia, 
                interpretation=niveau
            )

            # 5. Système de bonus/malus automatique
            if score_ia <= 30:
                SanctionRecompense.objects.create(
                    operateur=dataset.operateur, 
                    type_alerte='sanction',
                    score_qos=score_ia, 
                    message=f"Alerte : Performance réseau insuffisante détectée ({score_ia:.2f}/100)."
                )
            elif score_ia >= 85:
                SanctionRecompense.objects.create(
                    operateur=dataset.operateur, 
                    type_alerte='felicitation',
                    score_qos=score_ia, 
                    message=f"Félicitations : Excellente stabilité réseau ({score_ia:.2f}/100)."
                )

        # Mise à jour de l'état du fichier
        dataset.traite = True
        dataset.save()
        return True, "Le fichier a été analysé par le système avec succès."

    except Exception as e:
        return False, f"Une erreur est survenue durant le traitement : {str(e)}"