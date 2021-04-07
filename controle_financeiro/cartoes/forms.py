from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from .models import Cartao


class CartaoForm(forms.ModelForm):

    class Meta:
        model = Cartao
        fields = ["nome", "limite", "dia_fechamento", "pode_parcelar"]
        label = {
            "nome": "Nome",
            "limite": "Valor Limite",
            "dia_fechamento": "Dia do Fechamento",
            "pode_parcelar": "Pode Parcelar?",
        }


# class CartaoForm(forms.Form):

#     titulo = forms.CharField(
#         max_length=100,
#         label=_("Nome do cartão"),
#         required=True,
#     )

#     limite = forms.DecimalField(
#         max_digits=9,
#         decimal_places=2,
#         label=_("Valor limite"),
#         required=True,
#     )

#     dia_fechamento = forms.IntegerField(
#         validators=[
#             MinValueValidator(1),
#             MaxValueValidator(25),
#         ],
#         label=_("Dia do fechamento"),
#         required=True,
#     )

#     pode_parcelar = forms.ChoiceField(
#         widget=forms.RadioSelect,
#         choices=Cartao.ESCOLHAS_PERMISSAO_PARCELAMENTO,
#         label=_("Pode parcelar?"),
#         required=True,
#     )
