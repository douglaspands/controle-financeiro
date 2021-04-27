from typing import Any, Dict

from base.views import LoginRequiredBase
from carteiras.models import Carteira
from carteiras.usecases import (adicionar_despesa_no_centro_custo,
                                adicionar_receita_no_centro_custo)
from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import DeleteView

from .forms import DespesaForm, LancamentoForm, ReceitaForm
from .models import Lancamento
from .usecases import criar_nova_despesa, criar_nova_receita


class LancamentoLista(LoginRequiredBase, ListView):
    model = Lancamento
    template_name = "lancamentos/lancamento_lista.html"
    context_object_name = "lancamentos"
    fields = ["despesa", "receita"]
    paginate_by = settings.REGISTROS_POR_PAGINA

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Lancamento.objects.select_related(
            "centro_custo", "centro_custo__carteira"
        ).filter(
            centro_custo__carteira__slug=self.kwargs.get("carteira_slug"),
            centro_custo__carteira__usuario_id=self.request.user.pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras:detalhar",
            kwargs={"slug": self.kwargs.get("carteira_slug")},
        )
        if not context.get("lancamentos").exists():
            context["redirecionar"] = context["href_voltar"]
        return context


class LancamentoDetalhe(LoginRequiredBase, View):
    template_name = "lancamentos/lancamento_detalhe.html"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        carteira_slug = self.kwargs.get("carteira_slug")
        usuario_pk = self.request.user.pk
        return Lancamento.objects.select_related(
            "centro_custo",
            "centro_custo__carteira",
        ).prefetch_related(
            "despesa__parcelas"
        ).filter(
            centro_custo__carteira__slug=carteira_slug,
            centro_custo__carteira__usuario_id=usuario_pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = {
            "href_voltar": reverse_lazy(
                "gerenciamento_carteiras_lancamentos:listar",
                kwargs={"carteira_slug": kwargs.get("carteira_slug")},
            ),
            **kwargs,
        }
        context["lancamento"] = self.get_queryset(*args, **kwargs).get(
            pk=kwargs.get("pk")
        )
        if context["lancamento"].tipo == Lancamento.TIPO_DESPESA:
            context["despesa"] = context["lancamento"].despesa
            context["parcelas"] = context["lancamento"].despesa.parcelas.all()
        else:
            context["receita"] = context["lancamento"].receita
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request, self.template_name, self.get_context_data(*args, **kwargs)
        )


class LancamentoCriar(LoginRequiredBase, View):
    template_name = "lancamentos/lancamento_criar.html"

    def get_success_url(self) -> HttpResponse:
        return reverse_lazy(
            "gerenciamento_carteiras_lancamentos:listar",
            kwargs={"carteira_slug": self.kwargs.get("carteira_slug")},
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        carteira_slug = kwargs.get("carteira_slug")
        carteira = get_object_or_404(
            Carteira, slug=carteira_slug, usuario_id=self.request.user.pk
        )
        context = {
            "lancamento_form": kwargs.pop(
                "lancamento_form", LancamentoForm(carteira=carteira)
            ),
            "receita_form": kwargs.pop("receita_form", ReceitaForm()),
            "despesa_form": kwargs.pop("despesa_form", DespesaForm()),
            "tipos_lancamento": ",".join(
                [form.prefix for form in (ReceitaForm, DespesaForm)]
            ),
            "href_voltar": reverse_lazy(
                "gerenciamento_carteiras:detalhar",
                kwargs={"slug": carteira_slug},
            ),
        }
        context.update(kwargs)
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request, self.template_name, self.get_context_data(*args, **kwargs)
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        contexto_erro = {}
        carteira = get_object_or_404(
            Carteira, slug=kwargs.get("carteira_slug"), usuario_id=request.user.pk
        )

        lancamento_form = LancamentoForm(request.POST, carteira=carteira)
        if lancamento_form.is_valid():
            lancamento = lancamento_form.save(commit=False)
        else:
            contexto_erro["lancamento_form"] = lancamento_form

        if (
            not contexto_erro
            and lancamento_form.cleaned_data["tipo"] == Lancamento.TIPO_RECEITA
        ):
            receita_form = ReceitaForm(request.POST)
            if receita_form.is_valid():
                receita = receita_form.save(commit=False)
                criar_nova_receita(
                    lancamento=lancamento, receita=receita, carteira=carteira
                )
            else:
                contexto_erro["receita_form"] = receita_form

        if (
            not contexto_erro
            and lancamento_form.cleaned_data["tipo"] == Lancamento.TIPO_DESPESA
        ):
            despesa_form = DespesaForm(
                request.POST, centro_custo=lancamento.centro_custo
            )
            if despesa_form.is_valid():
                despesa = despesa_form.save(commit=False)
                criar_nova_despesa(
                    lancamento=lancamento, despesa=despesa, carteira=carteira
                )
            else:
                contexto_erro["despesa_form"] = despesa_form

        if contexto_erro:
            return render(
                request,
                self.template_name,
                self.get_context_data(*args, **kwargs, **contexto_erro),
            )
        else:
            return redirect(self.get_success_url())


class LancamentoExcluir(LoginRequiredBase, DeleteView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = "lancamentos/lancamento_excluir.html"
    context_object_name = "lancamento"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras:detalhar",
            kwargs={"slug": self.kwargs.get("carteira_slug")},
        )
        return context

    def get_success_url(self) -> str:
        return reverse_lazy(
            "gerenciamento_carteiras_lancamentos:listar",
            kwargs={"carteira_slug": self.kwargs.get("carteira_slug")},
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        lancamento = get_object_or_404(Lancamento, pk=kwargs.get("pk"))
        if lancamento.tipo == Lancamento.TIPO_RECEITA:
            adicionar_despesa_no_centro_custo(lancamento.centro_custo, lancamento.receita.valor_total)
        else:
            adicionar_receita_no_centro_custo(lancamento.centro_custo, lancamento.despesa.valor_total)
        lancamento.delete()
        return redirect(self.get_success_url())
