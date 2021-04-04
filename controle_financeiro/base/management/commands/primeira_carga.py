from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import Group
from lancamentos.models import Categoria
from carteiras.models import Tipo
from usuarios.models import Usuario


class Command(BaseCommand):

    help = 'Primeira carga em tempo de desenvolvimento.'

    def handle(self, *args, **options):

        try:
            grupo = Group(
                name=Usuario.GRUPO_CONSUMIDOR,
            )
            grupo.save()

            categoria = Categoria(titulo='Presente', slug='presente', descricao='')
            categoria.save()

            categoria = Categoria(titulo='Mercado', slug='mercado', descricao='')
            categoria.save()

            categoria = Categoria(titulo='Alimentação', slug='alimentacao', descricao='')
            categoria.save()

            categoria = Categoria(titulo='Serviços', slug='servicos', descricao='')
            categoria.save()

            tipo = Tipo(titulo='Conta', slug='conta', grupo=Tipo.GRUPO_CONTA)
            tipo.save()

            tipo = Tipo(titulo='Carteira', slug='carteira', grupo=Tipo.GRUPO_CONTA)
            tipo.save()

            tipo = Tipo(titulo='Cartão', slug='cartao', grupo=Tipo.GRUPO_CARTAO)
            tipo.save()

            tipo = Tipo(titulo='Cartão Credito', slug='cartao-credito', grupo=Tipo.GRUPO_CARTAO)
            tipo.save()

            tipo = Tipo(titulo='Cartao de Beneficio', slug='cartao-beneficio', grupo=Tipo.GRUPO_CARTAO)
            tipo.save()

        except Exception as error:
            self.stdout.write(self.style.ERROR(str(error)))
            raise CommandError('Erro ao tentar dar a primeira carga')

        self.stdout.write(self.style.SUCCESS('Primeira carga feita com sucesso.'))
