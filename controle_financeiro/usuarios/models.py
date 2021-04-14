from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):

    GRUPO_CONSUMIDOR = "Consumidor"

    @property
    def nome_apresentacao(self) -> str:
        if self.pessoa:
            return self.pessoa.nome_apresentacao
        else:
            return self.username
