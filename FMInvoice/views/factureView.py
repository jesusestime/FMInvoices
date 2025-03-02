from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from FMInvoice.models import Facture, LigneCommande, Client, Emetteur, Service, EmissionDateEmission, \
    UtilisateurEmetteurStation, DateEmission, Emission
from FMInvoice.forms import FactureForm, ClientForm


@login_required
def creer_facture(request):
    utilisateur_emetteur = UtilisateurEmetteurStation.objects.get(utilisateur=request.user)
    emetteurs_disponibles = Emetteur.objects.filter(station__in=utilisateur_emetteur.stations.all())

    if request.method == 'POST':
        facture_form = FactureForm(request.POST, emetteurs=emetteurs_disponibles)
        client_form = ClientForm(request.POST, prefix='client')

        print("POST data:", request.POST)
        print("Lignes de commande:", request.POST.getlist('lignes_commande[]'))

        if facture_form.is_valid():
            with transaction.atomic():
                if 'new_client' in request.POST and client_form.is_valid():
                    client = client_form.save()
                else:
                    client = facture_form.cleaned_data['client']

                facture = facture_form.save(commit=False)
                facture.emetteur_createur = utilisateur_emetteur
                facture.client = client
                facture.save()

                lignes_data = request.POST.getlist('lignes_commande[]')
                for ligne in lignes_data:
                    try:
                        print(f"Traitement de la ligne: {ligne}")
                        parts = ligne.split(';')
                        print(f"Parts (avant ajustement): {parts}")
                        if len(parts) < 3:
                            raise ValueError(f"Format invalide pour la ligne: {ligne}")

                        service_id = parts[0]
                        emissions_str = ';'.join(parts[1:-1])  # Tout sauf service_id et prix_unitaire
                        prix_unitaire = float(parts[-1].strip())

                        print(f"service_id: {service_id}, emissions_str: {emissions_str}, prix_unitaire: {prix_unitaire}")

                        service = Service.objects.get(id=service_id)
                        ligne_commande = LigneCommande.objects.create(
                            service=service,
                            prix_unitaire=prix_unitaire,
                            prix_total=prix_unitaire * service.taille
                        )

                        emission_date_pairs = emissions_str.split(';')
                        total_dates = 0
                        for pair in emission_date_pairs:
                            emission_id, dates_str = pair.split(':', 1)
                            emission = Emission.objects.get(id=emission_id)
                            dates = [datetime.strptime(d.strip(), '%Y-%m-%d').date() for d in dates_str.split(',')]
                            total_dates += len(dates)

                            date_emissions = [DateEmission.objects.get_or_create(date=d)[0] for d in dates]
                            emission_date = EmissionDateEmission.objects.create(emission=emission)
                            emission_date.date_emission.set(date_emissions)
                            ligne_commande.emission_date_emission.add(emission_date)

                        ligne_commande.prix_total = prix_unitaire * total_dates * service.taille
                        ligne_commande.save()

                        facture.lignes_commande.add(ligne_commande)
                    except (ValueError, IndexError) as e:
                        print(f"Erreur dans le traitement de la ligne: {ligne} - {e}")
                        raise

                return redirect('facture_detail', id=facture.id)
    else:
        facture_form = FactureForm(emetteurs=emetteurs_disponibles)
        client_form = ClientForm(prefix='client')

    return render(request, 'FMInvoice/facture/creer_facture.html', {
        'facture_form': facture_form,
        'client_form': client_form,
        'services': Service.objects.all(),
        'emissions': Emission.objects.all(),
    })
@login_required
def facture_detail(request, id):
    facture = get_object_or_404(Facture, id=id)
    lignes_commande = facture.lignes_commande.all()

    return render(request, 'FMInvoice/facture/facture_detail.html', {
        'facture': facture,
        'lignes_commande': lignes_commande,
    })








from django.db import transaction
from datetime import datetime

@login_required
def facture_list(request):
    factures = Facture.objects.all().order_by('-date_creation').annotate(
        montant_total=Sum('lignes_commande__prix_total')
    )
    return render(request, 'FMInvoice/facture/facture_list.html', {
        'factures': factures,
    })

@login_required
def facture_edit(request, id):
    facture = get_object_or_404(Facture, id=id)
    utilisateur_emetteur = UtilisateurEmetteurStation.objects.get(utilisateur=request.user)
    emetteurs_disponibles = Emetteur.objects.filter(station__in=utilisateur_emetteur.stations.all())

    if request.method == 'POST':
        facture_form = FactureForm(request.POST, instance=facture, emetteurs=emetteurs_disponibles)
        if facture_form.is_valid():
            with transaction.atomic():
                facture = facture_form.save(commit=False)
                facture.emetteur_createur = utilisateur_emetteur
                facture.save()

                # Gestion des lignes de commande
                facture.lignes_commande.clear()  # Supprimer les anciennes lignes
                lignes_data = request.POST.getlist('lignes_commande[]')
                for ligne in lignes_data:
                    try:
                        parts = ligne.split(';')
                        if len(parts) < 3:
                            raise ValueError(f"Format invalide pour la ligne: {ligne}")

                        service_id = parts[0]
                        emissions_str = ';'.join(parts[1:-1])
                        prix_unitaire_str = parts[-1].strip().replace(',', '.')  # Remplacer la virgule par un point
                        prix_unitaire = float(prix_unitaire_str)  # Conversion en float

                        service = Service.objects.get(id=service_id)
                        ligne_commande = LigneCommande.objects.create(
                            service=service,
                            prix_unitaire=prix_unitaire,
                            prix_total=prix_unitaire * service.taille
                        )

                        emission_date_pairs = emissions_str.split(';')
                        total_dates = 0
                        for pair in emission_date_pairs:
                            emission_id, dates_str = pair.split(':', 1)
                            emission = Emission.objects.get(id=emission_id)
                            dates = [datetime.strptime(d.strip(), '%Y-%m-%d').date() for d in dates_str.split(',')]
                            total_dates += len(dates)

                            date_emissions = [DateEmission.objects.get_or_create(date=d)[0] for d in dates]
                            emission_date = EmissionDateEmission.objects.create(emission=emission)
                            emission_date.date_emission.set(date_emissions)
                            ligne_commande.emission_date_emission.add(emission_date)

                        ligne_commande.prix_total = prix_unitaire * total_dates * service.taille
                        ligne_commande.save()

                        facture.lignes_commande.add(ligne_commande)
                    except (ValueError, IndexError) as e:
                        print(f"Erreur dans le traitement de la ligne: {ligne} - {e}")
                        raise

                return redirect('facture_detail', id=facture.id)
    else:
        facture_form = FactureForm(instance=facture, emetteurs=emetteurs_disponibles)

    return render(request, 'FMInvoice/facture/facture_edit.html', {
        'facture_form': facture_form,
        'facture': facture,
        'services': Service.objects.all(),
        'emissions': Emission.objects.all(),
    })