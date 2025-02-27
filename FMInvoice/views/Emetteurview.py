from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from FMInvoice.models import Emetteur
from FMInvoice.forms import EmetteurForm

@login_required
def emetteur_index(request):
    emetteurs = Emetteur.objects.all()
    return render(
        request,
        'FMInvoice/emetteur/index.html',
        {'emetteurs': emetteurs}
    )

@login_required
def emetteur_create(request):
    if request.method == 'POST':
        form = EmetteurForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "L'émetteur a été ajouté avec succès !")
                return redirect('/emetteur')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = EmetteurForm()
    return render(
        request,
        'FMInvoice/emetteur/create.html',
        {'form': form}
    )

@login_required
def emetteur_edit(request, id):
    emetteur = get_object_or_404(Emetteur, pk=id)
    if request.method == 'POST':
        form = EmetteurForm(request.POST, instance=emetteur)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "L'émetteur a été modifié avec succès !")
                return redirect('/emetteur')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = EmetteurForm(instance=emetteur)
    return render(
        request,
        'FMInvoice/emetteur/edit.html',
        {'form': form, 'emetteur': emetteur}
    )

@login_required
def emetteur_delete(request, id):
    emetteur = get_object_or_404(Emetteur, pk=id)
    emetteur.delete()
    messages.success(request, "L'émetteur a été supprimé avec succès !")
    return redirect('/emetteur')

@login_required
def emetteur_detail(request, id):
    emetteur = get_object_or_404(Emetteur, pk=id)
    return render(
        request,
        'FMInvoice/emetteur/detail.html',
        {'emetteur': emetteur}
    )