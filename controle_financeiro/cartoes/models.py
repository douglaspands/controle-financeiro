from datetime import date, datetime

from base.models import BaseModel
from carteiras.models import CentroCusto
from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Cartao(BaseModel):

    PERMISSAO_PARCELAMENTO_POSITIVO = True
    PERMISSAO_PARCELAMENTO_NEGATIVO = False

    ESCOLHAS_PERMISSAO_PARCELAMENTO = [
        (PERMISSAO_PARCELAMENTO_POSITIVO, "Sim"),
        (PERMISSAO_PARCELAMENTO_NEGATIVO, "Não"),
    ]

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    limite = models.DecimalField(max_digits=11, decimal_places=2)
    dia_fechamento = models.IntegerField(
        default=1, validators=[MaxValueValidator(25), MinValueValidator(1)]
    )
    pode_parcelar = models.BooleanField(choices=ESCOLHAS_PERMISSAO_PARCELAMENTO)

    centro_custo = models.OneToOneField(CentroCusto, on_delete=models.CASCADE, related_name="cartao")

    class Meta:
        ordering = ["nome"]
        unique_together = (("centro_custo_id", "slug"),)
        indexes = [
            models.Index(fields=["centro_custo_id", "slug"]),
        ]

    def __str__(self):
        return f"{self.nome}"

    @property
    def proximo_fechamento(self) -> date:
        hoje = datetime.now().date()
        try:
            data_fechamento = hoje.replace(self.dia_fechamento)
        except BaseException:
            data_fechamento = (hoje + relativedelta(months=1)).replace(
                day=1
            ) - relativedelta(days=1)

        if data_fechamento < hoje:
            data_fechamento = data_fechamento + relativedelta(months=1)

        return data_fechamento

    @property
    def tem_lancamentos(self) -> bool:
        return self.centro_custo.lancamentos.exists()
