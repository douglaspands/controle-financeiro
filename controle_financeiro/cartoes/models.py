from datetime import date, datetime

from base.models import BaseModel
from carteiras.models import Carteira
from usuarios.models import Usuario
from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Cartao(BaseModel):

    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    limite = models.DecimalField(max_digits=9, decimal_places=2)
    dia_fechamento = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(25),
            MinValueValidator(1)
        ]
    )
    carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE)
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return f'{self.titulo}'

    @property
    def proximo_fechamento(self) -> date:
        hoje = datetime.now().date()
        try:
            data_fechamento = hoje.replace(self.dia_fechamento)
        except BaseException:
            data_fechamento = (hoje + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)

        if data_fechamento < hoje:
            data_fechamento = data_fechamento + relativedelta(months=1)

        return data_fechamento
