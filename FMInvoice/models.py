from django.db import models
from django.contrib.auth.models import User


class Facture(models.Model):
    numero_facture = models.CharField(max_length=100, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    emetteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='factures')
    devise = models.CharField(max_length=10, choices=[('BIF', 'BIF'), ('USD', 'Dollars'), ('EUR', 'Euro')])

    def __str__(self):
        return f"Facture {self.numero_facture}"


class Emission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=255)
    categorie = models.CharField(max_length=50, choices=[('Radio', 'Radio'), ('TV', 'TV')])

    def __str__(self):
        return self.nom


class Service(models.Model):
    code = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=255)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    taille = models.PositiveIntegerField()  # Taille en secondes
    categorie = models.CharField(max_length=50, choices=[('Radio', 'Radio'), ('TV', 'TV')])

    def __str__(self):
        return self.nom


class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    emissions = models.ManyToManyField(Emission, through='EmissionLigneFacture')

    def __str__(self):
        return f"Ligne Facture {self.id} - {self.service.nom}"


class EmissionLigneFacture(models.Model):
    ligne_facture = models.ForeignKey(LigneFacture, on_delete=models.CASCADE)
    emission = models.ForeignKey(Emission, on_delete=models.CASCADE)
    date_emission = models.DateField()

    def __str__(self):
        return f"{self.emission.nom} ({self.date_emission}) - Ligne {self.ligne_facture.id}"
