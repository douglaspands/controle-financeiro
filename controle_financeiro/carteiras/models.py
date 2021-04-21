from base.models import BaseModel
from django.db import models
from usuarios.models import Usuario


class Carteira(BaseModel):

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="usuario"
    )

    class Meta:
        ordering = ["nome"]
        unique_together = (
            ("usuario_id", "id"),
            ("usuario_id", "slug"),
        )
        indexes = [
            models.Index(fields=["usuario_id", "id"]),
            models.Index(fields=["usuario_id", "slug"]),
        ]

    def __str__(self):
        return f"{self.nome}"

    @property
    def tem_centro_custos(self) -> bool:
        return self.centro_custos.exists()

    @property
    def tem_cartoes(self) -> bool:
        return self.centro_custos.filter(tipo=CentroCusto.CARTAO).exists()

    @property
    def tem_contas(self) -> bool:
        return self.centro_custos.filter(tipo=CentroCusto.CONTA).exists()

    @property
    def tem_lancamentos(self) -> bool:
        return self.centro_custos.exclude(lancamentos__isnull=True).exists()


class CentroCusto(BaseModel):

    CONTA = 1
    CARTAO = 2

    TIPOS_ESCOLHAS = [
        (CONTA, "Conta"),
        (CARTAO, "Cartão"),
    ]

    tipo = models.IntegerField(choices=TIPOS_ESCOLHAS)

    carteira = models.ForeignKey(
        Carteira, on_delete=models.CASCADE, related_name="centro_custos"
    )

    class Meta:
        unique_together = (("carteira_id", "id"),)
        indexes = [
            models.Index(fields=["carteira_id", "id"]),
        ]

    def __str__(self) -> str:
        return self.descricao

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
        return descricao

    @property
    def tem_lancamentos(self) -> bool:
        return self.lancamentos.exists()

    @property
    def pode_parcelar(self) -> bool:
        if self.e_cartao:
            pode_parcelar = self.cartao.pode_parcelar
        else:
            pode_parcelar = False
        return pode_parcelar
