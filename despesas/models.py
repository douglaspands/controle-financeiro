from django.db import models
from base.models import BaseModel


class Categoria(BaseModel):

    slug = models.SlugField(max_length=200)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()

    def __str__(self):
        return f'{self.pk} - {self.titulo}'


class Despesa(BaseModel):

    categorias = models.ManyToManyField(Categoria, blank=True)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    datahora = models.DateTimeField()

    def __str__(self):
        return f'{self.pk} - {self.descricao[:20]}'
