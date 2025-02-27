from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from FMInvoice.models import CategorieEmissionService
from FMInvoice.forms import CategorieEmissionServiceForm  # You'll need to create this form

@login_required
def index(request):
    categories = CategorieEmissionService.objects.all()
    return render(
        request,
        'FMInvoice/categorie_emission_service/index.html',
        {'categories': categories}
    )

@login_required
def create(request):
    if request.method == 'POST':
        form = CategorieEmissionServiceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "La catégorie a été ajoutée avec succès !")
                return redirect('/categorie_emission_service')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = CategorieEmissionServiceForm()
    return render(
        request,
        'FMInvoice/categorie_emission_service/create.html',
        {'form': form}
    )

@login_required
def edit(request, id):
    categorie = get_object_or_404(CategorieEmissionService, pk=id)
    if request.method == 'POST':
        form = CategorieEmissionServiceForm(request.POST, instance=categorie)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "La catégorie a été modifiée avec succès !")
                return redirect('/categorie_emission_service')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer !")
    else:
        form = CategorieEmissionServiceForm(instance=categorie)
    return render(
        request,
        'FMInvoice/categorie_emission_service/edit.html',
        {'form': form, 'categorie': categorie}
    )

@login_required
def delete(request, id):
    categorie = get_object_or_404(CategorieEmissionService, pk=id)
    categorie.delete()
    messages.success(request, "La catégorie a été supprimée avec succès !")
    return redirect('/categorie_emission_service')