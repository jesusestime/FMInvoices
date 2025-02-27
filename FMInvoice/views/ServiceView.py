from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from FMInvoice.models import Service
from FMInvoice.forms import ServiceForm  # You'll need to create this form

@login_required
def service_index(request):
    services = Service.objects.all()
    return render(
        request,
        'FMInvoice/service/index.html',
        {'services': services}
    )

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            try:
                service = form.save()
                messages.success(request, "Le service a été ajouté avec succès !")
                return redirect('/service')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = ServiceForm()
    return render(
        request,
        'FMInvoice/service/create.html',
        {'form': form}
    )

@login_required
def service_edit(request, id):
    service = get_object_or_404(Service, pk=id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Le service a été modifié avec succès !")
                return redirect('/service')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = ServiceForm(instance=service)
    return render(
        request,
        'FMInvoice/service/edit.html',
        {'form': form, 'service': service}
    )

@login_required
def service_delete(request, id):
    service = get_object_or_404(Service, pk=id)
    service.delete()
    messages.success(request, "Le service a été supprimé avec succès !")
    return redirect('/service')