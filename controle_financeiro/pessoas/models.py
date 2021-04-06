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

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="pessoa"
    )

    def __str__(self):
        return ("Fisica" if self.tipo == self.PESSOA_FISICA else "Juridica")

    @property
    def nome_apresentacao(self) -> str:
        if self.tipo == self.PESSOA_FISICA:
            return self.fisica.nome
        else:
            return self.juridica.nome_fantasia

    @property
    def e_fisica(self) -> bool:
        return bool(self.fisica)

    @property
    def e_juridica(self) -> bool:
        return bool(self.juridica)


class Fisica(BaseModel):

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)

    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, related_name="fisica")

    def __str__(self):
        return self.nome_completo

    @property
    def nome_completo(self) -> str:
        return f"{self.nome} {self.sobrenome}"


class Juridica(BaseModel):

    nome = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=100)

    pessoa = models.OneToOneField(
        Pessoa, on_delete=models.CASCADE, related_name="juridica"
    )

    def __str__(self):
        return self.nome_fantasia


class Contato(BaseModel):

    email = models.EmailField()

    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, related_name="contato")

    def __str__(self):
        return self.email


class Telefone(BaseModel):

    FIXO = "F"
    MOVEL = "M"

    TIPOS_ESCOLHAS = [(FIXO, "Telefone Fixo"), (MOVEL, "Telefone Móvel")]

    tipo = models.CharField(max_length=1, choices=TIPOS_ESCOLHAS)
    numero = models.CharField(max_length=15)

    contato = models.OneToOneField(
        Contato, on_delete=models.CASCADE, related_name="telefones"
    )

    def __str__(self):
        return self.numero
