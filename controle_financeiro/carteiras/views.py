from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CarteiraForm
from .models import Carteira


class CarteiraLista(ListView):
    model = Carteira
    template_name = 'carteiras/carteira_lista.html'
    fields = ['titulo', 'tipo']
    context_object_name = 'carteiras'
    paginate_by = 20

    def get_queryset(self):
        return Carteira.objects.select_related('tipo')


class CarteiraDetalhe(DetailView):
    model = Carteira
    template_name = 'carteiras/carteira_detalhe.html'
    context_object_name = 'carteira'

    def get_queryset(self):
        return Carteira.objects.select_related('tipo')


class CarteiraCriar(CreateView):
    model = Carteira
    form_class = CarteiraForm
    template_name = 'carteiras/carteira_criar.html'
    context_object_name = 'carteira'

    def get_queryset(self):
        return Carteira.objects.select_related('tipo')

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CarteiraForm(request.POST)
        if form.is_valid():
            carteira = form.save(commit=False)
            carteira.slug = slugify(carteira.titulo)
            form.save()
            return redirect('carteiras:listar')
        else:
            return render(request, self.template_name, {'form': form})


class CarteiraAtualizar(UpdateView):
    model = Carteira
    form_class = CarteiraForm
    template_name = 'carteiras/carteira_atualizar.html'
    context_object_name = 'carteira'

    def get_queryset(self):
        return Carteira.objects.select_related('tipo')

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        instance = get_object_or_404(Carteira, pk=pk)
        form = CarteiraForm(request.POST, instance=instance)
        if form.is_valid():
            carteira = form.save(commit=False)
            carteira.slug = slugify(carteira.titulo)
            carteira.save()
            return redirect('carteiras:listar')
        else:
            return render(request, self.template_name, {'form': form})


class CarteiraExcluir(DeleteView):
    model = Carteira
    form_class = CarteiraForm
    template_name = 'carteiras/carteira_excluir.html'
    success_url = reverse_lazy('carteiras:listar')
    context_object_name = 'carteira'
