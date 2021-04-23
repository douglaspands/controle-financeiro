from decimal import Decimal

from carteiras.models import Carteira, CentroCusto
from carteiras.usecases import (adicionar_despesa_no_centro_custo,
                                adicionar_receita_no_centro_custo)

from .forms import DespesaForm, LancamentoForm, ReceitaForm
from .models import Lancamento


def criar_nova_receita(
    lancamento_form: LancamentoForm,
    receita_form: ReceitaForm,
    carteira_slug: str,
    usuario_pk: int,
):
    """Criar nova receita.

    Args:
        lancamento_form (LancamentoForm): Formulario de Lançamento.
        receita_form (ReceitaForm): Formulario de Receita.
        carteira_slug (str): Slug da carteira.
        usuario_pk (int): ID do usuario.
    """
    try:
        lancamento = lancamento_form.save(commit=False)
        receita = receita_form.save(commit=False)
        lancamento.carteira = Carteira.objects.get(
            slug=carteira_slug, usuario_id=usuario_pk
        )
        lancamento.datahora = receita.datahora
        lancamento.save()
        receita.lancamento = lancamento
        adicionar_receita_no_centro_custo(lancamento.centro_custo, receita.valor_total)
        receita.save()
    except Exception as error:
        lancamento.delete()
        raise error


def criar_nova_despesa(
    lancamento_form: LancamentoForm,
    despesa_form: DespesaForm,
    carteira_slug: str,
    usuario_pk: int,
):
    """Criar nova receita.

    Args:
        lancamento_form (LancamentoForm): Formulario de Lançamento.
        despesa_form (DespesaForm): Formulario de Receita.
        carteira_slug (str): Slug da carteira.
        usuario_pk (int): ID do usuario.
    """
    try:
        lancamento = lancamento_form.save(commit=False)
        despesa = despesa_form.save(commit=False)
        lancamento.carteira = Carteira.objects.get(
            slug=carteira_slug, usuario_id=usuario_pk
        )
        lancamento.datahora = despesa.datahora        
        lancamento.save()
        despesa.lancamento = lancamento
        adicionar_despesa_no_centro_custo(lancamento.centro_custo, despesa.valor_total)
        despesa.save()
    except Exception as error:
        lancamento.delete()
        raise error


__all__ = (
    "criar_nova_receita",
    "criar_nova_despesa",
)
