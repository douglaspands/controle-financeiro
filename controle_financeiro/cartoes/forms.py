from base.forms.monetary import MonetaryField
from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from .models import Cartao


class CartaoForm(forms.ModelForm):

    slug = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False)
    valor_limite = MonetaryField()

    class Meta:
        model = Cartao
        fields = ["nome", "slug", "valor_limite", "dia_fechamento", "pode_parcelar"]
        label = {
            "nome": "Nome",
            "valor_limite": "Valor Limite",
            "dia_fechamento": "Dia do Fechamento",
            "pode_parcelar": "Pode Parcelar?",
        }

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset", None)
        super().__init__(*args, **kwargs)

    def _existe_slug(self):
        if (
            self.queryset
            and self.queryset.filter(slug=self.cleaned_data["slug"]).exists()
        ):
            raise ValidationError("Já existe cartão com esse nome!")

    def clean(self):
        self.cleaned_data["slug"] = slugify(self.cleaned_data["nome"])
        if self.instance:
            if self.instance.slug != self.cleaned_data["slug"]:
                self._existe_slug()
        else:
            self._existe_slug()
