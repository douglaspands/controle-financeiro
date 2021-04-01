from django import forms
from django.forms import ModelForm

from .models import Cartao


class CartaoForm(ModelForm):

    class Meta:
        model = Cartao
        fields = ['titulo', 'limite', 'dia_fechamento']
        labels = {
            'titulo': 'Titulo',
            'limite': 'Limite',
            'dia_fechamento': 'Dia do Fechamento',
        }
