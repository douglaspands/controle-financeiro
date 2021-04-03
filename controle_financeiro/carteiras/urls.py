from django.urls import path

from .views import (CarteiraAtualizar, CarteiraCriar, CarteiraDetalhe,
                    CarteiraExcluir, CarteiraLista)

app_name = 'carteiras'

urlpatterns = [
    path('', CarteiraLista.as_view(), name='listar'),
    path('criar', CarteiraCriar.as_view(), name='criar'),
    path('<int:pk>', CarteiraDetalhe.as_view(), name='detalhar'),
    path('<int:pk>/editar', CarteiraAtualizar.as_view(), name='editar'),
    path('<int:pk>/excluir', CarteiraExcluir.as_view(), name='excluir'),
]
