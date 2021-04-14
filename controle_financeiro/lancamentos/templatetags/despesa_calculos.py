from django import template
from decimal import Decimal
from ..models import Lancamento

register = template.Library()


@register.filter(is_safe=True)
def calcular_parcela(Lancamento: Lancamento) -> Decimal:
    return Lancamento.valor_parcela
