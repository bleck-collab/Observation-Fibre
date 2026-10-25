from django.contrib import admin
from .models import Dataset, QoSMetric, SanctionRecompense, Message, AvisPublic, Sondage, ReponseSondage

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('operateur', 'fichier', 'date_upload', 'traite')
    list_filter = ('operateur', 'traite')

@admin.register(QoSMetric)
class QoSMetricAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'score_qos', 'interpretation', 'date_prediction')
    list_filter = ('interpretation',)

@admin.register(SanctionRecompense)
class SanctionRecompenseAdmin(admin.ModelAdmin):
    list_display = ('operateur', 'type_alerte', 'score_qos', 'date_creation')
    list_filter = ('type_alerte', 'operateur')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'destinataire', 'contenu', 'date_envoi', 'lu')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('contenu', 'expediteur__username', 'destinataire__username')

@admin.register(AvisPublic)
class AvisPublicAdmin(admin.ModelAdmin):
    list_display = ('operateur', 'note', 'telephone', 'date_creation')
    list_filter = ('operateur', 'note')
    search_fields = ('commentaire', 'telephone')

@admin.register(Sondage)
class SondageAdmin(admin.ModelAdmin):
    list_display = ('titre', 'createur_type', 'operateur_cible', 'est_actif', 'date_creation')
    list_filter = ('createur_type', 'est_actif')

@admin.register(ReponseSondage)
class ReponseSondageAdmin(admin.ModelAdmin):
    list_display = ('sondage', 'note', 'date_reponse')
    list_filter = ('note', 'date_reponse')