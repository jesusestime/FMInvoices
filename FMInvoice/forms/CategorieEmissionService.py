from django.forms import ModelForm
from FMInvoice.models import CategorieEmissionService



class CategorieEmissionServiceForm(ModelForm):
    class Meta:
        model = CategorieEmissionService
        fields = '__all__'