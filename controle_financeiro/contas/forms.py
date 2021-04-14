from decimal import Decimal

from base.forms.monetary import MonetaryField
from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from .models import Conta


class ContaForm(forms.ModelForm):

    slug = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False)
    saldo = MonetaryField(required=False)

    class Meta:
        model = Conta
        fields = ["nome", "slug", "saldo"]
        label = {
            "nome": "Nome",
            "saldo": "Saldo",
        }

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset", None)
        super().__init__(*args, **kwargs)

    def _existe_slug(self):
        if (
            self.queryset
            and self.queryset.filter(slug=self.cleaned_data["slug"]).exists()
        ):
            raise ValidationError("Já existe conta com esse nome!")

    def clean(self):
        self.cleaned_data["slug"] = slugify(self.cleaned_data["nome"])
        self.cleaned_data["saldo"] = self.cleaned_data["saldo"] or Decimal("0.0")
        if self.instance:
            if self.instance.slug != self.cleaned_data["slug"]:
                self._existe_slug()
        else:
            self._existe_slug()
