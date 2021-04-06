from django.forms import ModelForm

from .models import Carteira


class CarteiraForm(ModelForm):

    class Meta:
        model = Carteira
        fields = ['nome']
        labels = {
            'nome': 'Nome',
        }
