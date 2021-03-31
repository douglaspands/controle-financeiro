from django.shortcuts import render, redirect
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
    paginate_by = 25

    def get_queryset(self):
        return Carteira.objects.select_related('tipo')


class CarteiraDetalhe(DetailView):
    model = Carteira
    template_name = 'carteiras/carteira_detalhe.html'

    def get_queryset(self):
        return Carteira.objects.select_related('tipo')


class CarteiraCriar(CreateView):
    model = Carteira
    form_class = CarteiraForm
    template_name = 'carteiras/carteira_criar.html'
    success_url = reverse_lazy('carteiras:lista')

    def get_queryset(self):
        return Carteira.objects.select_related('tipo')


class CarteiraAtualizar(UpdateView):
    model = Carteira
    form_class = CarteiraForm
    template_name = 'carteiras/carteira_atualizar.html'
    success_url = reverse_lazy('carteiras:lista')

    def get_queryset(self):
        return Carteira.objects.select_related('tipo')

    # def post(self, request, pk):
    #     form = CarteiraForm(request.POST, pk=pk)
    #     if form.is_valid():
    #         form.cleaned_data['slug'] = slugify(form.cleaned_data['titulo'])
    #         form.save()
    #         return redirect('carteiras:lista')
    #     else:
    #         return render(request, self.template_name, {'form': form})


class CarteiraExcluir(DeleteView):
    model = Carteira
    form_class = CarteiraForm
    template_name = 'carteiras/carteira_excluir.html'
    success_url = reverse_lazy('carteiras:lista')
