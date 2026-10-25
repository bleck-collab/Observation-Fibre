from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_dataset, name='upload_dataset'),
    path('dashboard/', views.dashboard_operateur, name='dashboard_operateur'),
    path('artec/', views.dashboard_artec, name='dashboard_artec'),
    path('chat/', views.boite_reception, name='boite_reception'),
    path('chat/<int:user_id>/', views.conversation, name='conversation'),
    path('public/', views.avis_public, name='avis_public'),
    path('sondages/', views.gerer_sondages, name='gerer_sondages'),
    path('sondages-public/', views.participer_sondages, name='participer_sondages'), # <-- Bien présente
]