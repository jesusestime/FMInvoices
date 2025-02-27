from django.forms import ModelForm
from FMInvoice.models import UtilisateurEmetteurStation
from django import forms


class UtilisateurEmetteurStationForm(ModelForm):
    class Meta:
        model = UtilisateurEmetteurStation
        fields = '__all__'