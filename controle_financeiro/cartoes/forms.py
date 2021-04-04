from carteiras.models import Tipo
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from .models import Cartao


class CartaoForm(forms.Form):

    titulo = forms.CharField(
        max_length=100,
        label=_('Nome do cartão'),
        required=True,
    )

    limite = forms.DecimalField(
        max_digits=9,
        decimal_places=2,
        label=_('Valor limite'),
        required=True,
    )

    dia_fechamento = forms.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(25),
        ],
        label=_('Dia do fechamento'),
        required=True,
    )

    pode_parcelar = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=Cartao.ESCOLHAS_PERMISSAO_PARCELAMENTO,
        label=_('Pode parcelar?'),
        required=True,
    )

    tipo = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[(tipo.pk, tipo.titulo) for tipo in Tipo.objects.filter(grupo=Tipo.GRUPO_CARTAO).all()],
        label=_('Tipo de cartão'),
        required=True,
    )
