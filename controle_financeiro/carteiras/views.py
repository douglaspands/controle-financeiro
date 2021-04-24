from typing import Any, Dict

from base.views import LoginRequiredBase
from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
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
    paginate_by = settings.REGISTROS_POR_PAGINA

    def get_queryset(self) -> QuerySet:
        return Carteira.objects.filter(usuario_id=self.request.user.pk)

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy("gerenciamento:index")
        if not context.get("carteiras").exists():
            context["redirecionar"] = context["href_voltar"]
        return context


class CarteiraDetalhe(LoginRequiredBase, DetailView):
    model = Carteira
    template_name = "carteiras/carteira_detalhe.html"
    context_object_name = "carteira"

    def get_queryset(self) -> QuerySet:
        return Carteira.objects.filter(usuario_id=self.request.user.pk)

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

    def get_queryset(self) -> QuerySet:
        return Carteira.objects.filter(usuario_id=self.request.user.pk)

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy("gerenciamento_carteiras:listar")
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = CarteiraForm(request.POST, queryset=self.get_queryset(*args, **kwargs))
        if form.is_valid():
            carteira = form.save(commit=False)
            carteira.usuario_id = request.user.pk
            form.save()
            return redirect("gerenciamento_carteiras:listar")
        else:
            return render(request, self.template_name, {"form": form})


class CarteiraAtualizar(LoginRequiredBase, UpdateView):
    model = Carteira
    form_class = CarteiraForm
    template_name = "carteiras/carteira_atualizar.html"
    context_object_name = "carteira"

    def get_queryset(self) -> QuerySet:
        return Carteira.objects.filter(usuario_id=self.request.user.pk)

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy("gerenciamento_carteiras:listar")
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(
            self.get_queryset(), slug=kwargs.get("slug")
        )
        form = CarteiraForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("gerenciamento_carteiras:listar")
        else:
            return render(request, self.template_name, {"form": form})


class CarteiraExcluir(LoginRequiredBase, DeleteView):
    model = Carteira
    form_class = CarteiraForm
    template_name = "carteiras/carteira_excluir.html"
    context_object_name = "carteira"
    success_url = reverse_lazy("gerenciamento_carteiras:listar")

    def get_queryset(self) -> QuerySet:
        return Carteira.objects.filter(usuario_id=self.request.user.pk)

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy("gerenciamento_carteiras:listar")
        return context
