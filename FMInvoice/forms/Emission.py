from django.forms import ModelForm
from FMInvoice.models import Emission



class EmissionForm(ModelForm):
    class Meta:
        model = Emission
        fields = '__all__'