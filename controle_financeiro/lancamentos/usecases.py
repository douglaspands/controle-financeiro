from carteiras.models import Carteira

from .forms import DespesaForm, LancamentoForm, ReceitaForm


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
        lancamento.carteira = Carteira.objects.get(slug=carteira_slug, usuario_id=usuario_pk)
        lancamento.save()
        receita = receita_form.save(commit=False)
        receita.lancamento = lancamento
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
        lancamento.carteira = Carteira.objects.get(slug=carteira_slug, usuario_id=usuario_pk)
        lancamento.save()
        despesa = despesa_form.save(commit=False)
        despesa.lancamento = lancamento
        despesa.save()
    except Exception as error:
        lancamento.delete()
        raise error
