import locale
from decimal import Decimal

from django import forms

locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")


class MonetaryInput(forms.CharField):
    def prepare_value(self, value):
        valor = locale.currency(value, grouping=True).replace("R$ ", "")
        return valor

    def to_python(self, value):
        valor = Decimal(value.replace(".", "").replace(",", "."))
        return valor
