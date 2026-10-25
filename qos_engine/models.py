from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    OPERATEURS = [('YAS', 'YAS'), ('Orange', 'Orange'), ('Airtel', 'Airtel')]
    
    operateur = models.CharField(max_length=20, choices=OPERATEURS)
    fichier = models.FileField(upload_to='datasets/')
    date_upload = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Dataset {self.operateur} - {self.date_upload.strftime('%Y-%m-%d %H:%M')}"

class QoSMetric(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='metriques')
    csr = models.FloatField()
    debit = models.FloatField()
    latence = models.FloatField()
    disponibilite = models.FloatField()
    score_qos = models.FloatField()
    interpretation = models.CharField(max_length=50)
    date_prediction = models.DateTimeField(auto_now_add=True)

class SanctionRecompense(models.Model):
    TYPE_CHOICES = [('sanction', 'Sanction'), ('felicitation', 'Félicitation')]
    
    operateur = models.CharField(max_length=20)
    type_alerte = models.CharField(max_length=20, choices=TYPE_CHOICES)
    score_qos = models.FloatField()
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.expediteur.username} à {self.destinataire.username} : {self.contenu[:30]}..."

class AvisPublic(models.Model):
    OPERATEURS = [('YAS', 'YAS'), ('Orange', 'Orange'), ('Airtel', 'Airtel')]
    
    operateur = models.CharField(max_length=20, choices=OPERATEURS)
    note = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # Note de 1 à 5
    commentaire = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True, help_text="Optionnel")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis {self.operateur} - {self.note}/5"

class Sondage(models.Model):
    CREATEUR_CHOICES = [('ARTEC', 'ARTEC'), ('OPERATEUR', 'Opérateur')]
    OPERATEURS = [('YAS', 'YAS'), ('Orange', 'Orange'), ('Airtel', 'Airtel')]
    
    titre = models.CharField(max_length=200)
    question = models.CharField(max_length=255)
    createur_type = models.CharField(max_length=20, choices=CREATEUR_CHOICES)
    operateur_cible = models.CharField(max_length=20, choices=OPERATEURS, blank=True, null=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.createur_type}] {self.titre}"

class ReponseSondage(models.Model):
    sondage = models.ForeignKey(Sondage, on_delete=models.CASCADE, related_name='reponses')
    note = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # 1 à 5
    commentaire = models.TextField(blank=True, null=True)
    date_reponse = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réponse à {self.sondage.titre} - {self.note}/5"