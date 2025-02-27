from django import forms
from FMInvoice.models import Emetteur

class EmetteurForm(forms.ModelForm):
    class Meta:
        model = Emetteur
        fields = '__all__'