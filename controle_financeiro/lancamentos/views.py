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
    template_name = 'lancamentos/lancamento_lista.html'
    context_object_name = 'lancamentos'
    fields = ['categorias', 'descricao', 'valor', 'datahora', 'carteira']
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        params = {}
        if self.kwargs.get("cartao_slug"):
            params["porta__cartao__slug"] = self.kwargs.get("cartao_slug")

        return (
            Lancamento.objects.select_related("porta", "porta__carteira")
            .prefetch_related("cartegorias")
            .filter(**params)
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class LancamentoDetalhe(LoginRequiredBase, DetailView):
    model = Lancamento
    template_name = 'lancamentos/lancamento_detalhe.html'
    context_object_name = 'lancamento'

    def get_queryset(self):
        return Lancamento.objects.prefetch_related('categorias').filter(
            criador=self.request.user
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class LancamentoCriar(LoginRequiredBase, CreateView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = 'lancamentos/lancamento_criar.html'
    success_url = reverse_lazy('lancamentos:listar')
    context_object_name = 'lancamento'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    # def get_queryset(self):
    #     return Lancamento.objects.prefetch_related('categorias').filter(
    #         criador=self.request.user
    #     )

    # def get_initial(self):
    #     initial = super(LancamentoCriar, self).get_initial()
    #     initial.update({'parcelado': 1, 'datahora': datetime.now()})
    #     return initial

    # def post(self, request: HttpRequest) -> HttpResponse:
    #     form = LancamentoForm(request.POST)
    #     if form.is_valid():
    #         Lancamento = form.save(commit=False)
    #         Lancamento.criador = request.user
    #         Lancamento.save()
    #         return redirect('lancamentos:listar')
    #     else:
    #         return render(request, self.template_name, {'form': form})


class LancamentoAtualizar(LoginRequiredBase, UpdateView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = 'lancamentos/lancamento_atualizar.html'
    success_url = reverse_lazy('lancamentos:listar')
    context_object_name = 'lancamento'

    def get_queryset(self):
        return Lancamento.objects.prefetch_related('categorias').filter(
            criador=self.request.user
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class LancamentoExcluir(LoginRequiredBase, DeleteView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = 'lancamentos/lancamento_excluir.html'
    context_object_name = 'lancamento'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def get_success_url(self):
        params = {}
        params["carteira_slug"] = self.kwargs.get("carteira_slug")
        if self.kwargs.get("cartao_slug"):
            params["cartao_slug"] = self.kwargs.get("cartao_slug")
        return reverse_lazy(
            "gerenciamento_carteiras_cartoes_lancamentos:listar",
            kwargs=params,
        )
