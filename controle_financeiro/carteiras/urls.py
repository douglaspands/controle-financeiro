from django.urls import include, path

from .views import (CarteiraAtualizar, CarteiraCriar, CarteiraDetalhe,
                    CarteiraExcluir, CarteiraLista)

app_name = 'carteiras'

urlpatterns = [
    path('', CarteiraLista.as_view(), name='listar'),
    path('criar', CarteiraCriar.as_view(), name='criar'),
    path('<int:pk>', CarteiraDetalhe.as_view(), name='detalhar'),
    path('<int:pk>/editar', CarteiraAtualizar.as_view(), name='editar'),
    path('<int:pk>/excluir', CarteiraExcluir.as_view(), name='excluir'),
    path('<int:carteira_pk>/cartoes/', include('cartoes.urls', namespace='cartoes')),
    # path('<int:carteira_pk>/contas/', include('contas.urls', namespace='contas')),
    path('<int:carteira_pk>/lancamentos/', include('lancamentos.urls', namespace='lancamentos')),
]
