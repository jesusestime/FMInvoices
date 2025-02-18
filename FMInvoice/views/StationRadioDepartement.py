from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from FMInvoice.models import StationRadioDepartement
from FMInvoice.forms import StationRadioDepartmentForm

@login_required
def index(request):
    station_radio_departements = StationRadioDepartement.objects.all()
    return render(
        request,
        'FMInvoice/station_radio_departement/index.html',  # Correct template path
        {
            'station_radio_departements': station_radio_departements
        }
    )

@login_required
def create(request):
    if request.method == 'POST':
        form = StationRadioDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La station radio département a été sauvegardée avec succès !")
            return redirect('/station_radio_departement')  # Correct redirect URL
        else:
            messages.error(request, 'Une erreur s\'est produite. Veuillez réessayer !')
            return render(request, 'FMInvoice/station_radio_departement/create.html', {'form': form}) # Render form with errors
    else:  # For GET requests, render the empty form
        form = StationRadioDepartmentForm()
    return render(
        request,
        'FMInvoice/station_radio_departement/create.html', # Correct template path
        {
            'form': form
        }
    )

@login_required
def edit(request, id):
    try:
        station_radio_departement = StationRadioDepartement.objects.get(pk=id)
    except StationRadioDepartement.DoesNotExist:
        messages.error(request, "Station radio département non trouvée.")
        return redirect('/station_radio_departement')

    if request.method == 'POST':
        form = StationRadioDepartmentForm(request.POST, instance=station_radio_departement)
        if form.is_valid():
            form.save()
            messages.success(request, "La station radio département a été modifiée avec succès !")
            return redirect('/station_radio_departement') # Correct redirect URL
        else:
             messages.error(request, 'Une erreur s\'est produite. Veuillez réessayer !')
             return render(request, 'FMInvoice/station_radio_departement/edit.html', {'form': form, 'station_radio_departement': station_radio_departement}) # Render form with errors
    else:  # GET request
        form = StationRadioDepartmentForm(instance=station_radio_departement)
    return render(
        request,
        'FMInvoice/station_radio_departement/edit.html', # Correct template path
        {
            'form': form,
            'station_radio_departement': station_radio_departement # Pass the object to the template
        }
    )


@login_required
def delete(request, id):
    try:
        station_radio_departement = StationRadioDepartement.objects.get(pk=id)
        station_radio_departement.delete()
        messages.success(request, "La station radio département a été supprimée avec succès !")
    except StationRadioDepartement.DoesNotExist:
        messages.error(request, "Station radio département non trouvée.")

    return redirect('/station_radio_departement') # Correct redirect URL