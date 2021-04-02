from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CartaoForm
from .models import Cartao
from carteiras.models import Carteira
from carteiras.models import Tipo


class CartaoLista(ListView):
    model = Cartao
    template_name = 'cartoes/cartao_lista.html'
    fields = ['titulo', 'carteira']
    context_object_name = 'cartoes'
    paginate_by = 20

    def get_queryset(self):
        return Cartao.objects.select_related('carteira')


class CartaoDetalhe(DetailView):
    model = Cartao
    template_name = 'cartoes/cartao_detalhe.html'
    context_object_name = 'cartao'

    def get_queryset(self):
        return Cartao.objects.select_related('carteira')


class CartaoCriar(CreateView):
    model = Cartao
    form_class = CartaoForm
    template_name = 'cartoes/cartao_criar.html'
    context_object_name = 'cartao'

    def get_queryset(self):
        return Cartao.objects.select_related('carteira')

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CartaoForm(request.POST)
        if form.is_valid():
            cartao = form.save(commit=False)
            cartao.slug = slugify(cartao.titulo)
            titulo_ = f'Cartão: {cartao.titulo}'
            slug_ = slugify(titulo_)
            carteira = Carteira(
                titulo=titulo_,
                slug=slug_,
                tipo=Tipo.objects.get(slug='cartao-credito')
            )
            carteira.save()
            cartao.carteira = carteira
            cartao.save()
            return redirect('cartoes:listar')
        else:
            return render(request, self.template_name, {'form': form})


class CartaoAtualizar(UpdateView):
    model = Cartao
    form_class = CartaoForm
    template_name = 'cartoes/cartao_atualizar.html'
    context_object_name = 'cartao'

    def get_queryset(self):
        return Cartao.objects.select_related('carteira')

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        instance = get_object_or_404(Cartao, pk=pk)
        form = CartaoForm(request.POST, instance=instance)
        if form.is_valid():
            cartao = form.save(commit=False)
            cartao.slug = slugify(cartao.titulo)
            carteira = cartao.carteira
            titulo_ = f'Cartão: {cartao.titulo}'
            slug_ = slugify(titulo_)
            carteira.titulo = titulo_
            carteira.slug = slug_
            carteira.save()
            cartao.carteira = carteira
            cartao.save()
            return redirect('cartoes:listar')
        else:
            return render(request, self.template_name, {'form': form})


class CartaoExcluir(DeleteView):
    model = Cartao
    form_class = CartaoForm
    template_name = 'cartoes/cartao_excluir.html'
    context_object_name = 'cartao'
    success_url = reverse_lazy('cartoes:listar')
