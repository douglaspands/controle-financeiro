from django import forms
from django.forms import ModelForm

from .models import Despesa


class DespesaForm(ModelForm):

    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'parcelado', 'carteira', 'datahora', 'categorias']
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor',
            'Qtde Parcelas': 'parcelado',
            'carteira': 'Carteira',
            'datahora': 'Data e Hora',
            'categorias': 'Categorias'
        }
        widgets = {
            'datahora': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'})
        }
