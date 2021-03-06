from typing import Any, Dict

from base.views import LoginRequiredBase
from carteiras.models import Carteira
from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CartaoForm
from .models import Cartao
from .usecases import criar_novo_cartao


class CartaoLista(LoginRequiredBase, ListView):
    model = Cartao
    template_name = "cartoes/cartao_lista.html"
    fields = ["nome"]
    context_object_name = "cartoes"
    paginate_by = settings.REGISTROS_POR_PAGINA

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Cartao.objects.select_related(
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
        if not context.get("cartoes").exists():
            context["redirecionar"] = context["href_voltar"]
        return context


class CartaoDetalhe(LoginRequiredBase, DetailView):
    model = Cartao
    template_name = "cartoes/cartao_detalhe.html"
    context_object_name = "cartao"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Cartao.objects.select_related(
            "centro_custo", "centro_custo__carteira"
        ).filter(
            centro_custo__carteira__slug=self.kwargs.get("carteira_slug"),
            centro_custo__carteira__usuario_id=self.request.user.pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras_cartoes:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )
        return context


class CartaoCriar(LoginRequiredBase, CreateView):
    model = Cartao
    form_class = CartaoForm
    template_name = "cartoes/cartao_criar.html"
    context_object_name = "cartao"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Cartao.objects.select_related(
            "centro_custo", "centro_custo__carteira"
        ).filter(
            centro_custo__carteira__slug=self.kwargs.get("carteira_slug"),
            centro_custo__carteira__usuario_id=self.request.user.pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras_cartoes:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        carteira_slug = kwargs.get("carteira_slug")
        form = self.form_class(
            request.POST, queryset=self.get_queryset(*args, **kwargs)
        )
        if form.is_valid():
            cartao = form.save(commit=False)
            carteira_slug = kwargs.get("carteira_slug")
            carteira = get_object_or_404(
                Carteira, slug=carteira_slug, usuario_id=request.user.pk
            )
            criar_novo_cartao(cartao=cartao, carteira=carteira)
            return redirect(
                "gerenciamento_carteiras_cartoes:listar",
                carteira_slug=carteira_slug,
            )
        else:
            return render(request, self.template_name, {"form": form, **kwargs})


class CartaoAtualizar(LoginRequiredBase, UpdateView):
    model = Cartao
    form_class = CartaoForm
    template_name = "cartoes/cartao_atualizar.html"
    context_object_name = "cartao"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Cartao.objects.select_related(
            "centro_custo", "centro_custo__carteira"
        ).filter(
            centro_custo__carteira__slug=self.kwargs.get("carteira_slug"),
            centro_custo__carteira__usuario_id=self.request.user.pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras_cartoes:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(
            self.get_queryset(*args, **kwargs), slug=kwargs.get("slug")
        )
        form = self.form_class(
            request.POST, instance=instance, queryset=self.get_queryset(*args, **kwargs)
        )
        if form.is_valid():
            form.save()
            return redirect(
                "gerenciamento_carteiras_cartoes:listar",
                carteira_slug=kwargs.get("carteira_slug"),
            )
        else:
            return render(request, self.template_name, {"form": form})


class CartaoExcluir(LoginRequiredBase, DeleteView):
    model = Cartao
    form_class = CartaoForm
    template_name = "cartoes/cartao_excluir.html"
    context_object_name = "cartao"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Cartao.objects.select_related(
            "centro_custo", "centro_custo__carteira"
        ).filter(
            centro_custo__carteira__slug=self.kwargs.get("carteira_slug"),
            centro_custo__carteira__usuario_id=self.request.user.pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras_cartoes:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )
        return context

    def get_success_url(self):
        return reverse_lazy(
            "gerenciamento_carteiras_cartoes:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        cartao = self.get_queryset(*args, **kwargs).get(slug=kwargs.get("slug"))
        cartao.centro_custo.delete()
        return redirect(self.get_success_url())
