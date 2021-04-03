from datetime import datetime

from base.views import LoginRequiredBase
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import DespesaForm
from .models import Despesa


class DespesaLista(LoginRequiredBase, ListView):
    model = Despesa
    template_name = "despesas/despesa_lista.html"
    context_object_name = "despesas"
    fields = ["categorias", "descricao", "valor", "datahora", "carteira"]
    paginate_by = 20

    def get_queryset(self):
        return Despesa.objects.prefetch_related("categorias").filter(
            criador=self.request.user
        )


class DespesaDetalhe(LoginRequiredBase, DetailView):
    model = Despesa
    template_name = "despesas/despesa_detalhe.html"
    context_object_name = "despesa"

    def get_queryset(self):
        return Despesa.objects.prefetch_related("categorias").filter(
            criador=self.request.user
        )


class DespesaCriar(LoginRequiredBase, CreateView):
    model = Despesa
    form_class = DespesaForm
    template_name = "despesas/despesa_criar.html"
    success_url = reverse_lazy("despesas:listar")
    context_object_name = "despesa"

    def get_queryset(self):
        return Despesa.objects.prefetch_related("categorias").filter(
            criador=self.request.user
        )

    def get_initial(self):
        initial = super(DespesaCriar, self).get_initial()
        initial.update({"parcelado": 1, "datahora": datetime.now()})
        return initial

    def post(self, request: HttpRequest) -> HttpResponse:
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.criador = request.user
            despesa.save()
            return redirect("despesas:listar")
        else:
            return render(request, self.template_name, {"form": form})


class DespesaAtualizar(LoginRequiredBase, UpdateView):
    model = Despesa
    form_class = DespesaForm
    template_name = "despesas/despesa_atualizar.html"
    success_url = reverse_lazy("despesas:listar")
    context_object_name = "despesa"

    def get_queryset(self):
        return Despesa.objects.prefetch_related("categorias").filter(
            criador=self.request.user
        )


class DespesaExcluir(LoginRequiredBase, DeleteView):
    model = Despesa
    form_class = DespesaForm
    template_name = "despesas/despesa_excluir.html"
    success_url = reverse_lazy("despesas:listar")
    context_object_name = "despesa"

    def get_queryset(self):
        return Despesa.objects.prefetch_related("categorias").filter(
            criador=self.request.user
        )
