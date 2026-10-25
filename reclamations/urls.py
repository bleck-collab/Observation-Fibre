
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('reclamation/', views.creer_reclamation, name='creer_reclamation'),
    path('suivi/', views.suivre_reclamation, name='suivi_reclamation'),
    path('liste-reclamations/', views.liste_reclamations, name='liste_reclamations'),
    path('modifier-statut/<int:id>/', views.modifier_statut, name='modifier_statut'),
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='deconnexion'),
]
