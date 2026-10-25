from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Avg, Q
from django.contrib.auth.models import User
from .models import Dataset, QoSMetric, SanctionRecompense, Message, AvisPublic, Sondage, ReponseSondage
from .services import traiter_dataset

@login_required
def upload_dataset(request):
    operateur = None
    if request.user.groups.filter(name='YAS').exists(): operateur = 'YAS'
    elif request.user.groups.filter(name='Orange').exists(): operateur = 'Orange'
    elif request.user.groups.filter(name='Airtel').exists(): operateur = 'Airtel'

    if not operateur and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux opérateurs.")
        return redirect('avis_public') # Modifié ici

    if request.method == 'POST':
        fichier = request.FILES.get('fichier')
        if fichier:
            dataset = Dataset.objects.create(operateur=operateur, fichier=fichier)
            messages.info(request, "Fichier reçu. L'IA analyse vos données...")
            succes, msg = traiter_dataset(dataset)
            if succes:
                messages.success(request, msg)
            else:
                messages.error(request, msg)
            return redirect('upload_dataset')

    datasets = Dataset.objects.filter(operateur=operateur).order_by('-date_upload') if operateur else Dataset.objects.all()
    return render(request, 'qos_engine/upload.html', {'datasets': datasets, 'operateur': operateur})


@login_required
def dashboard_operateur(request):
    operateur = None
    if request.user.groups.filter(name='YAS').exists(): operateur = 'YAS'
    elif request.user.groups.filter(name='Orange').exists(): operateur = 'Orange'
    elif request.user.groups.filter(name='Airtel').exists(): operateur = 'Airtel'

    if not operateur:
        messages.error(request, "Accès réservé aux opérateurs.")
        return redirect('avis_public') # Modifié ici

    stats_qos = QoSMetric.objects.filter(dataset__operateur=operateur).aggregate(moyenne=Avg('score_qos'))
    score_moyen = stats_qos['moyenne'] or 0
    sanctions = SanctionRecompense.objects.filter(operateur=operateur, type_alerte='sanction').count()
    felicitations = SanctionRecompense.objects.filter(operateur=operateur, type_alerte='felicitation').count()
    alertes_recentes = SanctionRecompense.objects.filter(operateur=operateur).order_by('-date_creation')[:10]

    context = {
        'operateur': operateur,
        'score_moyen': round(score_moyen, 2),
        'sanctions': sanctions,
        'felicitations': felicitations,
        'alertes': alertes_recentes
    }
    return render(request, 'qos_engine/dashboard.html', context)


@login_required
def dashboard_artec(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='ARTEC').exists()):
        messages.error(request, "Accès strictement réservé à l'ARTEC.")
        return redirect('avis_public') # Modifié ici

    operateurs = ['YAS', 'Orange', 'Airtel']
    stats_operateurs = []

    for op in operateurs:
        moy = QoSMetric.objects.filter(dataset__operateur=op).aggregate(moyenne=Avg('score_qos'))['moyenne']
        score_moyen = round(moy, 2) if moy else 0
        sanctions = SanctionRecompense.objects.filter(operateur=op, type_alerte='sanction').count()
        felicitations = SanctionRecompense.objects.filter(operateur=op, type_alerte='felicitation').count()

        stats_operateurs.append({
            'nom': op,
            'score_moyen': score_moyen,
            'sanctions': sanctions,
            'felicitations': felicitations,
        })

    dernieres_alertes = SanctionRecompense.objects.all().order_by('-date_creation')[:15]

    context = {
        'stats_operateurs': stats_operateurs,
        'dernieres_alertes': dernieres_alertes,
    }
    return render(request, 'qos_engine/dashboard_artec.html', context)


@login_required
def boite_reception(request):
    is_artec = request.user.is_superuser or request.user.groups.filter(name='ARTEC').exists()
    
    if is_artec:
        contacts = User.objects.filter(groups__name__in=['YAS', 'Orange', 'Airtel']).distinct()
    else:
        contacts = User.objects.filter(Q(groups__name='ARTEC') | Q(is_superuser=True)).distinct()

    messages_recus = Message.objects.filter(destinataire=request.user).order_by('-date_envoi')[:5]
    
    context = {
        'contacts': contacts,
        'messages_recus': messages_recus,
        'is_artec': is_artec
    }
    return render(request, 'qos_engine/chat_inbox.html', context)


@login_required
def conversation(request, user_id):
    autre_utilisateur = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            Message.objects.create(
                expediteur=request.user,
                destinataire=autre_utilisateur,
                contenu=contenu
            )
            return redirect('conversation', user_id=user_id)

    historique = Message.objects.filter(
        (Q(expediteur=request.user) & Q(destinataire=autre_utilisateur)) |
        (Q(expediteur=autre_utilisateur) & Q(destinataire=request.user))
    ).order_by('date_envoi')

    Message.objects.filter(expediteur=autre_utilisateur, destinataire=request.user, lu=False).update(lu=True)

    context = {
        'autre_utilisateur': autre_utilisateur,
        'historique': historique
    }
    return render(request, 'qos_engine/chat_conversation.html', context)


def avis_public(request):
    stats = []
    for op in ['YAS', 'Orange', 'Airtel']:
        moyenne = AvisPublic.objects.filter(operateur=op).aggregate(Avg('note'))['note__avg']
        total = AvisPublic.objects.filter(operateur=op).count()
        
        stats.append({
            'operateur': op,
            'moyenne': round(moyenne, 1) if moyenne else 0,
            'total': total
        })

    if request.method == 'POST':
        operateur = request.POST.get('operateur')
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        telephone = request.POST.get('telephone')

        if operateur and note:
            AvisPublic.objects.create(
                operateur=operateur,
                note=int(note),
                commentaire=commentaire,
                telephone=telephone
            )
            messages.success(request, "Merci ! Votre avis a bien été enregistré et pris en compte par l'ARTEC.")
            return redirect('avis_public')

    derniers_avis = AvisPublic.objects.all().order_by('-date_creation')[:10]

    context = {
        'stats': stats,
        'derniers_avis': derniers_avis
    }
    return render(request, 'qos_engine/avis_public.html', context)


@login_required
def gerer_sondages(request):
    is_artec = request.user.is_superuser or request.user.groups.filter(name='ARTEC').exists()
    
    operateur_nom = None
    if request.user.groups.filter(name='YAS').exists(): operateur_nom = 'YAS'
    elif request.user.groups.filter(name='Orange').exists(): operateur_nom = 'Orange'
    elif request.user.groups.filter(name='Airtel').exists(): operateur_nom = 'Airtel'

    if not is_artec and not operateur_nom:
        messages.error(request, "Accès non autorisé.")
        return redirect('avis_public') # Modifié ici

    if request.method == 'POST':
        titre = request.POST.get('titre')
        question = request.POST.get('question')
        
        if titre and question:
            if is_artec:
                Sondage.objects.create(titre=titre, question=question, createur_type='ARTEC')
            else:
                Sondage.objects.create(titre=titre, question=question, createur_type='OPERATEUR', operateur_cible=operateur_nom)
            
            messages.success(request, "Sondage créé avec succès !")
            return redirect('gerer_sondages')

    if is_artec:
        sondages = Sondage.objects.all().order_by('-date_creation')
    else:
        sondages = Sondage.objects.filter(createur_type='OPERATEUR', operateur_cible=operateur_nom).order_by('-date_creation')

    context = {
        'sondages': sondages,
        'is_artec': is_artec,
        'operateur_nom': operateur_nom
    }
    return render(request, 'qos_engine/gerer_sondages.html', context)


def participer_sondages(request):
    sondages_actifs = Sondage.objects.filter(est_actif=True).order_by('-date_creation')

    if request.method == 'POST':
        sondage_id = request.POST.get('sondage_id')
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')

        if sondage_id and note:
            sondage = Sondage.objects.get(id=sondage_id)
            ReponseSondage.objects.create(
                sondage=sondage,
                note=int(note),
                commentaire=commentaire
            )
            messages.success(request, "Merci ! Votre réponse a bien été enregistrée.")
            return redirect('participer_sondages')

    context = {
        'sondages': sondages_actifs
    }
    return render(request, 'qos_engine/participer_sondages.html', context)


def connexion(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name='ARTEC').exists():
            return redirect('dashboard_artec')
        else:
            return redirect('dashboard_operateur')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser or user.groups.filter(name='ARTEC').exists():
                return redirect('dashboard_artec')
            elif user.groups.filter(name__in=['YAS', 'Orange', 'Airtel']).exists():
                return redirect('dashboard_operateur')
            else:
                return redirect('avis_public')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'qos_engine/login.html')