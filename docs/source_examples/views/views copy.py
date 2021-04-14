from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from .forms import LancamentoForm
from .models import Lancamento, Categoria


class LancamentoLista(ListView):
    model = Lancamento
    template_name = 'lancamentos/Lancamento_lista.html'
    fields = ['categorias', 'descricao', 'valor', 'datahora']


class LancamentoDetalhe(View):

    template_name = 'lancamentos/Lancamento_detalhe.html'

    def get(self, request: HttpRequest, pk: int = None, form: LancamentoForm = None) -> HttpResponse:
        if not form:
            form_args = {}
            if pk:
                form_args['Lancamento'] = get_object_or_404(
                    Lancamento.objects.prefetch_related('Categoria'), pk=pk)
            form = LancamentoForm(**form_args)
        context = {
            'form': form,
            'categorias': Categoria.objects.all()
        }
        return render(request, self.template_name, context)


class LancamentoCriar(LancamentoDetalhe):

    template_name = 'lancamentos/Lancamento_criar.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LancamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return reverse_lazy('lancamentos:listar')
        else:
            return self.get(request, form=form)

# class LancamentoDetalhe(DetailView):
#     model = Lancamento
#     template_name = 'lancamentos/Lancamento_detalhe.html'
#     fields = ['categorias', 'descricao', 'valor', 'datahora']


# class LancamentoCriar(CreateView):
#     model = Lancamento
#     template_name = 'lancamentos/Lancamento_criar.html'
#     # fields = ['categorias', 'descricao', 'valor', 'datahora']
#     success_url = reverse_lazy('lancamentos:listar')
#     form_class = LancamentoForm


class LancamentoAtualizar(UpdateView):
    model = Lancamento
    template_name = 'lancamentos/Lancamento_atualizar.html'
    fields = ['categorias', 'descricao', 'valor', 'datahora']
    success_url = reverse_lazy('lancamentos:listar')


class LancamentoExcluir(DeleteView):
    model = Lancamento
    template_name = 'lancamentos/Lancamento_excluir.html'
    fields = ['categorias', 'descricao', 'valor', 'datahora']
    success_url = reverse_lazy('lancamentos:listar')
