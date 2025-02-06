from django.contrib import admin
from .models import (
    Facture,
    CommandeService,
    Client,
    Service,
    Emission,
    ServiceEmission,
)

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero_facture', 'type_facture', 'statut_validite', 'statut_visibilite', 'devise', 'date_creation', 'date_mise_a_jour')
    list_filter = ('statut_validite', 'statut_visibilite', 'type_facture', 'devise')
    search_fields = ('numero_facture',)
    date_hierarchy = 'date_creation'


class CommandeServiceInline(admin.TabularInline):
    model = CommandeService
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'taille', 'prix_unitaire', 'categorie')
    list_filter = ('categorie',)
    search_fields = ('nom', 'code')
    inlines = [CommandeServiceInline]  # Inline utilisé ici pour les commandes


class ServiceEmissionInline(admin.TabularInline):
    model = ServiceEmission
    extra = 1


@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'categorie')
    list_filter = ('categorie',)
    search_fields = ('nom', 'code')
    inlines = [ServiceEmissionInline]  # Inline utilisé ici pour les services


@admin.register(ServiceEmission)
class ServiceEmissionAdmin(admin.ModelAdmin):
    list_display = ('service', 'emission', 'date_emission')
    list_filter = ('date_emission',)
    search_fields = ('service__nom', 'emission__nom')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_client', 'adresse', 'telephone', 'email', 'nif', 'registre_commerce', 'assujetti_tva')
    list_filter = ('type_client', 'assujetti_tva')
    search_fields = ('nom', 'email', 'telephone')
