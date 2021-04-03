from base.models import BaseModel
from usuarios.models import Usuario
from django.db import models


class Tipo(BaseModel):
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    permite_parcelamento = models.BooleanField()

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo}"


class Carteira(BaseModel):
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo}"

    @property
    def permite_parcelamento(self) -> bool:
        return self.tipo.permite_parcelamento
