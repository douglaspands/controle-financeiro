from django.forms import ModelForm
from django import forms
from .models import Despesa


class DespesaForm(ModelForm):

    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'datahora', 'categorias']
        labels = {
            'descricao': 'Descrição',
            'datahora': 'Data e Hora',
            'valor': 'Valor',
            'categorias': 'Categorias'
        }
        widgets = {
            'datahora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # def __init__(self, *args, **kwargs):
    #     despesa = kwargs.pop('despesa', None)
    #     super(DespesaForm, self).__init__(*args, **kwargs)
    #     if isinstance(despesa, Despesa):
    #         for key in self._meta.fields:
    #             if hasattr(self.despesa, key):
    #                 self.fields[key].initial = getattr(self.despesa, key)
