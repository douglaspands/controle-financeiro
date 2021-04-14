from carteiras.models import Carteira, CentroCusto

from .forms import CartaoForm


def criar_novo_cartao(form: CartaoForm, carteira_slug: str, usuario_pk: int):
    """Criar novo cartão.

    Args:
        form (CartaoForm): Formulario do cartão.
        carteira_slug (str): Slug da carteira.
        usuario_pk (int): ID do usuario.
    """
    try:
        centro_custo = CentroCusto.objects.create(
            tipo=CentroCusto.CARTAO,
            carteira=Carteira.objects.get(usuario_id=usuario_pk, slug=carteira_slug),
        )
        cartao = form.save(commit=False)
        cartao.centro_custo = centro_custo
        cartao.save()
    except Exception as error:
        centro_custo.delete()
        raise error
