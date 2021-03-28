from django.db import models
from django.urls import reverse


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse('detalhe', kwargs={'pk': self.pk})
