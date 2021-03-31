from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import DespesaForm
from .models import Despesa


class DespesaLista(ListView):
    model = Despesa
    template_name = 'despesas/despesa_lista.html'
    fields = ['categorias', 'descricao', 'valor', 'datahora']
    paginate_by = 25

    def get_queryset(self):
        return Despesa.objects.prefetch_related('categorias')


class DespesaDetalhe(DetailView):
    model = Despesa
    form_class = DespesaForm
    template_name = 'despesas/despesa_detalhe.html'


class DespesaCriar(CreateView):
    model = Despesa
    form_class = DespesaForm
    template_name = 'despesas/despesa_criar.html'
    success_url = reverse_lazy('despesas:lista')


class DespesaAtualizar(UpdateView):
    model = Despesa
    form_class = DespesaForm
    template_name = 'despesas/despesa_atualizar.html'
    success_url = reverse_lazy('despesas:lista')


class DespesaExcluir(DeleteView):
    model = Despesa
    form_class = DespesaForm
    template_name = 'despesas/despesa_excluir.html'
    success_url = reverse_lazy('despesas:lista')
