from carteiras.models import Carteira, CentroCusto

from .models import Cartao


def criar_novo_cartao(cartao: Cartao, carteira: Carteira) -> Cartao:
    """Criar novo cartão.

    Args:
        cartao (Cartao): Cartão gerado mas não salvo pelo formulario.
        carteira (Carteira): Carteira onde o cartão será atrelado.

    Raises:
        Exception: - Validação dos parametros de entrada;
                   - Erro generico ao persistir no banco;

    Returns:
        Cartao: Cartão salva no banco.
    """
    if not (
        isinstance(cartao, Cartao)
        and cartao.pk is None
        and isinstance(carteira, Carteira)
        and carteira.pk is not None
    ):
        raise Exception("Erro nos argumentos para criação do novo cartão!")

    try:
        centro_custo = CentroCusto.objects.create(
            tipo=CentroCusto.TIPO_CARTAO,
            carteira=carteira,
        )
        cartao.centro_custo = centro_custo
        cartao.save()
        return cartao

    except Exception as error:
        centro_custo.delete()
        raise error
