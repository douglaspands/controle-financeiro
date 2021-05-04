from carteiras.models import Carteira, CentroCusto

from .models import Conta


def criar_nova_conta(conta: Conta, carteira: Carteira) -> Conta:
    """Criar nova conta.

    Args:
        conta (Conta): Conta gerada mas não salva pelo formulario.
        carteira (Carteira): Carteira onde a conta será atrelado.

    Raises:
        Exception: - Validação dos parametros de entrada;
                   - Erro generico ao persistir no banco;

    Returns:
        Conta: Conta salva no banco.
    """
    if not (
        isinstance(conta, Conta)
        and conta.pk is None
        and isinstance(carteira, Carteira)
        and carteira.pk is not None
    ):
        raise Exception("Erro nos argumentos para criação da nova conta!")

    try:
        centro_custo = CentroCusto.objects.create(
            tipo=CentroCusto.TIPO_CONTA,
            carteira=carteira,
        )
        conta.centro_custo = centro_custo
        conta.save()
        return conta

    except Exception as error:
        centro_custo.delete()
        raise error
