from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from FMInvoice.models import Emission, Service, UtilisateurEmetteurStation, Facture, StationRadioDepartement, \
    CategorieEmissionService


@login_required
def index(request):
    assert isinstance(request, HttpRequest)

    # Récupération des statistiques dynamiques
    total_emissions = Emission.objects.count()
    total_services = Service.objects.count()
    total_utilisateurs = UtilisateurEmetteurStation.objects.count()
    total_stations = StationRadioDepartement.objects.count()
    total_factures = Facture.objects.filter(statut_validite='Valide').count()
    total_categories = CategorieEmissionService.objects.count()

    # Contexte à passer au template
    context = {
        'total_emissions': total_emissions,
        'total_services': total_services,
        'total_utilisateurs': total_utilisateurs,
        'total_stations': total_stations,
        'total_factures': total_factures,
        'total_categories': total_categories,
        'user': request.user,
    }

    return render(request, 'FMInvoice/home/index.html', context)


# Display a view for after redirecting the new employee without is_staff or is_superuser roles
def perm_is_employee(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'FMInvoice/perm/employee.html'
    )


# Display a view for after redirecting the employee without is_superuser role
def perm_is_admin(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'FMInvoice/perm/admin.html'
    )