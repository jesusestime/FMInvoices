from django.forms import ModelForm
from FMInvoice.models import Service



class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'