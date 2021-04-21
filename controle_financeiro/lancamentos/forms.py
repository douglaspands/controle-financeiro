from base.forms.monetary import MonetaryField
from carteiras.models import CentroCusto
from django import forms

from .models import Despesa, Lancamento, Receita


class CentroCustoAttrs(forms.Select):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            centro_custo = value.instance
            option["attrs"].update(
                {
                    "pode-parcelar": centro_custo.pode_parcelar,
                    "e-cartao": centro_custo.e_cartao,
                    "e-conta": centro_custo.e_conta,
                }
            )
        return option


class LancamentoForm(forms.ModelForm):
    prefix = "lancamento"

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Lancamento
        fields = ["id", "tipo", "categorias", "centro_custo"]
        labels = {
            "tipo": "Tipo",
            "categorias": "Categorias",
            "centro_custo": "Centro de Custo",
        }
        widgets = {"centro_custo": CentroCustoAttrs}

    def __init__(self, *args, **kwargs):

        carteira_slug = kwargs.pop("carteira_slug", None)
        usuario_pk = kwargs.pop("usuario_pk", None)

        super().__init__(*args, **kwargs)

        self.fields["centro_custo"].queryset = CentroCusto.objects.filter(
            carteira__slug=carteira_slug,
            carteira__usuario_id=usuario_pk,
        ).all()


class ReceitaForm(forms.ModelForm):
    prefix = "receita"

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    valor_total = MonetaryField(required=True)

    class Meta:
        model = Receita
        fields = ["id", "nome", "valor_total", "datahora"]
        labels = {
            "tipo": "Nome",
            "valor_total": "Valor Total",
            "datahora": "Data e Hora",
        }
        widgets = {
            "datahora": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M:%S", attrs={"type": "datetime-local"}
            ),
        }


class DespesaForm(forms.ModelForm):
    prefix = "despesa"

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    valor_total = MonetaryField(required=True)

    class Meta:
        model = Despesa
        fields = [
            "id",
            "nome",
            "valor_total",
            "datahora",
            "quantidade_parcelas",
        ]
        labels = {
            "tipo": "Nome",
            "valor_total": "Valor Total",
            "datahora": "Data e Hora",
            "quantidade_parcelas": "Qtde. Parcelas",
        }
        widgets = {
            "datahora": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M:%S", attrs={"type": "datetime-local"}
            ),
        }
