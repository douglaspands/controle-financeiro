from django.urls import path

from .views import (LancamentoAtualizar, LancamentoCriar, LancamentoDetalhe,
                    LancamentoExcluir, LancamentoLista)

app_name = 'lancamentos'

urlpatterns = [
    path('', LancamentoLista.as_view(), name='listar'),
    path('criar', LancamentoCriar.as_view(), name='criar'),
    path('<int:pk>', LancamentoDetalhe.as_view(), name='detalhar'),
    path('<int:pk>/editar', LancamentoAtualizar.as_view(), name='editar'),
    path('<int:pk>/excluir', LancamentoExcluir.as_view(), name='excluir'),
]
