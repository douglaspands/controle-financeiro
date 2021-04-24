from base.forms.monetary import MonetaryField
from django import forms
from django.core.exceptions import ValidationError

from .models import Despesa, Lancamento, Receita
from carteiras.models import CentroCusto


class LancamentoForm(forms.ModelForm):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    centro_custo_id = forms.ChoiceField(
        widget=forms.Select, required=True, initial=None, label="Fonte"
    )

    class Meta:
        model = Lancamento
        fields = ["id", "tipo", "categorias", "centro_custo_id"]
        labels = {
            "tipo": "Tipo",
            "categorias": "Categorias",
        }

    def __init__(self, *args, **kwargs):

        carteira_slug = kwargs.pop("carteira_slug", None)
        usuario_pk = kwargs.pop("usuario_pk", None)
        centro_custo_pk = kwargs.pop("centro_custo_pk", None)

        super().__init__(*args, **kwargs)

        choices = [(None, "---------")]
        for tipo_id, tipo_desc in sorted(CentroCusto.TIPOS_ESCOLHAS):
            choice = (
                tipo_desc,
                [
                    (cc.pk, cc.descricao)
                    for cc in CentroCusto.objects.filter(
                        carteira__slug=carteira_slug,
                        carteira__usuario_id=usuario_pk,
                        tipo=tipo_id,
                    ).all()
                ],
            )
            if len(choice[1]) > 0:
                choices.append(choice)

        self.fields["centro_custo_id"].initial = centro_custo_pk
        self.fields["centro_custo_id"].label = "Fonte"
        self.fields["centro_custo_id"].choices = choices

    # def clean_centro_custo_id(self):
    #     if not self.cleaned_data["centro_custo_id"] or not self.cleaned_data["centro_custo_id"].isdigit():
    #         raise ValidationError("Favor selecione uma opção valida!")
    #     self.cleaned_data["centro_custo_id"] = int(self.cleaned_data["centro_custo_id"])

    def clean(self):
        self.cleaned_data["centro_custo_id"] = int(self.cleaned_data["centro_custo_id"])


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
