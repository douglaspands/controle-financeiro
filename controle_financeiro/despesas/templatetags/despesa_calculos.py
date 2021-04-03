from django import template
from decimal import Decimal
from ..models import Despesa

register = template.Library()


@register.filter(is_safe=True)
def calcular_parcela(despesa: Despesa) -> Decimal:
    return despesa.valor_parcela
