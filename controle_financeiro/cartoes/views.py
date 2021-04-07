from typing import Any, Dict

from base.views import LoginRequiredBase
from carteiras.models import Carteira, Porta
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CartaoForm
from .models import Cartao


class CartaoLista(LoginRequiredBase, ListView):
    model = Cartao
    template_name = "cartoes/cartao_lista.html"
    fields = ["titulo", "carteira"]
    context_object_name = "cartoes"
    paginate_by = 20

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Cartao.objects.select_related("porta", "porta__carteira").filter(
            porta__carteira__slug=self.kwargs.get("carteira_slug")
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class CartaoDetalhe(LoginRequiredBase, DetailView):
    model = Cartao
    template_name = "cartoes/cartao_detalhe.html"
    context_object_name = "cartao"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class CartaoCriar(LoginRequiredBase, CreateView):
    model = Cartao
    form_class = CartaoForm
    template_name = "cartoes/cartao_criar.html"
    context_object_name = "cartao"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        carteira_slug = kwargs.get("carteira_slug")
        form = CartaoForm(request.POST)
        if form.is_valid():
            porta = Porta.objects.create(
                tipo=Porta.CARTAO, carteira=Carteira.objects.get(slug=carteira_slug)
            )
            cartao = form.save(commit=False)
            cartao.slug = slugify(cartao.nome)
            cartao.porta = porta
            cartao.save()
            return redirect(
                "gerenciamento_carteiras_cartoes:listar",
                carteira_slug=carteira_slug,
            )
        else:
            return render(request, self.template_name, {"form": form})


class CartaoAtualizar(LoginRequiredBase, UpdateView):
    model = Cartao
    form_class = CartaoForm
    template_name = "cartoes/cartao_atualizar.html"
    context_object_name = "cartao"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(Cartao, slug=kwargs.get("slug"))
        form = CartaoForm(request.POST, instance=instance)
        if form.is_valid():
            cartao = form.save(commit=False)
            cartao.slug = slugify(cartao.nome)
            cartao.save()
            return redirect(
                "gerenciamento_carteiras_cartoes:listar",
                carteira_slug=request.kwargs.get("carteira_slug"),
            )
        else:
            return render(request, self.template_name, {"form": form})


class CartaoExcluir(LoginRequiredBase, DeleteView):
    model = Cartao
    form_class = CartaoForm
    template_name = "cartoes/cartao_excluir.html"
    context_object_name = "cartao"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def get_success_url(self):
        params = {}
        params["carteira_slug"] = self.kwargs.get("carteira_slug")
        return reverse_lazy(
            "gerenciamento_carteiras_cartoes:listar",
            kwargs=params,
        )
