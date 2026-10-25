
import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Reclamation
from .forms import ReclamationForm


def creer_reclamation(request):
    message = ''
    reclamation_reference = None

    if request.method == 'POST':
        form = ReclamationForm(request.POST)

        if form.is_valid():
            reclamation = form.save()
            message = 'Votre réclamation a été envoyée avec succès !'
            reclamation_reference = reclamation.reference
            form = ReclamationForm()
    else:
        form = ReclamationForm()

    return render(request, 'reclamations/formulaire.html', {
        'form': form,
        'message': message,
        'reclamation_reference': reclamation_reference,
    })


def accueil(request):
    return render(request, 'reclamations/accueil.html')


def suivre_reclamation(request):
    reclamation = None
    erreur = ''

    if request.method == 'POST':
        reference = request.POST.get('reference', '').strip()

        try:
            reference = uuid.UUID(reference)
            reclamation = Reclamation.objects.filter(
                reference=reference
            ).first()

            if reclamation is None:
                erreur = 'Aucune réclamation trouvée avec cette référence.'

        except (ValueError, AttributeError):
            erreur = 'Veuillez saisir une référence valide.'

    return render(request, 'reclamations/suivi_reclamation.html', {
        'reclamation': reclamation,
        'erreur': erreur
    })


@login_required
def tableau_bord(request):
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name='ARTEC').exists()
    ):
        return HttpResponseForbidden("Accès réservé à l'ARTEC.")

    reclamations = Reclamation.objects.all()

    return render(request, 'reclamations/tableau_bord.html', {
        'total': reclamations.count(),
        'en_attente': reclamations.filter(statut='En attente').count(),
        'en_cours': reclamations.filter(statut='En cours').count(),
        'resolues': reclamations.filter(statut='Résolue').count(),
    })


@login_required
def liste_reclamations(request):
    if (
        request.user.is_superuser
        or request.user.groups.filter(name='ARTEC').exists()
    ):
        reclamations = Reclamation.objects.all()
    else:
        groupe = request.user.groups.filter(
            name__in=['YAS', 'Orange', 'Airtel']
        ).first()

        if groupe:
            reclamations = Reclamation.objects.filter(
                operateur=groupe.name
            )
        else:
            reclamations = Reclamation.objects.none()

    recherche = request.GET.get('recherche', '').strip()

    if recherche:
        reclamations = reclamations.filter(
            Q(nom__icontains=recherche)
            | Q(sujet__icontains=recherche)
            | Q(operateur__icontains=recherche)
        )

    reclamations = reclamations.order_by('-date_creation')

    return render(request, 'reclamations/liste_reclamations.html', {
        'reclamations': reclamations,
        'recherche': recherche
    })


@login_required
def modifier_statut(request, id):
    if request.method != 'POST':
        return redirect('liste_reclamations')

    reclamation = get_object_or_404(Reclamation, id=id)

    if (
        request.user.is_superuser
        or request.user.groups.filter(name='ARTEC').exists()
    ):
        autorise = True
    else:
        groupe = request.user.groups.filter(
            name__in=['YAS', 'Orange', 'Airtel']
        ).first()

        autorise = (
            groupe is not None
            and reclamation.operateur == groupe.name
        )

    if not autorise:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à modifier cette réclamation."
        )

    nouveau_statut = request.POST.get('statut')

    if nouveau_statut in ['En attente', 'En cours', 'Résolue']:
        reclamation.statut = nouveau_statut
        reclamation.save()

    return redirect('liste_reclamations')
