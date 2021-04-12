from django import forms

from .models import Cartao
from base.forms.monetary import MonetaryField


class CartaoForm(forms.ModelForm):

    limite = MonetaryField()

    class Meta:
        model = Cartao
        fields = ["nome", "limite", "dia_fechamento", "pode_parcelar"]
        label = {
            "nome": "Nome",
            "limite": "Valor Limite",
            "dia_fechamento": "Dia do Fechamento",
            "pode_parcelar": "Pode Parcelar?",
        }
