from django.db import models
from base.models import BaseModel


class Categoria(BaseModel):

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField()

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return f'{self.titulo}'


class Despesa(BaseModel):

    categorias = models.ManyToManyField(Categoria, blank=True)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    datahora = models.DateTimeField()

    class Meta:
        ordering = ['-datahora']

    def __str__(self):
        return f'{self.descricao}'
