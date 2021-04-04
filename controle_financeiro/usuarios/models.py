from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    GRUPO_CONSUMIDOR = 'Consumidor'
    GRUPO_ESCOLHAS = [
        (GRUPO_CONSUMIDOR, 'Consumidor')
    ]
