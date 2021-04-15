from base.forms.monetary import MonetaryField
from django import forms

from .models import Despesa, Lancamento, Receita

from datetime import datetime


class LancamentoForm(forms.ModelForm):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Lancamento
        fields = ["id", "tipo", "categorias"]
        labels = {
            "tipo": "Tipo",
            "categorias": "Categorias",
        }


class ReceitaForm(forms.ModelForm):

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
            "situacao",
        ]
        labels = {
            "tipo": "Nome",
            "valor_total": "Valor Total",
            "datahora": "Data e Hora",
            "quantidade_parcelas": "Qtde. Parcelas",
            "situacao": "Situação",
        }
        widgets = {
            "datahora": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M:%S", attrs={"type": "datetime-local"}
            ),
        }
