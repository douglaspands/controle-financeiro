from decimal import Decimal

from base.models import BaseModel
from carteiras.models import Carteira
from django.db import models


class Categoria(BaseModel):

    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
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
    parcelado = models.IntegerField(default=1)
    carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-datahora']

    def __str__(self):
        return f'{self.descricao}'

    @property
    def tem_parcelas(self) -> bool:
        return self.carteira.permite_parcelamento

    @property
    def valor_parcela(self) -> Decimal:
        return self.valor / self.parcelado
