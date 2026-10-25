import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from sklearn.preprocessing import StandardScaler
import joblib

# 1. Préparation des données d'entraînement (Réseau Fibre)
# Variables : csr, debit, latence, disponibilite
data_X = np.array([
[82.5, 3.2, 85.0, 91.5], [85.1, 4.5, 72.0, 93.0], [88.8, 5.8, 65.0, 94.8],
[90.2, 6.7, 58.0, 95.5], [91.5, 7.9, 52.0, 96.2], [92.8, 8.8, 48.0, 97.0],
[93.6, 9.7, 44.0, 97.5], [94.5, 10.9, 40.0, 98.0], [95.1, 12.1, 36.0, 98.5],
[96.0, 13.5, 32.0, 99.0], [78.5, 2.5, 95.0, 89.0], [81.7, 3.8, 82.0, 91.5],
[87.2, 5.1, 70.0, 94.0], [89.5, 6.3, 61.0, 95.0], [92.0, 8.5, 49.0, 96.8],
[93.8, 10.2, 42.0, 97.8], [95.5, 12.8, 35.0, 98.7], [96.4, 14.6, 29.0, 99.2],
[97.1, 16.2, 25.0, 99.5], [98.0, 18.5, 20.0, 99.8]
], dtype=float)

data_Y = np.array([
18.0, 27.0, 34.0, 42.0, 49.0, 55.0, 61.0, 68.0, 74.0, 81.0, 10.0,
22.0, 31.0, 39.0, 53.0, 64.0, 76.0, 88.0, 95.0, 100.0
], dtype=float)

# 2. Normalisation des données
scaler_fibre = StandardScaler()
X_normalise = scaler_fibre.fit_transform(data_X)

print("Initialisation de l'apprentissage du modèle Fibre Optique...")

# 3. Construction du réseau de neurones (Architecture modifiée)
reseau = Sequential([
    Input(shape=(4,)),
    Dense(32, activation='relu'), # Différent de ton projet (16)
    Dense(12, activation='relu'), # Différent de ton projet (8)
    Dense(1, activation='linear')
])

# 4. Compilation avec un autre optimiseur
reseau.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])

# 5. Entraînement
reseau.fit(X_normalise, data_Y, epochs=300, verbose=0) # Différent de ton projet (200)

# 6. Sauvegarde du modèle
dossier_modeles = 'ml_models'
if not os.path.exists(dossier_modeles):
    os.makedirs(dossier_modeles)

reseau.save(f'{dossier_modeles}/modele_qos.h5')
joblib.dump(scaler_fibre, f'{dossier_modeles}/scaler_qos.pkl')

print("✅ Modèle de prédiction Fibre Optique généré et sauvegardé avec succès.")