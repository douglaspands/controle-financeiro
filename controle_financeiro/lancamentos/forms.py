from django import forms
from django.forms import ModelForm

from .models import Lancamento


class LancamentoForm(ModelForm):
    class Meta:
        model = Lancamento
        fields = ["tipo"]
        # labels = {
        #     'descricao': 'Descrição',
        #     'valor': 'Valor Total da Compra',
        #     'parcelado': 'Parcelas',
        #     'carteira': 'Carteira',
        #     'datahora': 'Data e Hora',
        #     'categorias': 'Categorias'
        # }
        # widgets = {
        #     'datahora': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'})
        # }
