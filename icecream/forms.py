from django.forms import ModelForm
from icecream.models import Flavour

class FlavourForm(ModelForm):
    class Meta:
        model = Flavour
