from carteiras.models import Carteira, CentroCusto

from .forms import ContaForm


def criar_nova_conta(form: ContaForm, carteira_slug: str, usuario_pk: int):
    """Criar nova conta.

    Args:
        form (ContaForm): Formulario da conta.
        carteira_slug (str): Slug da carteira.
        usuario_pk (int): ID do usuario.
    """
    try:
        centro_custo = CentroCusto.objects.create(
            tipo=CentroCusto.CONTA,
            carteira=Carteira.objects.get(usuario_id=usuario_pk, slug=carteira_slug),
        )
        conta = form.save(commit=False)
        conta.centro_custo = centro_custo
        conta.save()
    except Exception as error:
        centro_custo.delete()
        raise error
