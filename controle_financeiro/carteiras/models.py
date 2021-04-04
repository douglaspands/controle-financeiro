from base.models import BaseModel
from usuarios.models import Usuario
from django.db import models


class Tipo(BaseModel):

    GRUPO_CARTEIRA = 'CARTEIRA'
    GRUPO_CARTAO = 'CARTAO'

    GRUPOS_ESCOLHAS = [
        (GRUPO_CARTEIRA, 'Carteira'),
        (GRUPO_CARTAO, 'Cartão'),
    ]

    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    grupo = models.CharField(max_length=20, choices=GRUPOS_ESCOLHAS)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return f'{self.titulo}'


class Carteira(BaseModel):

    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return f'{self.titulo}'


class CarteiraMixin(models.Model):

    carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    @property
    def tipo(self) -> str:
        return self.carteira.tipo
