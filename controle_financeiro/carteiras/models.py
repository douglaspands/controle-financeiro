from base.models import BaseModel
from usuarios.models import Usuario
from django.db import models


class Carteira(BaseModel):

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="usuario"
    )

    class Meta:
        ordering = ["nome"]
        unique_together = (("usuario_id", "id"), ("usuario_id", "slug"),)
        indexes = [
            models.Index(fields=["usuario_id", "id"]),
            models.Index(fields=["usuario_id", "slug"]),
        ]

    def __str__(self):
        return f"{self.nome}"

    @property
    def tem_cartoes(self) -> bool:
        return self.centro_custos.filter(tipo=CentroCusto.CARTAO).exists()

    @property
    def tem_contas(self) -> bool:
        return self.centro_custos.filter(tipo=CentroCusto.CONTA).exists()


class CentroCusto(BaseModel):

    CONTA = "CONTA"
    CARTAO = "CARTAO"

    TIPOS_ESCOLHAS = [
        (CONTA, "Conta"),
        (CARTAO, "Cartão"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_ESCOLHAS)

    carteira = models.ForeignKey(
        Carteira, on_delete=models.CASCADE, related_name="centro_custos"
    )

    class Meta:
        unique_together = (("carteira_id", "id"),)
        indexes = [
            models.Index(fields=["carteira_id", "id"]),
        ]

    @property
    def e_cartao(self) -> bool:
        return hasattr(self, "cartao")

    @property
    def e_conta(self) -> bool:
        return hasattr(self, "conta")

    @property
    def descricao(self) -> str:
        if self.e_cartao:
            descricao = f"Cartão {str(self.cartao)}"
        elif self.e_conta:
            descricao = f"Conta {str(self.conta)}"
        else:
            descricao = "N/A"
        return descricao[:20]
