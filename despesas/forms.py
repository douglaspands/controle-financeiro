from django.forms import ModelForm
from django import forms
from .models import Despesa


class DespesaForm(ModelForm):

    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'datahora', 'categorias']
        labels = {
            'descricao': 'Descrição',
            'datahora': 'Data e Hora',
            'valor': 'Valor',
            'categorias': 'Categorias'
        }
        widgets = {
            'datahora': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
        }
