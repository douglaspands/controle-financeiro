from decimal import Decimal

from base.models import BaseModel
from carteiras.models import CentroCusto
from django.core.validators import MinValueValidator
from django.db import models


class Categoria(BaseModel):

    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    descricao = models.TextField()

    class Meta:
        ordering = ["slug"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.titulo}"


class Lancamento(BaseModel):

    TIPO_RECEITA = 1
    TIPO_DESPESA = 2

    TIPOS_ESCOLHAS = [
        (TIPO_RECEITA, "Receita"),
        (TIPO_DESPESA, "Despesa"),
    ]

    tipo = models.IntegerField(choices=TIPOS_ESCOLHAS)
    categorias = models.ManyToManyField(Categoria, blank=True)
    datahora = models.DateTimeField()

    centro_custo = models.ForeignKey(
        CentroCusto, on_delete=models.CASCADE, related_name="lancamentos"
    )

    class Meta:
        ordering = ["-datahora"]

    def __str__(self):
        tipo_desc = "Receita" if self.tipo == Lancamento.TIPO_RECEITA else "Despesa"
        return f"{self.pk} - {tipo_desc} (Centro de custo {self.centro_custo.pk})"

    @property
    def e_despesa(self) -> bool:
        return hasattr(self, "despesa")

    @property
    def e_receita(self) -> bool:
        return hasattr(self, "receita")

    @property
    def descricao(self) -> str:
        if self.e_despesa:
            descricao = f"Despesa {self.despesa.nome}"
        elif self.e_receita:
            descricao = f"Receita {self.receita.nome}"
        else:
            descricao = "N/A"
        return descricao

    @property
    def valor(self) -> Decimal:
        if self.e_despesa:
            valor = self.despesa.valor_total * -1
        elif self.e_receita:
            valor = self.receita.valor_total
        else:
            valor = Decimal("0.0")
        return valor


class Receita(BaseModel):

    nome = models.CharField(max_length=100)
    valor_total = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    datahora = models.DateTimeField()

    lancamento = models.OneToOneField(
        Lancamento, on_delete=models.CASCADE, related_name="receita"
    )

    class Meta:
        ordering = ["-datahora"]

    def __str__(self):
        return f"{self.pk} - {self.nome} (Lancamento {self.lancamento.pk})"


class Despesa(BaseModel):

    SITUACAO_ABERTO = 1
    SITUACAO_PAGO = 2
    SITUACAO_CANCELADO = 3
    SITUACAO_ESTORNADO = 4

    SITUACOES_ESCOLHAS = [
        (SITUACAO_ABERTO, "Em Aberto"),
        (SITUACAO_PAGO, "Pago"),
        (SITUACAO_CANCELADO, "Cancelado"),
        (SITUACAO_ESTORNADO, "Estornado"),
    ]

    nome = models.CharField(max_length=100)
    valor_total = models.DecimalField(max_digits=11, decimal_places=2)
    datahora = models.DateTimeField()
    quantidade_parcelas = models.IntegerField(default=1)
    situacao = models.IntegerField(
        choices=SITUACOES_ESCOLHAS, default=SITUACAO_ABERTO
    )

    lancamento = models.OneToOneField(
        Lancamento, on_delete=models.CASCADE, related_name="despesa"
    )

    class Meta:
        ordering = ["-datahora"]

    def __str__(self):
        return f"{self.pk} - {self.nome} (Lancamento {self.lancamento.pk})"


class Parcela(BaseModel):

    SITUACAO_ABERTO = 1
    SITUACAO_PAGO = 2
    SITUACAO_CANCELADO = 3
    SITUACAO_ESTORNADO = 4

    SITUACOES_ESCOLHAS = [
        (SITUACAO_ABERTO, "Em Aberto"),
        (SITUACAO_PAGO, "Pago"),
        (SITUACAO_CANCELADO, "Cancelado"),
        (SITUACAO_ESTORNADO, "Estornado"),
    ]

    ordem = models.IntegerField(validators=[MinValueValidator(1)])
    data = models.DateField()
    valor = models.DecimalField(max_digits=11, decimal_places=2)
    situacao = models.IntegerField(choices=SITUACOES_ESCOLHAS, default=SITUACAO_ABERTO)

    despesa = models.ForeignKey(
        Despesa, on_delete=models.CASCADE, related_name="parcelas"
    )

    class Meta:
        ordering = ["data"]

    def __str__(self):
        return f"{self.pk} - {self.ordem}ª parcela (Despesa: {self.despesa.pk})"
