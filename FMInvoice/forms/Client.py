# FMInvoice/forms.py
from django import forms
from FMInvoice.models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'type_client', 'adresse', 'telephone', 'email', 'nif', 'registre_commerce', 'assujetti_tva']
        widgets = {
            'type_client': forms.Select(choices=Client.TYPE_CLIENT),
            'assujetti_tva': forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        type_client = cleaned_data.get('type_client')
        nif = cleaned_data.get('nif')
        registre_commerce = cleaned_data.get('registre_commerce')

        if type_client == 'Entreprise Locale' and (not nif or not registre_commerce):
            raise forms.ValidationError(
                "NIF et Registre de Commerce sont obligatoires pour une Entreprise Locale."
            )
        return cleaned_data