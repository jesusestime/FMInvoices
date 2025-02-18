from django.forms import ModelForm
from FMInvoice.models import StationRadioDepartement
from django import forms


class StationRadioDepartmentForm(ModelForm):
    class Meta:
        model = StationRadioDepartement
        fields = '__all__'