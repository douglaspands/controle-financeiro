from django import forms

from .models import Cartao
from base.forms import MonetaryInput


class CartaoForm(forms.ModelForm):

    limite = MonetaryInput(widget=forms.TextInput(attrs={"onkeyup": "formatarMoeda(this)"}))

    class Meta:
        model = Cartao
        fields = ["nome", "limite", "dia_fechamento", "pode_parcelar"]
        label = {
            "nome": "Nome",
            "limite": "Valor Limite",
            "dia_fechamento": "Dia do Fechamento",
            "pode_parcelar": "Pode Parcelar?",
        }
