from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # <-- Nouvel import pour la redirection
from qos_engine import views as qos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirige la racine (http://127.0.0.1:8000/) vers l'espace public
    path('', RedirectView.as_view(pattern_name='avis_public', permanent=False)),
    
    # On déplace les réclamations sous /reclamations/ pour ne pas gêner la racine
    path('reclamations/', include('reclamations.urls')), 
    
    path('qos/', include('qos_engine.urls')),
    path('login/', qos_views.connexion, name='login'),
]