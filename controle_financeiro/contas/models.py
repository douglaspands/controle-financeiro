from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):

    OPCOES_PERFIL = (('C', 'Consumidor'),)

    perfil = models.CharField(max_length=1, choices=OPCOES_PERFIL, null=True)
    data_nascimento = models.DateField(null=True)
