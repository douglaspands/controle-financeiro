from django.core.management.base import BaseCommand, CommandError

from lancamentos.models import Categoria


class Command(BaseCommand):

    help = "Carga da base de categorias."

    def handle(self, *args, **options):

        try:
            Categoria.objects.create(titulo="Alimentação", slug="alimentacao", descricao="Gastos com alimentação.")
            Categoria.objects.create(titulo="Mercado", slug="mercado", descricao="Gastos com mercado.")
            Categoria.objects.create(titulo="Presente", slug="presente", descricao="Gastos com presente.")
            Categoria.objects.create(titulo="Serviços", slug="servicos", descricao="Gastos com serviços.")

        except Exception as error:
            self.stdout.write(self.style.ERROR(str(error)))
            raise CommandError("Erro ao tentar dar a primeira carga")

        self.stdout.write(self.style.SUCCESS("Primeira carga feita com sucesso."))
