from typing import Any, Dict

from base.views import LoginRequiredBase
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CarteiraForm
from .models import Carteira


class CarteiraLista(LoginRequiredBase, ListView):
    model = Carteira
    template_name = "carteiras/carteira_lista.html"
    fields = ["nome"]
    context_object_name = "carteiras"
    paginate_by = 20

    def get_queryset(self) -> QuerySet:
        return Carteira.objects.filter(pessoa_id=self.request.user.pessoa.pk)

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy("gerenciamento:index")
        return context


class CarteiraDetalhe(LoginRequiredBase, DetailView):
    model = Carteira
    template_name = "carteiras/carteira_detalhe.html"
    context_object_name = "carteira"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy("gerenciamento_carteiras:listar")
        return context


class CarteiraCriar(LoginRequiredBase, CreateView):
    model = Carteira
    form_class = CarteiraForm
    template_name = "carteiras/carteira_criar.html"
    context_object_name = "carteira"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = (
            reverse_lazy("gerenciamento_carteiras:listar")
            if Carteira.objects.filter(pessoa_id=self.request.user.pessoa.pk).exists()
            else reverse_lazy("gerenciamento:index")
        )
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CarteiraForm(request.POST)
        if form.is_valid():
            carteira = form.save(commit=False)
            carteira.slug = slugify(carteira.nome)
            carteira.pessoa = request.user.pessoa
            form.save()
            return redirect("gerenciamento_carteiras:listar")
        else:
            return render(request, self.template_name, {"form": form})


class CarteiraAtualizar(LoginRequiredBase, UpdateView):
    model = Carteira
    form_class = CarteiraForm
    template_name = "carteiras/carteira_atualizar.html"
    context_object_name = "carteira"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy("gerenciamento_carteiras:listar")
        return context

    def post(self, request: HttpRequest, slug: str) -> HttpResponse:
        instance = get_object_or_404(Carteira, slug=slug)
        form = CarteiraForm(request.POST, instance=instance)
        if form.is_valid():
            carteira = form.save(commit=False)
            carteira.slug = slugify(carteira.nome)
            carteira.save()
            return redirect("gerenciamento_carteiras:listar")
        else:
            return render(request, self.template_name, {"form": form})


class CarteiraExcluir(LoginRequiredBase, DeleteView):
    model = Carteira
    form_class = CarteiraForm
    template_name = "carteiras/carteira_excluir.html"
    context_object_name = "carteira"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = (
            reverse_lazy("gerenciamento_carteiras:listar")
            if Carteira.objects.filter(pessoa_id=self.request.user.pessoa.pk).exists()
            else reverse_lazy("gerenciamento:index")
        )
        return context

    def get_success_url(self):
        if (
            Carteira.objects.exclude(slug=self.kwargs.get("slug"))
            .filter(pessoa_id=self.request.user.pessoa.pk)
            .exists()
        ):
            return reverse_lazy("gerenciamento_carteiras:listar")
        else:
            return reverse_lazy("gerenciamento:index")
