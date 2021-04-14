from base.models import BaseModel
from carteiras.models import CentroCusto
from django.db import models


class Conta(BaseModel):

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    saldo = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    centro_custo = models.OneToOneField(CentroCusto, on_delete=models.CASCADE, related_name="conta")

    class Meta:
        ordering = ['nome']
        unique_together = (("centro_custo_id", "slug"),)
        indexes = [
            models.Index(fields=["centro_custo_id", "slug"]),
        ]

    def __str__(self):
        return f'{self.nome}'
