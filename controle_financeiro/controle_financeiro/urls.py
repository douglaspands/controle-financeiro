"""controle_financeiro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.paginas, name='paginas')
Class-based views
    1. Add an import:  from other_app.views import Publico
    2. Add a URL to urlpatterns:  path('', Publico.as_view(), name='paginas')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", include("paginas.urls", namespace="paginas")),
    path("admin/", admin.site.urls),
    path("autenticacao/", include("autenticacao.urls", namespace="autenticacao")),
    path("gerenciamento/", include("gerenciamento.urls", namespace="gerenciamento")),
    path(
        "gerenciamento/carteiras/",
        include("carteiras.urls", namespace="gerenciamento_carteiras"),
    ),
    path(
        "gerenciamento/carteiras/<slug:carteira_slug>/cartoes/",
        include("cartoes.urls", namespace="gerenciamento_carteiras_cartoes"),
    ),
    path(
        "gerenciamento/carteiras/<slug:carteira_slug>/contas/",
        include("contas.urls", namespace="gerenciamento_carteiras_contas"),
    ),
    path(
        "gerenciamento/carteiras/<slug:carteira_slug>/lancamentos/",
        include("lancamentos.urls", namespace="gerenciamento_carteiras_lancamentos"),
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r"^__debug__/", include(debug_toolbar.urls, namespace="djdt")),
    ]
