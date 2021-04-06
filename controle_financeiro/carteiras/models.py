from base.models import BaseModel
from pessoas.models import Pessoa
from django.db import models


class Carteira(BaseModel):

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="pessoa")

    class Meta:
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.nome}"


class Porta(models.Model):

    CONTA = "CONTA"
    CARTAO = "CARTAO"

    TIPOS_ESCOLHAS = [
        (CONTA, "Conta"),
        (CARTAO, "Cartão"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_ESCOLHAS)

    carteira = models.ForeignKey(
        Carteira, on_delete=models.CASCADE, related_name="porta"
    )

    @property
    def e_cartao(self) -> bool:
        return bool(self.cartao)

    @property
    def e_conta(self) -> bool:
        return bool(self.conta)
