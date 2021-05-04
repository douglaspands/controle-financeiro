from django.urls import include, path

from .views import (
    CarteiraAtualizar,
    CarteiraCriar,
    CarteiraDetalhe,
    CarteiraDetalheOld,
    CarteiraExcluir,
    CarteiraLista,
)

app_name = "carteiras"

urlpatterns = [
    path("", CarteiraLista.as_view(), name="listar"),
    path("criar", CarteiraCriar.as_view(), name="criar"),
    path("<slug:slug>", CarteiraDetalhe.as_view(), name="detalhar"),
    path("<slug:slug>/detalhar", CarteiraDetalheOld.as_view(), name="detalhar_old"),
    path("<slug:slug>/editar", CarteiraAtualizar.as_view(), name="editar"),
    path("<slug:slug>/excluir", CarteiraExcluir.as_view(), name="excluir"),
    path("<slug:carteira_slug>/cartoes/", include("cartoes.urls", namespace="cartoes")),
    path("<slug:carteira_slug>/contas/", include("contas.urls", namespace="contas")),
    path("<slug:carteira_slug>/lancamentos/", include("lancamentos.urls", namespace="lancamentos")),
]
