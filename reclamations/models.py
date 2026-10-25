
import uuid
from django.db import models


class Reclamation(models.Model):
    reference = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    nom = models.CharField(max_length=100)
    email = models.EmailField()

    OPERATEURS = [
        ('YAS', 'YAS'),
        ('Orange', 'Orange'),
        ('Airtel', 'Airtel'),
    ]

    operateur = models.CharField(max_length=20, choices=OPERATEURS)
    sujet = models.CharField(max_length=200)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default="En attente")

    def __str__(self):
        return self.sujet
