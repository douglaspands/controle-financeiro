from django.urls import path

from .views import (DespesaAtualizar, DespesaCriar, DespesaDetalhe,
                    DespesaExcluir, DespesaLista)

app_name = 'despesas'

urlpatterns = [
    path('', DespesaLista.as_view(), name='lista'),
    path('criar', DespesaCriar.as_view(), name='criar'),
    path('<int:pk>', DespesaDetalhe.as_view(), name='detalhe'),
    path('<int:pk>/editar', DespesaAtualizar.as_view(), name='editar'),
    path('<int:pk>/excluir', DespesaExcluir.as_view(), name='excluir'),
]
