from django import forms
from FMInvoice.models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'type_client': forms.Select(choices=Client.TYPE_CLIENT),
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }