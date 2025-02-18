from django.contrib import admin
from .models import (
    StationRadioDepartement,
    UtilisateurEmetteurStation,
    Client,
    Emetteur,
    CategorieEmissionService,
    Emission,
    Service,
    EmissionDateEmission,
    LigneCommande,
    Facture, DateEmission,
)

# Inline for Many-to-Many relationships in UtilisateurEmetteurStation
class StationRadioDepartementInline(admin.TabularInline):
    model = UtilisateurEmetteurStation.stations.through  # Many-to-Many intermediary table
    extra = 1  # Number of empty forms to display

# Admin for UtilisateurEmetteurStation
@admin.register(UtilisateurEmetteurStation)
class UtilisateurEmetteurStationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur',)  # Display the username in the list view
    inlines = [StationRadioDepartementInline]  # Add the inline for Many-to-Many relationships

# Inline for EmissionDateEmission in LigneCommande
class EmissionDateEmissionInline(admin.TabularInline):
    model = LigneCommande.emission_date_emission.through  # Many-to-Many intermediary table
    extra = 1  # Number of empty forms to display

# Inline for LigneCommande in Facture
class LigneCommandeInline(admin.TabularInline):
    model = Facture.lignes_commande.through  # Many-to-Many intermediary table
    extra = 1  # Number of empty forms to display

# Admin for LigneCommande
@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):
    list_display = ('service', 'prix_unitaire', 'prix_total')
    inlines = [EmissionDateEmissionInline]  # Add inline for related EmissionDateEmission

# Admin for Facture
@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'emetteur', 'client', 'date_creation', 'statut_validite', 'statut_visibilite')
    inlines = [LigneCommandeInline]  # Ajout du Inline # Add inline for related LigneCommande

@admin.register(DateEmission)
class DateEmissionAdmin(admin.ModelAdmin):
    list_display = ('date',)
    list_filter = ('date',)

# Admin for EmissionDateEmission
@admin.register(EmissionDateEmission)
class EmissionDateEmissionAdmin(admin.ModelAdmin):
    list_display = ('emission',)
    list_filter = ('date_emission',)

# Admin for Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'taille', 'categorie')
    list_filter = ('categorie',)

# Admin for Emission
@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'categorie')
    list_filter = ('categorie',)

# Admin for CategorieEmissionService
@admin.register(CategorieEmissionService)
class CategorieEmissionServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'station')
    list_filter = ('station',)

# Admin for StationRadioDepartement
@admin.register(StationRadioDepartement)
class StationRadioDepartementAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'categorie')
    list_filter = ('categorie',)

# Admin for Client
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_client', 'adresse', 'telephone', 'email', 'nif', 'registre_commerce', 'assujetti_tva')
    list_filter = ('type_client', 'assujetti_tva')

# Admin for Emetteur
@admin.register(Emetteur)
class EmetteurAdmin(admin.ModelAdmin):
    list_display = ('nom_societe', 'type_societe', 'adresse', 'telephone', 'email', 'nif', 'registre_commerce', 'assujetti_tva', 'station')
    list_filter = ('assujetti_tva', 'station')