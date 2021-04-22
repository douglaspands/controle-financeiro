from datetime import datetime
from typing import Any, Dict

from base.views import LoginRequiredBase
from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

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
            **kwargs
        }
        context["lancamento"] = self.get_queryset(*args, **kwargs).get(
            pk=kwargs.get("pk")
        )
        if context["lancamento"].tipo == Lancamento.DESPESA:
            context["despesa"] = context["lancamento"].despesa
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
        usuario_pk = self.request.user.pk
        context = {
            "lancamento_form": kwargs.pop(
                "lancamento_form",
                LancamentoForm(
                    carteira_slug=carteira_slug,
                    usuario_pk=usuario_pk,
                ),
            ),
            "receita_form": kwargs.pop("receita_form", ReceitaForm()),
            "despesa_form": kwargs.pop("despesa_form", DespesaForm()),
            "tipos_lancamento": ",".join(
                [tipo.prefix for tipo in (ReceitaForm, DespesaForm)]
            ),
            "href_voltar": reverse_lazy(
                "gerenciamento_carteiras:detalhar",
                kwargs={"slug": carteira_slug},
            ),
            **kwargs,
        }
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request, self.template_name, self.get_context_data(*args, **kwargs)
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        contexto_erro = {}
        carteira_slug = kwargs["carteira_slug"]
        usuario_pk = request.user.pk

        lancamento_form = LancamentoForm(
            request.POST,
            carteira_slug=carteira_slug,
            usuario_pk=usuario_pk,
        )
        if not lancamento_form.is_valid():
            contexto_erro["lancamento_form"] = lancamento_form

        if (
            not contexto_erro
            and lancamento_form.cleaned_data["tipo"] == Lancamento.RECEITA
        ):
            receita_form = ReceitaForm(request.POST)
            if not receita_form.is_valid():
                contexto_erro["receita_form"] = receita_form
            else:
                criar_nova_receita(
                    lancamento_form=lancamento_form,
                    receita_form=receita_form,
                    carteira_slug=carteira_slug,
                    usuario_pk=usuario_pk,
                )

        if (
            not contexto_erro
            and lancamento_form.cleaned_data["tipo"] == Lancamento.DESPESA
        ):
            despesa_form = DespesaForm(request.POST, centro_custo=lancamento_form.cleaned_data["centro_custo"])
            if not despesa_form.is_valid():
                contexto_erro["despesa_form"] = despesa_form
            else:
                criar_nova_despesa(
                    lancamento_form=lancamento_form,
                    despesa_form=despesa_form,
                    carteira_slug=carteira_slug,
                    usuario_pk=usuario_pk,
                )

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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras:detalhar",
            kwargs={"slug": self.kwargs.get("carteira_slug")},
        )
        return context

    def get_success_url(self):
        return reverse_lazy(
            "gerenciamento_carteiras_lancamentos:listar",
            kwargs={"slug": self.kwargs.get("carteira_slug")},
        )
