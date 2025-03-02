from django.utils import timezone

from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


# Modèle Station Radio Département
class StationRadioDepartement(models.Model):
    code = models.CharField(max_length=50,editable=False, unique=True, verbose_name=_("Code Station Département"))
    nom = models.CharField(max_length=255, verbose_name=_("Nom Station Département"))
    CATEGORIES = [
        ('TV', 'TV'),
        ('Radio', 'Radio'),
    ]
    categorie = models.CharField(max_length=10, choices=CATEGORIES, verbose_name=_("Catégorie"))

    def save(self, *args, **kwargs):
        if not self.code:
            count = StationRadioDepartement.objects.count() + 1
            self.code = f"Sta{count}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nom


# Modèle Utilisateur Émetteur Station
class UtilisateurEmetteurStation(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Utilisateur"))
    stations = models.ManyToManyField(StationRadioDepartement, verbose_name=_("Stations où il travaille"))

    def __str__(self):
        return self.utilisateur.username


# Modèle Client
class Client(models.Model):
    TYPE_CLIENT = [
        ('Individuel', 'Individuel'),
        ('Entreprise Locale', 'Entreprise Locale'),
        ('Entreprise Étrangère', 'Entreprise Étrangère'),
    ]
    nom = models.CharField(max_length=255, verbose_name=_("Nom Client ou Société"))
    type_client = models.CharField(max_length=20, choices=TYPE_CLIENT, verbose_name=_("Type Client"))
    adresse = models.CharField(max_length=255, verbose_name=_("Adresse Client ou Société"))
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Téléphone"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))
    nif = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("NIF"))
    registre_commerce = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Registre de Commerce"))
    assujetti_tva = models.BooleanField(default=False, verbose_name=_("Assujetti à la TVA"))

    def save(self, *args, **kwargs):
        # Validation conditionnelle pour les champs NIF et Registre de Commerce
        if self.type_client == 'Entreprise Locale':
            if not self.nif or not self.registre_commerce:
                raise ValueError(_("NIF et Registre de Commerce sont obligatoires pour une Entreprise Locale"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


# Modèle Emetteur
class Emetteur(models.Model):
    nom_societe = models.CharField(max_length=255, verbose_name=_("Nom Société"))
    type_societe = models.CharField(max_length=255, verbose_name=_("Type Société"))
    adresse = models.CharField(max_length=255, verbose_name=_("Adresse Société"))
    telephone = models.CharField(max_length=20, verbose_name=_("Téléphone"))
    email = models.EmailField(verbose_name=_("Email"))
    nif = models.CharField(max_length=50, verbose_name=_("NIF"))
    registre_commerce = models.CharField(max_length=50, verbose_name=_("Registre de Commerce"))
    assujetti_tva = models.BooleanField(default=False, verbose_name=_("Assujetti à la TVA"))
    station = models.ForeignKey(StationRadioDepartement, on_delete=models.CASCADE, verbose_name=_("Station Radio Département"))

    def __str__(self):
        return self.nom_societe


# Modèle Catégorie Emission/Service
class CategorieEmissionService(models.Model):
    code = models.CharField(max_length=50,editable=False, unique=True, verbose_name=_("Code Catégorie"))
    nom = models.CharField(max_length=255, verbose_name=_("Nom Catégorie"))
    station = models.ForeignKey(StationRadioDepartement, on_delete=models.CASCADE, verbose_name=_("Station Radio Département"))

    def save(self, *args, **kwargs):
        if not self.code:
            count = CategorieEmissionService.objects.count() + 1
            self.code = f"CaEm{count}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nom


class Emission(models.Model):
    code = models.CharField(max_length=50, editable=False, unique=True, verbose_name=_("Code Émission"))
    nom = models.CharField(max_length=255, verbose_name=_("Nom Émission"))
    categories = models.ManyToManyField(CategorieEmissionService, verbose_name=_("Catégories Emission/Service"))

    def save(self, *args, **kwargs):
        if not self.code:
            count = Emission.objects.count() + 1
            self.code = f"Emi{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} - {', '.join([cat.nom for cat in self.categories.all()])}"


# Modèle Service
class Service(models.Model):
    code = models.CharField(editable=False, max_length=50, unique=True, verbose_name=_("Code Service"))
    nom = models.CharField(max_length=255, verbose_name=_("Nom Service"))
    taille = models.PositiveIntegerField(default=1, verbose_name=_("Unité(sec, mention, visit)"))
    categorie = models.ManyToManyField('CategorieEmissionService', verbose_name=_("Catégorie Emission/Service"))

    def save(self, *args, **kwargs):
        if not self.code:
            count = Service.objects.count() + 1
            self.code = f"Ser{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.taille})"

class DateEmission(models.Model):
    date = models.DateField(verbose_name=_("Date de l'émission"))

    def __str__(self):
        return str(self.date)

# Table intermédiaire Emission_DateEmission
class EmissionDateEmission(models.Model):
    emission = models.ForeignKey(Emission, on_delete=models.CASCADE, verbose_name=_("Émission"))
    date_emission =  models.ManyToManyField('DateEmission', verbose_name=_("Dates de l'émission"))

    def __str__(self):
        dates_str = ", ".join(str(date.date) for date in self.date_emission.all())
        return f"{self.emission.nom} - {dates_str}" if dates_str else self.emission.nom


# Modèle Ligne Commande
class LigneCommande(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_("Service"))
    emission_date_emission = models.ManyToManyField(EmissionDateEmission, verbose_name=_("Émission/Date Émission"))
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix Unitaire"))
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix Total"), null=True,editable=False)

    def calcul_nombre_emissions(self):
        """Calculer le nombre total de dates d'émission associées à ce service"""
        nombre_emissions = 0
        for emission_date in self.emission_date_emission.all():
            nombre_emissions += emission_date.date_emission.count()
        return nombre_emissions

    def calcul_prix_total(self):
        """Calculer le prix total en fonction du nombre de jours et de la taille du service"""
        nombre_jours = self.calcul_nombre_emissions()
        return self.prix_unitaire * nombre_jours * self.service.taille

    def __str__(self):
        # Vérifier si la taille est égale à 1 et afficher un trait si c'est le cas
        taille = self.service.taille if self.service.taille != 1 else "-"

        # Récupérer les noms des émissions associées
        emissions = ", ".join(str(emission) for emission in self.emission_date_emission.all()) or "Aucune émission"

        return f"{self.service.nom} ({taille}) - {self.prix_total} ({emissions})"


# Modèle Facture
class Facture(models.Model):
    STATUT_VALIDITE = [
        ('Annulée', 'Annulée'),
        ('Valide', 'Valide'),
    ]
    STATUT_VISIBILITE = [
        ('Oui', 'Oui'),
        ('Non', 'Non'),
    ]
    MODE_PAIEMENT = [
        ('Cash', 'Cash'),
        ('Banque', 'Banque'),
        ('Crédits', 'Crédits'),
        ('Monnaie Électronique', 'Monnaie Électronique'),
        ('Autre', 'Autre'),
    ]
    TYPE_FACTURE = [
        ('Proforma', 'Proforma'),
        ('Payée', 'Payée'),
        ('En Cours', 'En Cours'),
    ]
    DEVISES = [
        ('BIF', 'BIF'),
        ('Dollars', 'Dollars'),
        ('Euro', 'Euro'),
        ('Autre', 'Autre'),
    ]


    numero = models.CharField(max_length=50, unique=True, verbose_name=_("Numéro Facture"), editable=False)
    emetteur = models.ForeignKey(Emetteur, on_delete=models.CASCADE, verbose_name=_("Émetteur"))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_("Client"))
    date_creation = models.DateTimeField(default=now, verbose_name=_("Date de Création"))
    date_mise_a_jour = models.DateTimeField(auto_now=True, verbose_name=_("Date de Mise à Jour"))
    statut_validite = models.CharField(max_length=10, choices=STATUT_VALIDITE, default='Valide', verbose_name=_("Statut Validité"))
    statut_visibilite = models.CharField(max_length=3, choices=STATUT_VISIBILITE, default='Oui', verbose_name=_("Statut Visibilité"))
    emetteur_createur = models.ForeignKey(UtilisateurEmetteurStation, on_delete=models.CASCADE, verbose_name=_("Émetteur Créateur"))
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT, verbose_name=_("Mode de Paiement"))
    type_facture = models.CharField(max_length=20, choices=TYPE_FACTURE, verbose_name=_("Type Facture"))
    devise = models.CharField(max_length=20, choices=DEVISES, verbose_name=_("Devise"))
    lignes_commande = models.ManyToManyField(LigneCommande, verbose_name=_("Lignes de Commande"))
    justificatif_description = models.TextField(blank=True, null=True,verbose_name=_("Justificatif/Description de la Facture"))

    def get_montant_total(self):
        """Calcule le montant total de toutes les lignes de commande."""
        return sum(ligne.prix_total or 0 for ligne in self.lignes_commande.all())
    def save(self, *args, **kwargs):
        # Vérifier si c'est une nouvelle facture (pas de numéro défini)
        if not self.numero:
            year = timezone.now().strftime('%y')  # Année sur 2 chiffres
            # Utiliser une transaction pour éviter les doublons en cas d'accès concurrent
            with transaction.atomic():
                # Compter les factures existantes et incrémenter
                count = Facture.objects.count() + 1
                self.numero = f"BMG-{count:03d}/{year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero

    class Meta:
        verbose_name = _("Facture")
        verbose_name_plural = _("Factures")