import os
import django
import random

# Configuration de l'environnement Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Importation de tes modèles
from qos_engine.models import AvisPublic, Sondage, ReponseSondage, SanctionRecompense, QoSMetric

print("⏳ Génération des fausses données en cours...")

# 1. Générer des avis publics (pour l'accueil)
commentaires = [
    "La fibre est très stable dans mon quartier. !", 
    "Coupures fréquentes le soir, très deçu.",
    "Le service client répond rapidement, merci.",
    "Trop cher pour la qualité proposée.",
    "Je capte bien la 4G dans la capitale."
]
for _ in range(15):
    op = random.choice(['YAS', 'Orange', 'Airtel'])
    note = random.randint(1, 5)
    commentaire = random.choice(commentaires) if random.random() > 0.3 else ""
    AvisPublic.objects.create(operateur=op, note=note, commentaire=commentaire)

print("✅ Avis publics créés.")

# 2. Générer des sondages et des réponses
sondage1, _ = Sondage.objects.get_or_create(
    titre="Qualité de la 4G", 
    question="Comment trouvez-vous la couverture 4G cette année ?",
    createur_type="ARTEC"
)
sondage2, _ = Sondage.objects.get_or_create(
    titre="Service Client Orange", 
    question="Êtes-vous satisfait de l'accueil en agence ?",
    createur_type="OPERATEUR",
    operateur_cible="Orange"
)

for _ in range(10):
    ReponseSondage.objects.create(sondage=sondage1, note=random.randint(1, 5))
    ReponseSondage.objects.create(sondage=sondage2, note=random.randint(1, 5))

print("✅ Sondages et réponses créés.")

# 3. Générer de fausses alertes (sanctions/félicitations) pour les dashboards
for _ in range(5):
    SanctionRecompense.objects.create(
        operateur='YAS', type_alerte='felicitation', score_qos=random.uniform(85, 98),
        message="Débit fibre optimal constaté sur la zone."
    )
    SanctionRecompense.objects.create(
        operateur='Airtel', type_alerte='sanction', score_qos=random.uniform(15, 35),
        message="Perte de signal importante sur le réseau."
    )
    SanctionRecompense.objects.create(
        operateur='Orange', type_alerte='felicitation', score_qos=random.uniform(85, 95),
        message="Bonne stabilité de la latence."
    )

print("✅ Sanctions et félicitations créées.")
print("🎉 TOUTES LES DONNÉES DE DÉMONSTRATION SONT PRÊTES !")