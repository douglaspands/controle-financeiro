from django.urls import path

from .views import (ContaAtualizar, ContaCriar, ContaDetalhe,
                    ContaExcluir, ContaLista)

app_name = 'contas'

urlpatterns = [
    path('', ContaLista.as_view(), name='listar'),
    path('criar', ContaCriar.as_view(), name='criar'),
    path('<slug:slug>', ContaDetalhe.as_view(), name='detalhar'),
    path('<slug:slug>/editar', ContaAtualizar.as_view(), name='editar'),
    path('<slug:slug>/excluir', ContaExcluir.as_view(), name='excluir'),
]
