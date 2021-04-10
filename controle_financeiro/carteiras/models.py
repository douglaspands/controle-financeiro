from base.models import BaseModel
from pessoas.models import Pessoa
from django.db import models


class Carteira(BaseModel):

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="pessoa")

    class Meta:
        ordering = ["nome"]
        unique_together = (("pessoa_id", "slug"),)
        indexes = [
            models.Index(fields=["pessoa_id", "slug"]),
        ]

    def __str__(self):
        return f"{self.nome}"

    @property
    def tem_cartoes(self):
        return self.portas.filter(tipo=Porta.CARTAO).exists()

    @property
    def tem_contas(self):
        return self.portas.filter(tipo=Porta.CONTA).exists()


class Porta(models.Model):

    CONTA = "CONTA"
    CARTAO = "CARTAO"

    TIPOS_ESCOLHAS = [
        (CONTA, "Conta"),
        (CARTAO, "Cartão"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_ESCOLHAS)

    carteira = models.ForeignKey(
        Carteira, on_delete=models.CASCADE, related_name="portas"
    )

    @property
    def e_cartao(self) -> bool:
        return self.cartao.exists()

    @property
    def e_conta(self) -> bool:
        return self.conta.exists()
