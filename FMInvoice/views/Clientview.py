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

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from FMInvoice.models import Client
from FMInvoice.forms import ClientForm
from django.contrib import messages

@login_required
def create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                client = form.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Vérifier si c'est une requête AJAX
                    return JsonResponse({
                        'success': True,
                        'client_id': client.id,
                        'client_name': str(client),
                    })
                messages.success(request, "Le client a été ajouté avec succès !")
                return redirect('/client')
            except ValueError as e:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': str(e),
                    }, status=400)
                messages.error(request, str(e))
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors.as_json(),
                }, status=400)
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