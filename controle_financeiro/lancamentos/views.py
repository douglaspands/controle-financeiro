from datetime import datetime

from base.views import LoginRequiredBase
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import LancamentoForm
from .models import Lancamento


class LancamentoLista(LoginRequiredBase, ListView):
    model = Lancamento
    template_name = 'lancamentos/Lancamento_lista.html'
    context_object_name = 'lancamentos'
    fields = ['categorias', 'descricao', 'valor', 'datahora', 'carteira']
    paginate_by = 20

    def get_queryset(self):
        return Lancamento.objects.prefetch_related('categorias').filter(
            criador=self.request.user
        )


class LancamentoDetalhe(LoginRequiredBase, DetailView):
    model = Lancamento
    template_name = 'lancamentos/Lancamento_detalhe.html'
    context_object_name = 'Lancamento'

    def get_queryset(self):
        return Lancamento.objects.prefetch_related('categorias').filter(
            criador=self.request.user
        )


class LancamentoCriar(LoginRequiredBase, CreateView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = 'lancamentos/Lancamento_criar.html'
    success_url = reverse_lazy('lancamentos:listar')
    context_object_name = 'Lancamento'

    def get_queryset(self):
        return Lancamento.objects.prefetch_related('categorias').filter(
            criador=self.request.user
        )

    def get_initial(self):
        initial = super(LancamentoCriar, self).get_initial()
        initial.update({'parcelado': 1, 'datahora': datetime.now()})
        return initial

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LancamentoForm(request.POST)
        if form.is_valid():
            Lancamento = form.save(commit=False)
            Lancamento.criador = request.user
            Lancamento.save()
            return redirect('lancamentos:listar')
        else:
            return render(request, self.template_name, {'form': form})


class LancamentoAtualizar(LoginRequiredBase, UpdateView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = 'lancamentos/Lancamento_atualizar.html'
    success_url = reverse_lazy('lancamentos:listar')
    context_object_name = 'Lancamento'

    def get_queryset(self):
        return Lancamento.objects.prefetch_related('categorias').filter(
            criador=self.request.user
        )


class LancamentoExcluir(LoginRequiredBase, DeleteView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = 'lancamentos/Lancamento_excluir.html'
    success_url = reverse_lazy('lancamentos:listar')
    context_object_name = 'Lancamento'

    def get_queryset(self):
        return Lancamento.objects.prefetch_related('categorias').filter(
            criador=self.request.user
        )
