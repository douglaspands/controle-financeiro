from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from .forms import DespesaForm
from .models import Despesa, Categoria


class DespesaLista(ListView):
    model = Despesa
    template_name = 'despesas/despesa_lista.html'
    fields = ['categorias', 'descricao', 'valor', 'datahora']


class DespesaDetalhe(View):

    template_name = 'despesas/despesa_detalhe.html'

    def get(self, request: HttpRequest, pk: int = None, form: DespesaForm = None) -> HttpResponse:
        if not form:
            form_args = {}
            if pk:
                form_args['despesa'] = get_object_or_404(
                    Despesa.objects.prefetch_related('Categoria'), pk=pk)
            form = DespesaForm(**form_args)
        context = {
            'form': form,
            'categorias': Categoria.objects.all()
        }
        return render(request, self.template_name, context)


class DespesaCriar(DespesaDetalhe):

    template_name = 'despesas/despesa_criar.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return reverse_lazy('despesas:listar')
        else:
            return self.get(request, form=form)

# class DespesaDetalhe(DetailView):
#     model = Despesa
#     template_name = 'despesas/despesa_detalhe.html'
#     fields = ['categorias', 'descricao', 'valor', 'datahora']


# class DespesaCriar(CreateView):
#     model = Despesa
#     template_name = 'despesas/despesa_criar.html'
#     # fields = ['categorias', 'descricao', 'valor', 'datahora']
#     success_url = reverse_lazy('despesas:listar')
#     form_class = DespesaForm


class DespesaAtualizar(UpdateView):
    model = Despesa
    template_name = 'despesas/despesa_atualizar.html'
    fields = ['categorias', 'descricao', 'valor', 'datahora']
    success_url = reverse_lazy('despesas:listar')


class DespesaExcluir(DeleteView):
    model = Despesa
    template_name = 'despesas/despesa_excluir.html'
    fields = ['categorias', 'descricao', 'valor', 'datahora']
    success_url = reverse_lazy('despesas:listar')
