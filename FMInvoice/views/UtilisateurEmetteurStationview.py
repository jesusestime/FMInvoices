from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from FMInvoice.models import UtilisateurEmetteurStation
from FMInvoice.forms import UtilisateurEmetteurStationForm

@login_required
def index(request):
    utilisateurs_emetteurs = UtilisateurEmetteurStation.objects.all()
    return render(
        request,
        'FMInvoice/utilisateur_emetteur_station/index.html',
        {'utilisateurs_emetteurs': utilisateurs_emetteurs}
    )

@login_required
def create(request):
    if request.method == 'POST':
        form = UtilisateurEmetteurStationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'utilisateur émetteur a été ajouté avec succès !")
            return redirect('/utilisateur_emetteur_station')
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = UtilisateurEmetteurStationForm()
    return render(
        request,
        'FMInvoice/utilisateur_emetteur_station/create.html',
        {'form': form}
    )

@login_required
def edit(request, id):
    utilisateur_emetteur = get_object_or_404(UtilisateurEmetteurStation, pk=id)
    if request.method == 'POST':
        form = UtilisateurEmetteurStationForm(request.POST, instance=utilisateur_emetteur)
        if form.is_valid():
            form.save()
            messages.success(request, "L'utilisateur émetteur a été modifié avec succès !")
            return redirect('/utilisateur_emetteur_station')
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = UtilisateurEmetteurStationForm(instance=utilisateur_emetteur)
    return render(
        request,
        'FMInvoice/utilisateur_emetteur_station/edit.html',
        {'form': form, 'utilisateur_emetteur': utilisateur_emetteur}
    )

@login_required
def delete(request, id):
    utilisateur_emetteur = get_object_or_404(UtilisateurEmetteurStation, pk=id)
    utilisateur_emetteur.delete()
    messages.success(request, "L'utilisateur émetteur a été supprimé avec succès !")
    return redirect('/utilisateur_emetteur_station')
