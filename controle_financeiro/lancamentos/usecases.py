from typing import Tuple

from carteiras.models import Carteira
from carteiras.usecases import (
    adicionar_despesa_no_centro_custo,
    adicionar_receita_no_centro_custo,
)

from .models import Despesa, Lancamento, Receita


def criar_nova_receita(
    lancamento: Lancamento, receita: Receita, carteira: Carteira
) -> Tuple[Lancamento, Receita]:
    if not (
        isinstance(lancamento, Lancamento)
        and lancamento.pk is None
        and isinstance(receita, Receita)
        and receita.pk is None
        and isinstance(carteira, Carteira)
        and carteira.pk is not None
    ):
        raise Exception("Erro nos argumentos para criação da nova receita!")

    try:
        lancamento.carteira = carteira
        lancamento.datahora = receita.datahora
        lancamento.save()
        receita.lancamento = lancamento
        adicionar_receita_no_centro_custo(
            centro_custo=lancamento.centro_custo, valor_total=receita.valor_total
        )
        receita.save()
        return lancamento, receita

    except Exception as error:
        lancamento.delete()
        raise error


def criar_nova_despesa(
    lancamento: Lancamento, despesa: Despesa, carteira: Carteira
) -> Tuple[Lancamento, Despesa]:
    if not (
        isinstance(lancamento, Lancamento)
        and lancamento.pk is None
        and isinstance(despesa, Despesa)
        and despesa.pk is None
        and isinstance(carteira, Carteira)
        and carteira.pk is not None
    ):
        raise Exception("Erro nos argumentos para criação da nova despesa!")

    try:
        lancamento.carteira = carteira
        lancamento.datahora = despesa.datahora
        lancamento.save()
        despesa.lancamento = lancamento
        adicionar_despesa_no_centro_custo(
            centro_custo=lancamento.centro_custo, valor_total=despesa.valor_total
        )
        despesa.save()
        return lancamento, despesa

    except Exception as error:
        lancamento.delete()
        raise error


__all__ = (
    "criar_nova_receita",
    "criar_nova_despesa",
)
