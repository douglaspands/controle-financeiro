from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from .models import Carteira


class CarteiraForm(forms.ModelForm):

    slug = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False)

    class Meta:
        model = Carteira
        fields = ["nome", "slug"]
        labels = {
            "nome": "Nome",
        }

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset", None)
        super().__init__(*args, **kwargs)

    def _existe_slug(self):
        if (
            self.queryset
            and self.queryset.filter(slug=self.cleaned_data["slug"]).exists()
        ):
            raise ValidationError("Já existe carteira com esse nome!")

    def clean(self):
        self.cleaned_data["slug"] = slugify(self.cleaned_data["nome"])
        if self.instance:
            if self.instance.slug != self.cleaned_data["slug"]:
                self._existe_slug()
        else:
            self._existe_slug()
