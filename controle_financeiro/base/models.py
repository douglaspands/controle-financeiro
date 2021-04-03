from django.db import models
from django.urls import reverse


class BaseModel(models.Model):

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse('detalhar', kwargs={'pk': self.pk})
