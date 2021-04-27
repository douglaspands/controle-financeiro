from django import template

from ..models import Despesa, Parcela

register = template.Library()


@register.filter(is_safe=True)
def descricao_situacao_despesa(situacao: int) -> str:
    descricao = [s[1] for s in Despesa.SITUACOES_ESCOLHAS if s[0] == situacao]
    return descricao[0] if len(descricao) > 0 else "N/D"


@register.filter(is_safe=True)
def descricao_situacao_parcela(situacao: int) -> str:
    descricao = [s[1] for s in Parcela.SITUACOES_ESCOLHAS if s[0] == situacao]
    return descricao[0] if len(descricao) > 0 else "N/D"
