from base.models import BaseModel
from carteiras.models import Porta
from django.db import models


class Conta(BaseModel):

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    saldo = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    porta = models.OneToOneField(Porta, on_delete=models.CASCADE, related_name="conta")

    class Meta:
        ordering = ['nome']
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f'{self.nome}'
