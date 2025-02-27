from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from FMInvoice.models import Emission
from FMInvoice.forms import EmissionForm  # You'll need to create this form

@login_required
def emission_index(request):
    emissions = Emission.objects.all()
    return render(
        request,
        'FMInvoice/emission/index.html',
        {'emissions': emissions}
    )

@login_required
def emission_create(request):
    if request.method == 'POST':
        form = EmissionForm(request.POST)
        if form.is_valid():
            try:
                emission = form.save()
                messages.success(request, "L'émission a été ajoutée avec succès !")
                return redirect('/emission')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = EmissionForm()
    return render(
        request,
        'FMInvoice/emission/create.html',
        {'form': form}
    )

@login_required
def emission_edit(request, id):
    emission = get_object_or_404(Emission, pk=id)
    if request.method == 'POST':
        form = EmissionForm(request.POST, instance=emission)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "L'émission a été modifiée avec succès !")
                return redirect('/emission')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = EmissionForm(instance=emission)
    return render(
        request,
        'FMInvoice/emission/edit.html',
        {'form': form, 'emission': emission}
    )

@login_required
def emission_delete(request, id):
    emission = get_object_or_404(Emission, pk=id)
    emission.delete()
    messages.success(request, "L'émission a été supprimée avec succès !")
    return redirect('/emission')