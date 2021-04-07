from django.urls import path

from .views import (CartaoAtualizar, CartaoCriar, CartaoDetalhe,
                    CartaoExcluir, CartaoLista)

app_name = 'cartoes'

urlpatterns = [
    path('', CartaoLista.as_view(), name='listar'),
    path('criar', CartaoCriar.as_view(), name='criar'),
    path('<slug:slug>', CartaoDetalhe.as_view(), name='detalhar'),
    path('<slug:slug>/editar', CartaoAtualizar.as_view(), name='editar'),
    path('<slug:slug>/excluir', CartaoExcluir.as_view(), name='excluir'),
]
