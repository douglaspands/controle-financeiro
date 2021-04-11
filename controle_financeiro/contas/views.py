from typing import Any, Dict

from base.views import LoginRequiredBase
from carteiras.models import Carteira, CentroCusto
from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ContaForm
from .models import Conta


class ContaLista(LoginRequiredBase, ListView):
    model = Conta
    template_name = "contas/conta_lista.html"
    fields = ["nome"]
    context_object_name = "contas"
    paginate_by = settings.REGISTROS_POR_PAGINA

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Conta.objects.select_related(
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
        if not context.get("contas").exists():
            context["redirecionar"] = context["href_voltar"]
        return context


class ContaDetalhe(LoginRequiredBase, DetailView):
    model = Conta
    template_name = "contas/conta_detalhe.html"
    context_object_name = "conta"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Conta.objects.select_related(
            "centro_custo", "centro_custo__carteira"
        ).filter(
            centro_custo__carteira__slug=self.kwargs.get("carteira_slug"),
            centro_custo__carteira__usuario_id=self.request.user.pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras_contas:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )
        return context


class ContaCriar(LoginRequiredBase, CreateView):
    model = Conta
    form_class = ContaForm
    template_name = "contas/conta_criar.html"
    context_object_name = "conta"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Conta.objects.select_related(
            "centro_custo", "centro_custo__carteira"
        ).filter(
            centro_custo__carteira__slug=self.kwargs.get("carteira_slug"),
            centro_custo__carteira__usuario_id=self.request.user.pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras_contas:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        carteira_slug = kwargs.get("carteira_slug")
        form = self.form_class(request.POST)
        if form.is_valid():
            centro_custo = CentroCusto.objects.create(
                tipo=CentroCusto.CONTA,
                carteira=Carteira.objects.get(
                    usuario_id=request.user.pk, slug=carteira_slug
                ),
            )
            conta = form.save(commit=False)
            conta.slug = slugify(conta.nome)
            conta.centro_custo = centro_custo
            conta.save()
            return redirect(
                "gerenciamento_carteiras_contas:listar",
                carteira_slug=carteira_slug,
            )
        else:
            return render(request, self.template_name, {"form": form})


class ContaAtualizar(LoginRequiredBase, UpdateView):
    model = Conta
    form_class = ContaForm
    template_name = "contas/conta_atualizar.html"
    context_object_name = "conta"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Conta.objects.select_related(
            "centro_custo", "centro_custo__carteira"
        ).filter(
            centro_custo__carteira__slug=self.kwargs.get("carteira_slug"),
            centro_custo__carteira__usuario_id=self.request.user.pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras_contas:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(self.get_queryset(*args, **kwargs), slug=kwargs.get("slug"))
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.slug = slugify(conta.nome)
            conta.save()
            return redirect(
                "gerenciamento_carteiras_contas:listar",
                carteira_slug=kwargs.get("carteira_slug"),
            )
        else:
            return render(request, self.template_name, {"form": form})


class ContaExcluir(LoginRequiredBase, DeleteView):
    model = Conta
    form_class = ContaForm
    template_name = "contas/conta_excluir.html"
    context_object_name = "conta"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Conta.objects.select_related(
            "centro_custo", "centro_custo__carteira"
        ).filter(
            centro_custo__carteira__slug=self.kwargs.get("carteira_slug"),
            centro_custo__carteira__usuario_id=self.request.user.pk,
        )

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context["href_voltar"] = reverse_lazy(
            "gerenciamento_carteiras_contas:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )
        return context

    def get_success_url(self):
        return reverse_lazy(
            "gerenciamento_carteiras_contas:listar",
            kwargs={
                "carteira_slug": self.kwargs.get("carteira_slug"),
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        conta = self.get_queryset(*args, **kwargs).get(slug=kwargs.get("slug"))
        conta.centro_custo.delete()
        return redirect(self.get_success_url())
