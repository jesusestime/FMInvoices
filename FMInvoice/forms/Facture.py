from django import forms
from FMInvoice.models import Facture, Client, Emetteur


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['emetteur', 'client', 'mode_paiement', 'type_facture', 'devise', 'justificatif_description']

    def __init__(self, *args, **kwargs):
        emetteurs = kwargs.pop('emetteurs', None)
        super().__init__(*args, **kwargs)
        if emetteurs:
            self.fields['emetteur'].queryset = emetteurs


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'type_client', 'adresse', 'telephone', 'email', 'nif', 'registre_commerce', 'assujetti_tva']


from django import forms
from FMInvoice.models import LigneCommande, Service, EmissionDateEmission


class LigneCommandeForm(forms.ModelForm):
    class Meta:
        model = LigneCommande
        fields = ['service', 'emission_date_emission', 'prix_unitaire']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.all()
        self.fields['emission_date_emission'].queryset = EmissionDateEmission.objects.all()
        self.fields['emission_date_emission'].widget = forms.CheckboxSelectMultiple()  # Pour sélection multiple

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        prix_unitaire = cleaned_data.get('prix_unitaire')

        if prix_unitaire and prix_unitaire < 0:
            raise forms.ValidationError("Le prix unitaire ne peut pas être négatif.")

        return cleaned_data