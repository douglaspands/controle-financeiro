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

    RECEITA = "RECEITA"
    DESPESA = "DESPESA"

    TIPOS_ESCOLHAS = [
        (RECEITA, "Receita"),
        (DESPESA, "Despesa"),
    ]

    tipo = models.CharField(max_length=10, choices=TIPOS_ESCOLHAS)
    categorias = models.ManyToManyField(Categoria, blank=True)

    centro_custo = models.ForeignKey(
        CentroCusto, on_delete=models.CASCADE, related_name="lancamentos"
    )

    def __str__(self):
        return "Lançamento - {}".format(
            "Receita" if self.tipo == self.RECEITA else "Despesa"
        )

    @property
    def e_despesa(self) -> bool:
        return bool(self.despesa)

    @property
    def e_receita(self) -> bool:
        return bool(self.receita)


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
        return f"{self.nome}"


class Despesa(BaseModel):

    SITUACAO_ABERTO = "ABERTO"
    SITUACAO_PAGO = "PAGO"
    SITUACAO_CANCELADO = "CANCELADO"
    SITUACAO_ESTORNADO = "ESTORNADO"

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
    situacao = models.CharField(
        max_length=20, choices=SITUACOES_ESCOLHAS, default=SITUACAO_ABERTO
    )

    lancamento = models.OneToOneField(
        Lancamento, on_delete=models.CASCADE, related_name="despesa"
    )

    class Meta:
        ordering = ["-datahora"]

    def __str__(self):
        return f"{self.nome}"


class Parcela(BaseModel):

    SITUACAO_ABERTO = "ABERTO"
    SITUACAO_PAGO = "PAGO"
    SITUACAO_CANCELADO = "CANCELADO"
    SITUACAO_ESTORNADO = "ESTORNADO"

    SITUACOES_ESCOLHAS = [
        (SITUACAO_ABERTO, "Em Aberto"),
        (SITUACAO_PAGO, "Pago"),
        (SITUACAO_CANCELADO, "Cancelado"),
        (SITUACAO_ESTORNADO, "Estornado"),
    ]

    ordem = models.IntegerField(validators=[MinValueValidator(1)])
    data = models.DateField()
    valor = models.DecimalField(max_digits=11, decimal_places=2)
    situacao = models.CharField(
        max_length=20, choices=SITUACOES_ESCOLHAS, default=SITUACAO_ABERTO
    )

    despesa = models.OneToOneField(
        Despesa, on_delete=models.CASCADE, related_name="parcelas"
    )

    class Meta:
        ordering = ["data"]

    def __str__(self):
        return f"{self.ordem}ª parcela"
