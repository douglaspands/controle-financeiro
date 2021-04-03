from django.urls import path

from .views import (CartaoAtualizar, CartaoCriar, CartaoDetalhe,
                    CartaoExcluir, CartaoLista)

app_name = 'cartoes'

urlpatterns = [
    path('', CartaoLista.as_view(), name='listar'),
    path('criar', CartaoCriar.as_view(), name='criar'),
    path('<int:pk>', CartaoDetalhe.as_view(), name='detalhar'),
    path('<int:pk>/editar', CartaoAtualizar.as_view(), name='editar'),
    path('<int:pk>/excluir', CartaoExcluir.as_view(), name='excluir'),
]
