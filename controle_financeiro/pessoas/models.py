from django.db import models
from base.models import BaseModel
from usuarios.models import Usuario


class Pessoa(BaseModel):

    PESSOA_FISICA = "F"
    PESSOA_JURIDICA = "J"

    TIPOS_ESCOLHAS = [
        (PESSOA_FISICA, "Pessoa Fisica"),
        (PESSOA_JURIDICA, "Pessoa Juridica"),
    ]

    tipo = models.CharField(max_length=1, choices=TIPOS_ESCOLHAS)

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="pessoa"
    )

    @property
    def nome_apresentacao(self) -> str:
        if self.tipo == self.PESSOA_FISICA:
            return self.fisica.nome
        else:
            return self.juridica.nome_fantasia


class Fisica(BaseModel):

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)

    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="fisica")

    @property
    def nome_completo(self) -> str:
        return f"{self.nome} {self.sobrenome}"


class Juridica(BaseModel):

    nome = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=100)

    pessoa = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE, related_name="juridica"
    )


class Contato(BaseModel):

    email = models.EmailField()

    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="contato")


class Telefone(BaseModel):

    FIXO = "F"
    MOVEL = "M"

    TIPOS_ESCOLHAS = [(FIXO, "Telefone Fixo"), (MOVEL, "Telefone Móvel")]

    tipo = models.CharField(max_length=1, choices=TIPOS_ESCOLHAS)

    numero = models.CharField(max_length=15)

    contato = models.ForeignKey(
        Contato, on_delete=models.CASCADE, related_name="telefones"
    )
