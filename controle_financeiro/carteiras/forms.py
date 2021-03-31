from django.forms import ModelForm

from .models import Carteira


class CarteiraForm(ModelForm):

    class Meta:
        model = Carteira
        fields = ['titulo', 'tipo']
        labels = {
            'titulo': 'Titulo',
            'tipo': 'Tipo'
        }
