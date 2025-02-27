from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from FMInvoice.models import Client
from FMInvoice.forms import ClientForm  # You'll need to create this form

@login_required
def index(request):
    clients = Client.objects.all()
    return render(
        request,
        'FMInvoice/client/index.html',
        {'clients': clients}
    )

@login_required
def create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Le client a été ajouté avec succès !")
                return redirect('/client')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = ClientForm()
    return render(
        request,
        'FMInvoice/client/create.html',
        {'form': form}
    )

@login_required
def edit(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Le client a été modifié avec succès !")
                return redirect('/client')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = ClientForm(instance=client)
    return render(
        request,
        'FMInvoice/client/edit.html',
        {'form': form, 'client': client}
    )

@login_required
def delete(request, id):
    client = get_object_or_404(Client, pk=id)
    client.delete()
    messages.success(request, "Le client a été supprimé avec succès !")
    return redirect('/client')


@login_required
def client_detail(request, id):
    client = get_object_or_404(Client, pk=id)
    return render(
        request,
        'FMInvoice/client/detail.html',
        {'client': client}
    )