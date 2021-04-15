from datetime import datetime

from base.views import LoginRequiredBase
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import DespesaForm, LancamentoForm, ReceitaForm
from .models import Lancamento


class LancamentoLista(LoginRequiredBase, ListView):
    model = Lancamento
    template_name = "lancamentos/lancamento_lista.html"
    context_object_name = "lancamentos"
    fields = ["categorias", "descricao", "valor", "datahora", "carteira"]
    paginate_by = settings.REGISTROS_POR_PAGINA

    def get_queryset(self, *args, **kwargs):
        params = {}
        if self.kwargs.get("cartao_slug"):
            params["centro_custo__cartao__slug"] = self.kwargs.get("cartao_slug")

        return (
            Lancamento.objects.select_related("centro_custo", "centro_custo__carteira")
            .prefetch_related("cartegorias")
            .filter(**params)
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class LancamentoDetalhe(LoginRequiredBase, DetailView):
    model = Lancamento
    template_name = "lancamentos/lancamento_detalhe.html"
    context_object_name = "lancamento"

    def get_queryset(self):
        return Lancamento.objects.prefetch_related("categorias").filter(
            criador=self.request.user
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class LancamentoCriar(LoginRequiredBase, View):
    template_name = "lancamentos/lancamento_criar.html"

    def get_success_url(self):
        return reverse_lazy(
            "gerenciamento_carteiras_lancamentos:listar",
            kwargs={"carteira_slug": self.kwargs.get("carteira_slug")},
        )

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = {
            "lancamento_form": LancamentoForm(prefix="lancamento"),
            "receita_form": ReceitaForm(prefix="receita"),
            "despesa_form": DespesaForm(prefix="despesa"),
            "tipos_lancamento": ",".join(
                [tipo[1] for tipo in Lancamento.TIPOS_ESCOLHAS]
            ),
        }
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras:detalhar",
            kwargs={"slug": kwargs.get("carteira_slug")},
        )
        return render(request, self.template_name, {**context, **kwargs})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        lancamento_form = LancamentoForm(request.POST)
        if lancamento_form.is_valid():
            print(lancamento_form.cleaned_data["tipo"])
        else:
            print(lancamento_form.errors)
        return redirect(self.get_success_url())


class LancamentoAtualizar(LoginRequiredBase, UpdateView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = "lancamentos/lancamento_atualizar.html"
    success_url = reverse_lazy("lancamentos:listar")
    context_object_name = "lancamento"

    def get_queryset(self):
        return Lancamento.objects.prefetch_related("categorias").filter(
            criador=self.request.user
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class LancamentoExcluir(LoginRequiredBase, DeleteView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = "lancamentos/lancamento_excluir.html"
    context_object_name = "lancamento"

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
