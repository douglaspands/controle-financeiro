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
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("paginas.urls", namespace="paginas")),
    path("admin/", admin.site.urls),
    path("autenticacao/", include("autenticacao.urls", namespace="autenticacao")),
    path("gerenciamento/", include("gerenciamento.urls", namespace="gerenciamento")),
    path("cartoes/", include("cartoes.urls", namespace="cartoes")),
    path("contas/", include("contas.urls", namespace="contas")),
    path("lancamentos/", include("lancamentos.urls", namespace="lancamentos")),
    path("carteiras/", include("carteiras.urls", namespace="carteiras")),
]
