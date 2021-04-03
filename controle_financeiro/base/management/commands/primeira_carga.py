from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import Group
from despesas.models import Categoria
from carteiras.models import Tipo


class Command(BaseCommand):

    help = 'Primeira carga em tempo de desenvolvimento.'

    def handle(self, *args, **options):

        try:
            grupo = Group(
                name='Consumidor',
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

            tipo = Tipo(
                titulo='Conta Bancaria', slug='conta-bancaria', permite_parcelamento=False
            )
            tipo.save()

            tipo = Tipo(titulo='Carteira', slug='carteira', permite_parcelamento=False)
            tipo.save()

            tipo = Tipo(
                titulo='Cartao de Credito', slug='cartao-credito', permite_parcelamento=True
            )
            tipo.save()

            tipo = Tipo(
                titulo='Cartao de Beneficio',
                slug='cartao-beneficio',
                permite_parcelamento=False,
            )
            tipo.save()

        except:
            raise CommandError('Erro ao tentar dar a primeira carga')

        self.stdout.write(self.style.SUCCESS('Primeira carga feita com sucesso.'))
