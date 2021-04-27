from decimal import ROUND_DOWN, Decimal
from typing import Tuple

from carteiras.models import Carteira, CentroCusto
from carteiras.usecases import (adicionar_despesa_no_centro_custo,
                                adicionar_receita_no_centro_custo)
from dateutil.relativedelta import relativedelta

from .models import Despesa, Lancamento, Parcela, Receita


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
        centro_custo = lancamento.centro_custo
        if centro_custo.tipo == CentroCusto.TIPO_CARTAO:
            despesa.situacao = Despesa.SITUACAO_ABERTO
        elif centro_custo.tipo == CentroCusto.TIPO_CONTA:
            despesa.situacao = Despesa.SITUACAO_PAGO
        despesa.save()

        if centro_custo.tipo == CentroCusto.TIPO_CARTAO:
            cartao = centro_custo.cartao
            data_parcela = None
            valor_parcela = Decimal(despesa.valor_total /
                                    despesa.quantidade_parcelas).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            valor_primera_parcela = valor_parcela + \
                (despesa.valor_total - (valor_parcela * despesa.quantidade_parcelas))
            for ordem in range(1, despesa.quantidade_parcelas + 1):
                if data_parcela:
                    data_parcela = data_parcela + relativedelta(months=1)
                else:
                    data_parcela = despesa.datahora.date()
                    if data_parcela.day >= cartao.dia_fechamento:
                        data_parcela = data_parcela + relativedelta(months=1)
                    data_parcela = data_parcela.replace(day=cartao.dia_fechamento)
                Parcela.objects.create(
                    ordem=ordem,
                    data=data_parcela,
                    valor=valor_primera_parcela if ordem == 1 else valor_parcela,
                    situacao=Parcela.SITUACAO_ABERTO,
                    despesa=despesa
                )

        return lancamento, despesa

    except Exception as error:
        lancamento.delete()
        raise error


__all__ = (
    "criar_nova_receita",
    "criar_nova_despesa",
)
