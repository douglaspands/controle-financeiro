from decimal import Decimal

from carteiras.models import CentroCusto


def adicionar_receita_no_centro_custo(centro_custo: CentroCusto, valor_total: Decimal):
    """Adicionar receita ao centro de custo.

    Args:
        centro_custo (CentroCusto): Centro de custo que recebera a receita
        valor_total (Decimal): Valor da receita
    """
    if centro_custo.e_cartao:
        cartao = centro_custo.cartao
        cartao.adicionar_receita(valor_total)
        cartao.save()
    elif centro_custo.e_conta:
        conta = centro_custo.conta
        conta.adicionar_receita(valor_total)
        conta.save()
    else:
        raise Exception("Não foi identificado o tipo do centro de custo!")


def adicionar_despesa_no_centro_custo(centro_custo: CentroCusto, valor_total: Decimal):
    """Adicionar despesa ao centro de custo.

    Args:
        centro_custo (CentroCusto): Centro de custo que recebera a despesa
        valor_total (Decimal): Valor da despesa
    """
    if centro_custo.e_cartao:
        cartao = centro_custo.cartao
        cartao.adicionar_despesa(valor_total)
        cartao.save()
    elif centro_custo.e_conta:
        conta = centro_custo.conta
        conta.adicionar_despesa(valor_total)
        conta.save()
    else:
        raise Exception("Não foi identificado o tipo do centro de custo!")


__all__ = (
    "adicionar_receita_no_centro_custo",
    "adicionar_despesa_no_centro_custo"
)
