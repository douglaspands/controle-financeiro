from datetime import datetime

from base.views import LoginRequiredBase
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import DespesaForm
from .models import Despesa


class DespesaLista(LoginRequiredBase, ListView):
    model = Despesa
    template_name = 'despesas/despesa_lista.html'
    context_object_name = 'despesas'
    fields = ['categorias', 'descricao', 'valor', 'datahora', 'carteira']
    paginate_by = 20

    def get_queryset(self):
        return Despesa.objects.prefetch_related('categorias')


class DespesaDetalhe(LoginRequiredBase, DetailView):
    model = Despesa
    template_name = 'despesas/despesa_detalhe.html'
    context_object_name = 'despesa'


class DespesaCriar(LoginRequiredBase, CreateView):
    model = Despesa
    form_class = DespesaForm
    template_name = 'despesas/despesa_criar.html'
    success_url = reverse_lazy('despesas:listar')
    context_object_name = 'despesa'

    def get_initial(self):
        initial = super(DespesaCriar, self).get_initial()
        initial.update({'parcelado': 1,
                        'datahora': datetime.now()})
        return initial


class DespesaAtualizar(LoginRequiredBase, UpdateView):
    model = Despesa
    form_class = DespesaForm
    template_name = 'despesas/despesa_atualizar.html'
    success_url = reverse_lazy('despesas:listar')
    context_object_name = 'despesa'


class DespesaExcluir(LoginRequiredBase, DeleteView):
    model = Despesa
    form_class = DespesaForm
    template_name = 'despesas/despesa_excluir.html'
    success_url = reverse_lazy('despesas:listar')
    context_object_name = 'despesa'
