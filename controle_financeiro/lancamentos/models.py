from base.models import BaseModel
from carteiras.models import Porta
from django.core.validators import MinValueValidator
from django.db import models


class Lancamento(BaseModel):

    RECEITA = "RECEITA"
    DESPESA = "DESPESA"

    TIPOS_ESCOLHAS = [
        (RECEITA, "Receita"),
        (DESPESA, "Despesa"),
    ]

    tipo = models.CharField(max_length=10, choices=TIPOS_ESCOLHAS)

    porta = models.ForeignKey(
        Porta, on_delete=models.CASCADE, related_name="lancamentos"
    )

    def __str__(self):
        return "Lançamento - {}".format('Receita' if self.tipo == self.RECEITA else 'Despesa')


class Receita(BaseModel):

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    valor_total = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    datahora = models.DateTimeField()

    lancamento = models.ForeignKey(
        Lancamento, on_delete=models.CASCADE, related_name="receita"
    )

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
    slug = models.SlugField(max_length=100, unique=True)
    valor_total = models.DecimalField(max_digits=11, decimal_places=2)
    datahora = models.DateTimeField()
    parcelas = models.IntegerField(default=1)
    encerrado = models.BooleanField(default=False)
    situacao = models.CharField(
        max_length=20, choices=SITUACOES_ESCOLHAS, default=SITUACAO_ABERTO
    )

    lancamento = models.ForeignKey(
        Lancamento, on_delete=models.CASCADE, related_name="despesa"
    )

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

    despesa = models.ForeignKey(
        Despesa, on_delete=models.CASCADE, related_name="parcelas"
    )

    class Meta:
        ordering = ["data"]
        indexes = [
            models.Index(fields=["data"]),
            models.Index(fields=["ordem"]),
        ]

    def __str__(self):
        numero_ordinal = f"{self.ordem}" + ("º" if self.ordem == 1 else "ª")
        return f"{numero_ordinal} parcela"
